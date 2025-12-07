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
class Document:
    def __init__(self, id_doc, titre, auteur=""):
        self.id = id_doc
        self.titre = titre
        self.auteur = auteur  # ajouté ici

    def to_csv_row(self):
        return [self.id, self.__class__.__name__, self.titre, self.auteur]

    @staticmethod
    def from_csv_row(row):
        if len(row) < 3:
            raise ValueError(f"CSV Document invalide : {row}")
        id_doc = row[0]
        type_doc = row[1]
        titre = row[2]
        rest = row[3:] if len(row) > 3 else []

        if type_doc == "Livre":
            dispo = rest[1] == 'True' if len(rest) > 1 else True
            auteur = rest[0] if len(rest) > 0 else ""
            return Livre(id_doc, titre, auteur, dispo)
        elif type_doc == "BandeDessinee":
            auteur = rest[0] if len(rest) > 0 else ""
            dessinateur = rest[1] if len(rest) > 1 else ""
            return BandeDessinee(id_doc, titre, auteur, dessinateur)
        elif type_doc == "Dictionnaire":
            auteur = rest[0] if len(rest) > 0 else ""
            return Dictionnaire(id_doc, titre, auteur)
        elif type_doc == "Journal":
            auteur = rest[1] if len(rest) > 1 else ""
            if len(rest) > 0:
                try:
                    date_parution = datetime.strptime(rest[0], "%Y-%m-%d").date()
                except ValueError:
                    date_parution = date.today()
            else:
                date_parution = date.today()
            return Journal(id_doc, titre, auteur, date_parution)
        else:
            auteur = rest[0] if len(rest) > 0 else ""
            return Document(id_doc, titre, auteur)

class Livre(Document):
    def __init__(self, id_doc, titre, est_disponible=True, auteur=""):
        super().__init__(id_doc, titre, auteur)
        self.est_disponible = est_disponible

    def to_csv_row(self):
        return [self.id, "Livre", self.titre, self.auteur, str(self.est_disponible)]

    def __str__(self):
        dispo = "Oui" if self.est_disponible else "Non"
        auteur_str = f" | Auteur : {self.auteur}" if self.auteur else ""
        return f"[Livre] {self.titre}{auteur_str} | Disponible : {dispo}"

class BandeDessinee(Document):
    def __init__(self, id_doc, titre, dessinateur):
        super().__init__(id_doc, titre)
        self.dessinateur = dessinateur

    def to_csv_row(self):
        return [self.id, "BandeDessinee", self.titre, self.dessinateur]

    def __str__(self):
        return f"[BD] {self.titre} | Dessinateur : {self.dessinateur}"

class Dictionnaire(Document):
    def __init__(self, id_doc, titre, auteur):
        super().__init__(id_doc, titre, auteur)

    def to_csv_row(self):
        return [self.id, "Dictionnaire", self.titre, self.auteur]

    def __str__(self):
        return f"[Dictionnaire] {self.titre} | Auteur : {self.auteur}"

class Journal(Document):
    def __init__(self, id_doc, titre, date_parution):
        super().__init__(id_doc, titre)
        self.date_parution = date_parution

    def to_csv_row(self):
        return [self.id, "Journal", self.titre, self.date_parution.isoformat()]

    def __str__(self):
        return f"[Journal] {self.titre} | Parution : {self.date_parution}"

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
# -----------------------------
# Classe Bibliotheque
# -----------------------------
class Bibliotheque:
    def __init__(self):
        self.adherents = []
        self.documents = []
        self.emprunts = []

    def nouvelle_id(self, collection):
        if collection:
            return str(int(max([obj.id for obj in collection], key=int)) + 1)
        return "1"

    def charger_csv(self):
        try:
            with open("adherents.csv", newline='', encoding="utf-8") as f:
                reader = csv.reader(f)
                self.adherents = [Adherent.from_csv_row(row) for row in reader]
        except FileNotFoundError:
            self.adherents = []
            print("Fichier 'adherents.csv' non trouvé, création d’une nouvelle liste.")
        try:
            with open("documents.csv", newline='', encoding="utf-8") as f:
                reader = csv.reader(f)
                self.documents = [Document.from_csv_row(row) for row in reader]
        except FileNotFoundError:
            self.documents = []
            print("Fichier 'documents.csv' non trouvé, création d’une nouvelle liste.")
        try:
            with open("emprunts.csv", newline='', encoding="utf-8") as f:
                reader = csv.reader(f)
                self.emprunts = [Emprunt.from_csv_row(row) for row in reader]
        except FileNotFoundError:
            self.emprunts = []
            print("Fichier 'emprunts.csv' non trouvé, création d’une nouvelle liste.")

    def sauvegarder_csv(self):
        try:
            with open("adherents.csv", "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                for a in self.adherents:
                    writer.writerow(a.to_csv_row())
            with open("documents.csv", "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                for d in self.documents:
                    writer.writerow(d.to_csv_row())
            with open("emprunts.csv", "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                for e in self.emprunts:
                    writer.writerow(e.to_csv_row())
        except Exception as e:
            print(f"Erreur lors de la sauvegarde CSV : {e}")
 # Gestion Adherents
    def ajouter_adherent(self, nom, prenom, email=""):
        id_ad = self.nouvelle_id(self.adherents)
        self.adherents.append(Adherent(id_ad, nom, prenom, email))
        print("Adhérent ajouté.")

    def supprimer_adherent(self, id_ad):
        before = len(self.adherents)
        self.adherents = [a for a in self.adherents if a.id != id_ad]
        after = len(self.adherents)
        print(f"Adhérent supprimé." if before != after else "Aucun adhérent trouvé avec cet ID.")

    def afficher_adherents(self):
        if not self.adherents:
            print("Aucun adhérent.")
        for idx, a in enumerate(self.adherents, 1):
            print(f"{idx}. {a}")


