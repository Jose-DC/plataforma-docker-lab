import argparse
import base64
import os
import re
import secrets
import shutil
import subprocess
from pathlib import Path

DEFAULT_BASE_DIR = Path(os.environ.get("PROJECTS_BASE_DIR", "/srv/proyectosDocker"))
PROJECT_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{0,62}$")


def available_stacks(base_dir):
    templates_dir = base_dir / "automatizacion" / "templates"
    if not templates_dir.is_dir():
        return []

    return sorted(
        item.name
        for item in templates_dir.iterdir()
        if item.is_dir() and (item / "docker-compose.yml").is_file()
    )


def parse_args():
    base_dir = DEFAULT_BASE_DIR
    stacks = available_stacks(base_dir)

    parser = argparse.ArgumentParser(
        description="Genera entornos Docker reproducibles a partir de plantillas."
    )
    parser.add_argument(
        "--nombre",
        "-n",
        required=True,
        help="Nombre del proyecto: minusculas, numeros, guion o guion bajo.",
    )
    parser.add_argument(
        "--stack",
        "-s",
        required=True,
        choices=stacks or None,
        help="Plantilla disponible en automatizacion/templates.",
    )
    parser.add_argument("--lang", help="Version del lenguaje (opcional).")
    parser.add_argument("--dbv", help="Version de la base de datos (opcional).")
    parser.add_argument(
        "--solo-generar",
        action="store_true",
        help="Copia y configura la plantilla sin crear redes ni iniciar contenedores.",
    )
    args = parser.parse_args()

    if not stacks:
        parser.error(f"No se encontraron plantillas en {base_dir / 'automatizacion/templates'}")
    if not PROJECT_NAME_PATTERN.fullmatch(args.nombre):
        parser.error(
            "El nombre debe comenzar con letra o numero, usar solo minusculas, "
            "numeros, guiones o guiones bajos, y tener hasta 63 caracteres."
        )

    args.base_dir = base_dir
    return args


def run(command):
    return subprocess.run(command, check=True, text=True)


def create_environment(args):
    project_dir = args.base_dir / args.nombre
    template_dir = args.base_dir / "automatizacion" / "templates" / args.stack
    proxy_compose = args.base_dir / "proxy" / "docker-compose.yml"

    if project_dir.exists():
        raise FileExistsError(f"El directorio de destino ya existe: {project_dir}")
    if not template_dir.is_dir():
        raise FileNotFoundError(f"No existe la plantilla: {template_dir}")
    if not args.solo_generar and not proxy_compose.is_file():
        raise FileNotFoundError(f"No se encontro la configuracion del proxy: {proxy_compose}")

    shutil.copytree(template_dir, project_dir)
    print(f"Plantilla '{args.stack}' copiada en {project_dir}")

    replace_project_name(project_dir / "docker-compose.yml", args.nombre)
    create_env(args, project_dir)

    if args.solo_generar:
        print("Proyecto generado. No se crearon redes ni contenedores.")
        return

    create_network(args.nombre)
    update_proxy_compose(proxy_compose, args.nombre)
    start_containers(project_dir)
    connect_proxy(args.nombre)


def replace_project_name(compose_path, project_name):
    content = compose_path.read_text(encoding="utf-8")
    compose_path.write_text(
        content.replace("${PROJECT}", project_name),
        encoding="utf-8",
    )


def create_env(args, project_dir):
    example_path = project_dir / ".env.example"
    env_path = project_dir / ".env"

    if not example_path.is_file():
        print("La plantilla no incluye .env.example; no se creo .env.")
        return

    replacements = {
        "PROJECT": args.nombre,
        "LANG_VERSION": args.lang,
        "DB_VERSION": args.dbv,
    }
    output = []

    for raw_line in example_path.read_text(encoding="utf-8").splitlines():
        if not raw_line or raw_line.lstrip().startswith("#") or "=" not in raw_line:
            output.append(raw_line)
            continue

        key, value = raw_line.split("=", 1)
        clean_key = key.strip()
        current_value = value.split("#", 1)[0].strip()

        if replacements.get(clean_key):
            output.append(f"{clean_key}={replacements[clean_key]}")
        elif current_value.startswith("change-me"):
            output.append(f"{clean_key}={generate_secret(clean_key)}")
        else:
            output.append(raw_line)

    env_path.write_text("\n".join(output) + "\n", encoding="utf-8")
    if os.name != "nt":
        os.chmod(env_path, 0o600)
    print(f"Archivo .env creado para '{args.nombre}'")


def generate_secret(key):
    if key == "APP_KEY":
        encoded = base64.b64encode(os.urandom(32)).decode("ascii")
        return f"base64:{encoded}"
    return secrets.token_urlsafe(24)


def create_network(project_name):
    network = f"proxy_{project_name}_net"
    result = subprocess.run(
        ["docker", "network", "ls", "--format", "{{.Name}}"],
        check=True,
        capture_output=True,
        text=True,
    )

    if network not in result.stdout.splitlines():
        run(["docker", "network", "create", "--driver", "bridge", network])
        print(f"Red externa '{network}' creada")
    else:
        print(f"Red externa '{network}' reutilizada")


def update_proxy_compose(compose_path, project_name):
    import ruamel.yaml

    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True

    with compose_path.open("r", encoding="utf-8") as file:
        compose_data = yaml.load(file)

    network = f"proxy_{project_name}_net"
    services = compose_data.get("services", {})
    networks = compose_data.setdefault("networks", {})

    if "npm" not in services:
        raise KeyError("El compose del proxy no contiene el servicio 'npm'.")

    npm_networks = services["npm"].setdefault("networks", [])
    if network not in npm_networks:
        npm_networks.append(network)
    networks.setdefault(network, {"external": True})

    with compose_path.open("w", encoding="utf-8") as file:
        yaml.dump(compose_data, file)

    print(f"Red '{network}' registrada en el compose del proxy")


def start_containers(project_dir):
    print(f"Iniciando contenedores de {project_dir.name}...")
    run(["docker", "compose", "-f", str(project_dir / "docker-compose.yml"), "up", "-d"])


def connect_proxy(project_name):
    proxy_container = "infra_nginx_proxy"
    network = f"proxy_{project_name}_net"
    result = subprocess.run(
        ["docker", "network", "inspect", network, "--format", "{{json .Containers}}"],
        check=True,
        capture_output=True,
        text=True,
    )

    if proxy_container not in result.stdout:
        run(["docker", "network", "connect", network, proxy_container])
        print(f"Proxy conectado a la red '{network}'")

    run(["docker", "restart", proxy_container])
    print("Proxy reiniciado para aplicar la nueva conexion")


def main():
    args = parse_args()
    try:
        create_environment(args)
    except (FileExistsError, FileNotFoundError, KeyError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Error: {error}") from error


if __name__ == "__main__":
    main()
