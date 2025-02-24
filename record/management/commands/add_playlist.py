from django.contrib.auth.models import User
from django.core.management import BaseCommand

from record.models import UserData, Playlist


class Command(BaseCommand):
    help = "Ajouter une playlist"

    def handle(self, *args, **options):
        print("Ajouter une playlist")
        users = User.objects.all()
        print("Utilisateurs : ")
        for user in users:
            print(f"{user.id}) {user.username}")
        user_id = int(input("Entrez le numéro de l'utilisateur: "))
        user = User.objects.get(id=user_id)

        name = input("Entrez le nom de la playlist : ")
        url = input("Entrez l'URL de la playlist : ")
        refresh_gap = int(input("Entrez la fréquence de rafraichissement de la playlist (en heures. ex : 12) : "))
        Playlist.objects.create(url=url, name=name, user=user, refresh_gap=refresh_gap)
        print("Playlist ajoutée")