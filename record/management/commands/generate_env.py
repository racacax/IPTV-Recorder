import json
import os

from django.core.management import BaseCommand
from django.core.management.utils import get_random_secret_key

from iptvrecorder.settings import BASE_DIR
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = _("Création du .env")

    def get_env_content(self, obj):
        content = ""
        for key, value in obj.items():
            content += f"{key}={value}\n"
        return content

    def handle(self, *args, **options):
        print(_("Génération du .env"))
        env_path = BASE_DIR / ".env"
        if os.path.exists(env_path):
            if input(_("Le fichier .env existe. Voulez-vous l'écraser ? (y/n)")).lower() != "y":
                print(_("Etape de modification du fichier .env ignorée"))
                return
        env = {
            "SECRET_KEY": get_random_secret_key(),
            "ALLOWED_HOSTS": ["localhost", "0.0.0.0"],
            "DEBUG": True,
            "RUNNING_PORT": 8000,
            "ENABLE_UWSGI": False,
            "LANGUAGE_CODE": "en",
        }
        additional_host = input(
            _(
                "Veuillez indiquer l'hôte à laquelle votre programme sera disponible "
                "(par défaut localhost/0.0.0.0). Laisser vide pour passer :"
            )
        )
        if additional_host:
            env["ALLOWED_HOSTS"].append(additional_host)
        port = input(
            _("Veuillez rentrer le port sur lequel vous voulez faire fonctionner l'application (8000 par défaut) :")
        )
        if port:
            env["PORT"] = int(port)
        lang = input(_("Veuillez entrer la langue à utiliser (fr ou en. en par défaut) :"))
        if lang:
            env["LANGUAGE_CODE"] = lang.strip().lower() == "fr" and "fr" or "en"
        env["ALLOWED_HOSTS"] = json.dumps(env["ALLOWED_HOSTS"])
        print(_("Contenu du fichier .env"))
        content = self.get_env_content(env)
        print(content)
        with open(env_path, "w") as env_file:
            env_file.write(content)
            env_file.close()
        print(_("Pour appliquer vos changements, le programme devra être redémarré."))
