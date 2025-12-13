import csv
from pathlib import Path
from datetime import date

from classes.adherent import Adherent
from classes.document import Document
from classes.livre import Livre
from classes.bande_dessinee import BandeDessinee
from classes.dictionnaire import Dictionnaire
from classes.journal import Journal
from classes.emprunt import Emprunt
from classes.bibliotheque import Bibliotheque


DOSSIER_FICHIERS = Path("fichiers")
chemin = DOSSIER_FICHIERS / "adherents.csv"
chemin = DOSSIER_FICHIERS / "documents.csv"
chemin = DOSSIER_FICHIERS / "emprunts.csv"

def charger_bibliotheque(biblio: Bibliotheque) -> None:
    """Charge les adhérents, documents et emprunts depuis les CSV (si présents)."""
    _charger_adherents(biblio)
    _charger_documents(biblio)
    _charger_emprunts(biblio)


def sauvegarder_bibliotheque(biblio: Bibliotheque) -> None:
    """Sauvegarde les adhérents, documents et emprunts dans les CSV."""
    DOSSIER_FICHIERS.mkdir(exist_ok=True)
    _sauvegarder_adherents(biblio)
    _sauvegarder_documents(biblio)
    _sauvegarder_emprunts(biblio)


# ===== Adhérents =====

def _charger_adherents(biblio: Bibliotheque) -> None:
    chemin = DOSSIER_FICHIERS / "adherents.csv"
    if not chemin.exists():
        return
    with chemin.open(newline="", encoding="utf-8") as f:
        lecteur = csv.reader(f, delimiter=";")
        for nom, prenom, email in lecteur:
            email = email or None
            biblio.ajouter_adherent(Adherent(nom, prenom, email))


def _sauvegarder_adherents(biblio: Bibliotheque) -> None:
    chemin = DOSSIER_FICHIERS / "adherents.csv"
    with chemin.open("w", newline="", encoding="utf-8") as f:
        ecrivain = csv.writer(f, delimiter=";")
        for a in biblio.lister_adherents():
            ecrivain.writerow([a.nom, a.prenom, a.email or ""])


# ===== Documents =====

def _charger_documents(biblio: Bibliotheque) -> None:
    chemin = DOSSIER_FICHIERS / "documents.csv"
    if not chemin.exists():
        return
    with chemin.open(newline="", encoding="utf-8") as f:
        lecteur = csv.reader(f, delimiter=";")
        for ligne in lecteur:
            if not ligne:
                continue
            type_doc = ligne[0]
            if type_doc == "LIVRE":
                _, titre, auteur, est_dispo = ligne
                doc = Livre(titre, auteur, est_dispo == "1")
            elif type_doc == "BD":
                _, titre, auteur, dessinateur = ligne
                doc = BandeDessinee(titre, auteur, dessinateur)
            elif type_doc == "DICT":
                _, titre, auteur = ligne
                doc = Dictionnaire(titre, auteur)
            elif type_doc == "JOURNAL":
                _, titre, s_date = ligne
                an, m, j = map(int, s_date.split("-"))
                doc = Journal(titre, date(an, m, j))
            else:
                # type inconnu : on peut créer un Document simple
                _, titre = ligne[0], ligne[1]
                doc = Document(titre)
            biblio.ajouter_document(doc)


def _sauvegarder_documents(biblio: Bibliotheque) -> None:
    chemin = DOSSIER_FICHIERS / "documents.csv"
    with chemin.open("w", newline="", encoding="utf-8") as f:
        ecrivain = csv.writer(f, delimiter=";")
        for d in biblio.lister_documents():
            if isinstance(d, Livre):
                ecrivain.writerow(
                    ["LIVRE", d.titre, d.auteur, "1" if d.est_dispo else "0"]
                )
            elif isinstance(d, BandeDessinee):
                ecrivain.writerow(["BD", d.titre, d.auteur, d.dessinateur])
            elif isinstance(d, Dictionnaire):
                ecrivain.writerow(["DICT", d.titre, d.auteur])
            elif isinstance(d, Journal):
                ecrivain.writerow(["JOURNAL", d.titre, d.date_paru.isoformat()])
            else:
                ecrivain.writerow(["DOC", d.titre])


# ===== Emprunts =====

def _charger_emprunts(biblio: Bibliotheque) -> None:
    chemin = DOSSIER_FICHIERS / "emprunts.csv"
    if not chemin.exists():
        return
    with chemin.open(newline="", encoding="utf-8") as f:
        lecteur = csv.reader(f, delimiter=";")
        for nom, prenom, titre, s_de, s_dr in lecteur:
            adherent = next(
                (a for a in biblio.adherents if a.nom == nom and a.prenom == prenom),
                None,
            )
            livre = next(
                (d for d in biblio.documents if isinstance(d, Livre) and d.titre == titre),
                None,
            )
            if adherent is None or livre is None:
                continue
            an, m, j = map(int, s_de.split("-"))
            date_emprunt = date(an, m, j)
            date_retour = None
            if s_dr:
                an2, m2, j2 = map(int, s_dr.split("-"))
                date_retour = date(an2, m2, j2)
            emprunt = Emprunt(adherent, livre, date_emprunt, date_retour)
            biblio.emprunts.append(emprunt)
            if date_retour is None:
                livre.est_dispo = False


def _sauvegarder_emprunts(biblio: Bibliotheque) -> None:
    chemin = DOSSIER_FICHIERS / "emprunts.csv"
    with chemin.open("w", newline="", encoding="utf-8") as f:
        ecrivain = csv.writer(f, delimiter=";")
        for e in biblio.lister_emprunts():
            s_de = e.date_emprunt.isoformat()
            s_dr = e.date_retour.isoformat() if e.date_retour else ""
            ecrivain.writerow(
                [e.adherent.nom, e.adherent.prenom, e.livre.titre, s_de, s_dr]
            )
