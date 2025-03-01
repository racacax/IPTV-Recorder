import subprocess
import threading
import time

import environ
import psutil

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env("./.env")

HOST = env("HOST", default="0.0.0.0")
PORT = env("RUNNING_PORT", default=8000)
ENABLE_UWSGI = env("ENABLE_UWSGI", cast=bool, default=False)


def is_port_in_use(port):
    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr.port == port:
            return True
    return False


def launch_django_web_server():
    subprocess.Popen(f"exec python manage.py runserver {HOST}:{PORT}", shell=True)


def launch_uwsgi():
    subprocess.Popen(
        "exec uwsgi --chdir=. --module=iptvrecorder.wsgi:application --env "
        f"DJANGO_SETTINGS_MODULE=iptvrecorder.settings --master --pidfile=./project-master.pid --http {HOST}:{PORT} "
        "--processes=2 --harakiri=20 --max-requests=20 --vacuum",
        shell=True,
    )


def launch_recordings_check():
    while not is_port_in_use(PORT):
        pass
    print("Starting recordings check process...")
    subprocess.Popen("exec python manage.py recordings_check", shell=True)


if not ENABLE_UWSGI:
    threading.Thread(target=launch_django_web_server, args=[]).start()
else:
    threading.Thread(target=launch_uwsgi, args=[]).start()

launch_recordings_check()
while True:
    time.sleep(1)
