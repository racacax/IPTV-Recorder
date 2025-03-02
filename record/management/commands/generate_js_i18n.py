import os
import re
from copy import deepcopy

import polib
from django.core.management import BaseCommand


from django.utils.translation import gettext_lazy as _

from iptvrecorder.settings import AVAILABLE_LANGUAGES, BASE_DIR


class Command(BaseCommand):
    help = _("Générer les traductions JS")

    def handle(self, *args, **options):
        frontend_path = BASE_DIR / "frontend"
        locale_path = BASE_DIR / "locale"
        files = [
            file
            for file in frontend_path.rglob("*")
            if file.suffix in {".ts", ".vue"} and "node_modules" not in file.parts
        ]
        base_translation_file = {}
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                pattern = r'gettext\(["\'](.*?)["\']\)'
                matches = re.findall(pattern, content)
                for match in matches:
                    base_translation_file[match] = ""
                f.close()
        for lang in AVAILABLE_LANGUAGES:
            regional_translation_file = deepcopy(base_translation_file)
            path = locale_path / lang / "LC_MESSAGES" / "djangojs.po"
            if os.path.exists(path):
                po = polib.pofile(path)
                for entry in po:
                    regional_translation_file[entry.msgid] = entry.msgstr
            po = polib.POFile()
            po.metadata = {
                "Content-Type": "text/plain; charset=UTF-8",
                "Content-Transfer-Encoding": "8bit",
            }
            for source, translation in regional_translation_file.items():
                entry = polib.POEntry(msgid=source, msgstr=translation)
                po.append(entry)
            po.save(path)
