from django.contrib.auth.models import User
from django.core.management import BaseCommand

from record.models import UserData


class Command(BaseCommand):
    help = "Définir les données utilisateurs"

    def handle(self, *args, **options):
        print("Définition du profil utilisateur")
        users = User.objects.all()
        print("Utilisateurs : ")
        for user in users:
            print(f"{user.id}) {user.username}")
        user_id = int(input("Entrez le numéro de l'utilisateur : "))
        user = User.objects.get(id=user_id)

        writing_directory = input("Entrez le chemin de destination des enregistrements pour cet utilisateur : ")
        UserData.objects.update_or_create(user=user, defaults={"writing_directory": writing_directory})
        print("Profil utilisateur crée")