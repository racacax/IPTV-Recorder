from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils.translation import gettext_lazy as _
from record.models import Playlist


class Command(BaseCommand):
    help = _("Ajouter une playlist")

    def handle(self, *args, **options):
        print(_("Ajouter une playlist"))
        users = User.objects.all()
        print(_("Utilisateurs : "))
        for user in users:
            print(_(f"{user.id}) {user.username}"))
        user_id = int(input(_("Entrez le numéro de l'utilisateur: ")))
        user = User.objects.get(id=user_id)

        name = input(_("Entrez le nom de la playlist : "))
        url = input(_("Entrez l'URL de la playlist : "))
        refresh_gap = int(input(_("Entrez la fréquence de rafraichissement de la playlist (en heures. ex : 12) : ")))
        Playlist.objects.create(url=url, name=name, user=user, refresh_gap=refresh_gap)
        print(_("Playlist ajoutée"))
