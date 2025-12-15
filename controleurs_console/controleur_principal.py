from classes.bibliotheque import Bibliotheque
from . import controleur_adherents as ca
from . import controleur_documents as cd
from . import controleur_emprunts as ce
from outils.validations import lire_choix_menu
from outils.gestion_csv import charger_bibliotheque, sauvegarder_bibliotheque
from outils.validations import lire_choix_menu


def afficher_menu() -> None:
    print("****************************************")
    print("* Bienvenue à votre bibliothèque       *")
    print("****************************************")
    print("* 1  Ajouter adhérent                  *")
    print("* 2  Supprimer adhérent                *")
    print("* 3  Afficher tous les adhérents       *")
    print("* 4  Ajouter document                  *")
    print("* 5  Supprimer document                *")
    print("* 6  Afficher tous les documents       *")
    print("* 7  Ajouter emprunt                   *")
    print("* 8  Retour d'un emprunt               *")
    print("* 9  Afficher tous les emprunts        *")
    print("* Q  Quitter                           *")
    print("****************************************")


def boucle_menu_principal() -> None:
    # 1) On crée l'objet Bibliotheque
    biblio = Bibliotheque()

    # 2) On charge les données depuis les fichiers CSV au démarrage
    charger_bibliotheque(biblio)

    # 3) Boucle principale du menu
    try:
        while True:
            afficher_menu()
            choix = lire_choix_menu({"1", "2", "3", "4", "5", "6", "7", "8", "9", "Q"})

            if choix == "1":
                ca.ajouter_adherent(biblio)
            elif choix == "2":
                ca.supprimer_adherent(biblio)
            elif choix == "3":
                ca.afficher_adherents(biblio)
            elif choix == "4":
                cd.ajouter_document(biblio)
            elif choix == "5":
                cd.supprimer_document(biblio)
            elif choix == "6":
                cd.afficher_documents(biblio)
            elif choix == "7":
                ce.ajouter_emprunt(biblio)
            elif choix == "8":
                ce.retour_emprunt(biblio)
            elif choix == "9":
                ce.afficher_emprunts(biblio)
            elif choix == "Q":
                print("Au revoir!")
                break
    finally:
        # 4) Quand on quitte le programme (même en cas d'erreur),
        # on sauvegarde TOUT dans les fichiers CSV
        sauvegarder_bibliotheque(biblio)
