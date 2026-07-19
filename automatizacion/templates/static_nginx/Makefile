PROJECT=$(shell grep PROJECT .env | cut -d '=' -f2)

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose down && docker compose up -d

ps:
	docker compose ps

logs:
	docker compose logs -f

shell:
	docker exec -it $(PROJECT)_app bash

destroy:
	docker compose down --remove-orphans
	-docker network disconnect proxy_$(PROJECT)_net infra_nginx_proxy 2>/dev/null || true
	@echo "Stack '$(PROJECT)' destruido (contenedor y redes externas desconectadas)"
