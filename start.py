import os
import subprocess
import threading
import time

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env("./.env")

PORT = env('RUNNING_PORT', default=8000)
ENABLE_UWSGI = env('ENABLE_UWSGI', cast=bool, default=False)
def launch_django_web_server():
    process = subprocess.Popen(f"exec python manage.py runserver 0.0.0.0:{PORT}", shell=True)


def launch_uwsgi():
    process = subprocess.Popen(
        "exec uwsgi --chdir=. --module=iptvrecorder.wsgi:application --env "
        f"DJANGO_SETTINGS_MODULE=iptvrecorder.settings --master --pidfile=./project-master.pid --http 0.0.0.0:{PORT} "
        "--processes=2 --harakiri=20 --max-requests=20 --vacuum",
        shell=True)


def launch_recordings_check():
    process = subprocess.Popen("exec ./recordings_check.sh", shell=True)


if not ENABLE_UWSGI:
    threading.Thread(target=launch_django_web_server, args=[]).start()
else:
    threading.Thread(target=launch_uwsgi, args=[]).start()

launch_recordings_check()
while True:
    time.sleep(1);
