from classes.livre import Livre
from classes.bande_dessinee import BandeDessinee
from classes.dictionnaire import Dictionnaire
from classes.journal import Journal
from classes.bibliotheque import Bibliotheque
from datetime import date


from classes.livre import Livre
from classes.bande_dessinee import BandeDessinee
from classes.dictionnaire import Dictionnaire
from classes.journal import Journal
from classes.bibliotheque import Bibliotheque


def ajouter_document(biblio: Bibliotheque) -> None:
    print("\n--- Ajouter un document ---")
    print("1 - Livre")
    print("2 - Bande dessinée")
    print("3 - Dictionnaire")
    print("4 - Journal")
    choix = input("Type : ").strip()

    titre = input("Titre : ").strip()
    if not titre:
        print("Erreur : le titre est obligatoire.\n")
        return

    # Types avec auteur obligatoire
    if choix in {"1", "2", "3"}:
        auteur = input("Auteur : ").strip()
        if not auteur:
            print("Erreur : l'auteur est obligatoire.\n")
            return

    # 1 - Livre
    if choix == "1":
        doc = Livre(titre, auteur)

    # 2 - Bande dessinée
    elif choix == "2":
        dessinateur = input("Dessinateur : ").strip()
        if not dessinateur:
            print("Erreur : le dessinateur est obligatoire pour une bande dessinée.\n")
            return
        doc = BandeDessinee(titre, auteur, dessinateur)

    # 3 - Dictionnaire
    elif choix == "3":
        doc = Dictionnaire(titre, auteur)

    # 4 - Journal
    elif choix == "4":
        date_parution = input("Date de parution (AAAA-MM-JJ) : ").strip()
        if not date_parution:
            print("Erreur : la date de parution est obligatoire pour un journal.\n")
            return
        doc = Journal(titre, date_parution)

    else:
        print("Erreur : type de document invalide.\n")
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
