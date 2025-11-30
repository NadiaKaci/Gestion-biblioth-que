# ---------------------------------
# Import nécessaire
# ---------------------------------
from abc import ABC, abstractmethod
from datetime import datetime
import csv

# ---------------------------------
# Fonctions utilitaires
# ---------------------------------
def saisie_str(prompt, facultatif=False):
    while True:
        valeur = input(prompt).strip()
        if valeur or facultatif:
            return valeur
        print("Erreur : la saisie ne peut pas être vide.")

def saisie_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Erreur : saisie invalide.")

def saisie_date_iso(prompt):
    while True:
        try:
            s = input(prompt).strip()
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            print("Erreur : format de date invalide (YYYY-MM-DD).")

# ---------------------------------
# Classes
# ---------------------------------
# Classe Document (abstraite)
class Document(ABC):
    def __init__(self, nom, auteur):
        self.nom = nom
        self.auteur = auteur

    def __str__(self):
        return f"[Document: {self.nom} | Auteur: {self.auteur}]"

# Classe Adherent
class Adherent:
    def __init__(self, id_adherent, nom, prenom, email=""):
        self.id = id_adherent
        self.nom = nom
        self.prenom = prenom
        self.email = email

    def to_csv_row(self):
        return [self.id, self.nom, self.prenom, self.email]

    @staticmethod
    def from_csv_row(row):
        id_ad = row[0] if len(row) > 0 else ""
        nom = row[1] if len(row) > 1 else ""
        prenom = row[2] if len(row) > 2 else ""
        email = row[3] if len(row) > 3 else ""
        return Adherent(id_ad, nom, prenom, email)

    def __str__(self):
        email_str = f" | Email: {self.email}" if self.email else ""
        return f"{self.nom} {self.prenom}{email_str} (ID : {self.id})"

# -----------------------------
# Classe Emprunt
# -----------------------------
class Emprunt:
    def __init__(self, id_emprunt, id_adherent, id_livre, date_emprunt, date_retour):
        self.id = id_emprunt
        self.id_adherent = id_adherent
        self.id_livre = id_livre
        self.date_emprunt = date_emprunt
        self.date_retour = date_retour

    def to_csv_row(self):
        return [self.id, self.id_adherent, self.id_livre, self.date_emprunt.isoformat(), self.date_retour.isoformat()]

    @staticmethod
    def from_csv_row(row):
        id_e = row[0] if len(row) > 0 else ""
        id_a = row[1] if len(row) > 1 else ""
        id_l = row[2] if len(row) > 2 else ""
        try:
            d_emprunt = datetime.strptime(row[3], "%Y-%m-%d").date() if len(row) > 3 else date.today()
        except ValueError:
            d_emprunt = date.today()
        try:
            d_retour = datetime.strptime(row[4], "%Y-%m-%d").date() if len(row) > 4 else date.today()
        except ValueError:
            d_retour = date.today()
        return Emprunt(id_e, id_a, id_l, d_emprunt, d_retour)

    def __str__(self):
        return f"Emprunt ID {self.id} | Adhérent {self.id_adherent} | Livre {self.id_livre} | Emprunt : {self.date_emprunt} | Retour : {self.date_retour}"


