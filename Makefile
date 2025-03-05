DOCKER_EXE		= docker exec -i iptvrecorder
DOCKER_EXE_TTY	= docker exec -it iptvrecorder
DCO_EXE			= docker compose

up_d:
	${DCO_EXE} up
up_detached_d:
	${DCO_EXE} up -d
stop_d:
	${DCO_EXE} stop
update build:
	${DCO_EXE} build
migrations_d:
	${DOCKER_EXE_TTY} make migrations
migrate_d:
	${DOCKER_EXE_TTY} make migrate
init_d:
	${DOCKER_EXE_TTY} make init
i18n-generate_d:
	${DOCKER_EXE_TTY} make i18n-generate
i18n-compile_d:
	${DOCKER_EXE_TTY} make i18n-compile
lint_d:
	${DOCKER_EXE} make lint
bash ssh:
	${DOCKER_EXE_TTY} bash

up:
	python start.py
up_detached:
	python start.py & disown
stop:
	python stop.py
migrations:
	python manage.py makemigrations
migrate:
	python manage.py migrate
init:
	python manage.py generate_env
	python manage.py createsuperuser
	python manage.py set_user_data
	python manage.py add_playlist
lint:
	python -m black .
	python -m flake8 .
i18n-generate:
	django-admin makemessages -l en --ignore "venv/*" --ignore "frontend/*"
	django-admin makemessages -l fr --ignore "venv/*" --ignore "frontend/*"
	python manage.py generate_js_i18n

i18n-compile:
	django-admin compilemessages --ignore "venv/*" --ignore "frontend/*"

build-js:
	cd frontend && npm run build
	rm -f static/assets/index-*
	rm -f record/templates/index.html
	mv dist/assets/index-* static/assets/
	mv dist/index.html record/templates/
	sed -i -e 's|http://localhost:8000||g' \
		   -e 's|window\.CSRF_TOKEN = ""|window.CSRF_TOKEN = "{{ csrf_token }}"|g' \
		   -e 's|/assets|/static/assets|g' record/templates/index.html
