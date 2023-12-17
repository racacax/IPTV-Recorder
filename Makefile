DOCKER_EXE		= docker exec -i
DOCKER_EXE_TTY	= docker exec -it
DCO_EXE			= docker-compose
PYTHON			= ${DOCKER_EXE_TTY} iptv-recorder_web_1 python

up_d:
	${DCO_EXE} up
up_detached_d:
	${DCO_EXE} up -d
update build:
	${DCO_EXE} build
migrations_d:
	${PYTHON} manage.py makemigrations
migrate_d:
	${PYTHON} manage.py migrate
init_d: migrate_d
	${PYTHON} manage.py createsuperuser
bash ssh:
	${DOCKER_EXE_TTY} iptv-recorder_web_1 bash

up:
	python start.py
up_detached:
	python start.py & disown
migrations:
	python manage.py makemigrations
migrate:
	python manage.py migrate
init: migrate
	python manage.py createsuperuser