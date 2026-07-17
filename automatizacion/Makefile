IMAGE ?= stackgen:1.0
BASE_DIR ?= $(abspath ..)
lang :=
dbv :=

LANGARG := $(if $(lang),--lang $(lang))
DBVARG := $(if $(dbv),--dbv $(dbv))
GENERATEARG := $(if $(solo_generar),--solo-generar)
DOCKER_SOCKET_GID := $(shell stat -c '%g' /var/run/docker.sock 2>/dev/null)

.PHONY: build crear stacks help

build:
	docker build -t $(IMAGE) .

crear:
	@test -n "$(nombre)" || (echo "Falta nombre=<proyecto>" && exit 1)
	@test -n "$(stack)" || (echo "Falta stack=<plantilla>" && exit 1)
	docker run --rm \
		-e HOME=/tmp \
		-e PROJECTS_BASE_DIR=/srv/proyectosDocker \
		--user "$(shell id -u):$(shell id -g)" \
		$(if $(DOCKER_SOCKET_GID),--group-add $(DOCKER_SOCKET_GID)) \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $(BASE_DIR):/srv/proyectosDocker \
		$(IMAGE) \
		-n $(nombre) -s $(stack) $(LANGARG) $(DBVARG) $(GENERATEARG)

stacks:
	@find templates -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort

help:
	@echo "Uso:"
	@echo "  make build"
	@echo "  make stacks"
	@echo "  make crear nombre=<proyecto> stack=<plantilla> [lang=<version>] [dbv=<version>]"
	@echo "  make crear nombre=<proyecto> stack=<plantilla> solo_generar=1"
