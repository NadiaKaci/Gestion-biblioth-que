from datetime import date
from classes.bibliotheque import Bibliotheque


def ajouter_emprunt(biblio: Bibliotheque) -> None:
    print("\n--- Ajouter un emprunt ---")
    prenom = input("Prénom de l'adhérent : ").strip()
    nom = input("Nom de l'adhérent : ").strip()
    titre = input("Titre du livre : ").strip()

    adherent = next(
        (a for a in biblio.adherents if a.nom == nom and a.prenom == prenom), None
    )
    if adherent is None:
        print("Adhérent introuvable.\n")
        return

    auj = date.today()
    if biblio.emprunter_livre(adherent, titre, auj):
        print(f"Emprunt créé le {auj.isoformat()}.\n")
    else:
        print("Livre introuvable ou non disponible.\n")


def retour_emprunt(biblio: Bibliotheque) -> None:
    print("\n--- Retour d'un emprunt ---")
    prenom = input("Prénom de l'adhérent : ").strip()
    nom = input("Nom de l'adhérent : ").strip()
    titre = input("Titre du livre : ").strip()

    adherent = next(
        (a for a in biblio.adherents if a.nom == nom and a.prenom == prenom), None
    )
    if adherent is None:
        print("Adhérent introuvable.\n")
        return

    auj = date.today()
    if biblio.retourner_livre(adherent, titre, auj):
        print(f"Livre retourné le {auj.isoformat()}.\n")
    else:
        print("Aucun emprunt correspondant trouvé.\n")


def afficher_emprunts(biblio: Bibliotheque) -> None:
    print("\n--- Liste des emprunts ---")
    emps = biblio.lister_emprunts()
    for e in emps:
        print(e)
    if not emps:
        print("(aucun emprunt)")
    print()
