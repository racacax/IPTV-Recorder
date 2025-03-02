DOCKER_EXE		= docker exec -i
DOCKER_EXE_TTY	= docker exec -it
DCO_EXE			= docker compose
PYTHON			= ${DOCKER_EXE_TTY} iptvrecorder python

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
	${DOCKER_EXE_TTY} iptvrecorder bash

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
lint:
	python -m black .
	python -m flake8 .
i18n-generate:
	django-admin makemessages -l en --ignore "venv/*" --ignore "frontend/*"
	django-admin makemessages -l fr --ignore "venv/*" --ignore "frontend/*"
	python manage.py generate_js_i18n

i18n-compile:
	django-admin compilemessages --ignore "venv/*" --ignore "frontend/*"

