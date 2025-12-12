from classes.livre import Livre
from classes.bande_dessinee import BandeDessinee
from classes.dictionnaire import Dictionnaire
from classes.journal import Journal
from classes.bibliotheque import Bibliotheque
from datetime import date


def ajouter_document(biblio: Bibliotheque) -> None:
    print("\n--- Ajouter un document ---")
    print("1 - Livre")
    print("2 - Bande dessinée")
    print("3 - Dictionnaire")
    print("4 - Journal")
    choix = input("Type : ").strip()

    titre = input("Titre : ").strip()

    if choix in {"1", "2", "3"}:
        auteur = input("Auteur : ").strip()

    if choix == "1":
        doc = Livre(titre, auteur)
    elif choix == "2":
        dessinateur = input("Dessinateur : ").strip()
        doc = BandeDessinee(titre, auteur, dessinateur)
    elif choix == "3":
        doc = Dictionnaire(titre, auteur)
    elif choix == "4":
        annee = int(input("Année de parution : "))
        mois = int(input("Mois : "))
        jour = int(input("Jour : "))
        doc = Journal(titre, date(annee, mois, jour))
    else:
        print("Choix erroné!")
        return

    biblio.ajouter_document(doc)
    print("Document ajouté.\n")


def supprimer_document(biblio: Bibliotheque) -> None:
    print("\n--- Supprimer un document ---")
    titre = input("Titre : ").strip()
    if biblio.supprimer_document(titre):
        print("Document supprimé.\n")
    else:
        print("Document introuvable.\n")


def afficher_documents(biblio: Bibliotheque) -> None:
    print("\n--- Liste des documents ---")
    docs = biblio.lister_documents()
    for d in docs:
        print(d)
    if not docs:
        print("(aucun document)")
    print()
