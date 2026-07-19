PROJECT=$(shell grep PROJECT .env | cut -d '=' -f2)

up:
	docker compose up -d

up-all:
	docker compose --profile pgadmin up -d

down:
	docker compose down

down-all:
	docker compose --profile pgadmin down

restart:
	docker compose down && docker compose up -d

rebuild:
	docker compose down
	docker compose build
	docker compose up -d

ps:
	docker compose ps

logs:
	docker compose logs -f

pgadmin:
	docker compose --profile pgadmin up -d pgadmin

shell:
	docker exec -it $(PROJECT)_app sh

dbshell:
	docker exec -it $(PROJECT)_db bash

destroy:
	docker compose --profile pgadmin down --volumes --remove-orphans
	-docker volume rm $(PROJECT)_db_data 2>/dev/null || true
	-docker volume rm $(PROJECT)_pgadmin_data 2>/dev/null || true
	-docker network disconnect proxy_$(PROJECT)_net infra_nginx_proxy 2>/dev/null || true
	-docker network rm $(PROJECT)_net 2>/dev/null || true
	@echo "Stack '$(PROJECT)' destruido (contenedores, volúmenes y red interna eliminados)"
