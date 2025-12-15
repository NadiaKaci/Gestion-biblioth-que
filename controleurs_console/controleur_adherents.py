from classes.adherent import Adherent
from classes.bibliotheque import Bibliotheque


def ajouter_adherent(biblio: Bibliotheque) -> None:
    print("\n--- Ajouter un adhérent ---")
    nom = input("Nom : ").strip()
    prenom = input("Prénom : ").strip()
    email = input("Courriel (optionnel) : ").strip() or None
    adherent = Adherent(nom, prenom, email)
    biblio.ajouter_adherent(adherent)
    print("Adhérent ajouté.\n")


def supprimer_adherent(biblio: Bibliotheque) -> None:
    print("\n--- Supprimer un adhérent ---")
    nom = input("Nom : ").strip()
    prenom = input("Prénom : ").strip()
    if biblio.supprimer_adherent(nom, prenom):
        print("Adhérent supprimé.\n")
    else:
        print("Adhérent introuvable.\n")


def afficher_adherents(biblio: Bibliotheque) -> None:
    print("\n--- Liste des adhérents ---")
    for a in biblio.lister_adherents():
        print(a)
    if not biblio.lister_adherents():
        print("(aucun adhérent)")
    print()