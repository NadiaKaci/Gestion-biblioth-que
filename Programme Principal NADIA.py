# ---------------------------------
# Imports nécessaires
# ---------------------------------
from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
import csv
import os  # <- ajoute ceci si ce n'est pas déjà fait

print("Le fichier sera créé dans :", os.getcwd())
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
# Classes Documents
# ---------------------------------
class Document:
    def __init__(self, id_doc, titre, auteur=""):
        self.id = id_doc
        self.titre = titre
        self.auteur = auteur

    def to_csv_row(self):
        return [self.id, self.__class__.__name__, self.titre, self.auteur]

    @staticmethod
    def from_csv_row(row):
        id_doc = row[0]
        type_doc = row[1]
        titre = row[2]
        rest = row[3:] if len(row) > 3 else []

        if type_doc == "Livre":
            auteur = rest[0] if len(rest) > 0 else ""
            dispo = rest[1] == 'True' if len(rest) > 1 else True
            return Livre(id_doc, titre, auteur, dispo)

        elif type_doc == "BandeDessinee":
            auteur = rest[0] if len(rest) > 0 else ""
            dessinateur = rest[1] if len(rest) > 1 else ""
            return BandeDessinee(id_doc, titre, auteur, dessinateur)

        elif type_doc == "Dictionnaire":
            auteur = rest[0] if len(rest) > 0 else ""
            return Dictionnaire(id_doc, titre, auteur)

        elif type_doc == "Journal":
            auteur = rest[0] if len(rest) > 1 else ""
            try:
                date_parution = datetime.strptime(rest[-1], "%Y-%m-%d").date()
            except:
                date_parution = date.today()
            return Journal(id_doc, titre, auteur, date_parution)

        return Document(id_doc, titre, "")

class Livre(Document):
    def __init__(self, id_doc, titre, auteur="", est_disponible=True):
        super().__init__(id_doc, titre, auteur)
        self.est_disponible = est_disponible

    def to_csv_row(self):
        return [self.id, "Livre", self.titre, self.auteur, str(self.est_disponible)]

    def __str__(self):
        dispo = "Oui" if self.est_disponible else "Non"
        return f"[Livre] {self.titre} | Auteur : {self.auteur} | Disponible : {dispo}"

class BandeDessinee(Document):
    def __init__(self, id_doc, titre, auteur, dessinateur):
        super().__init__(id_doc, titre, auteur)
        self.dessinateur = dessinateur

    def to_csv_row(self):
        return [self.id, "BandeDessinee", self.titre, self.auteur, self.dessinateur]

    def __str__(self):
        return f"[BD] {self.titre} | Auteur : {self.auteur} | Dessinateur : {self.dessinateur}"

class Dictionnaire(Document):
    def __init__(self, id_doc, titre, auteur):
        super().__init__(id_doc, titre, auteur)

    def to_csv_row(self):
        return [self.id, "Dictionnaire", self.titre, self.auteur]

    def __str__(self):
        return f"[Dictionnaire] {self.titre} | Auteur : {self.auteur}"

class Journal(Document):
    def __init__(self, id_doc, titre, auteur, date_parution):
        super().__init__(id_doc, titre, auteur)
        self.date_parution = date_parution

    def to_csv_row(self):
        return [self.id, "Journal", self.titre, self.auteur, self.date_parution.isoformat()]

    def __str__(self):
        return f"[Journal] {self.titre} | Auteur : {self.auteur} | Parution : {self.date_parution}"

# ---------------------------------
# Classe Adherent
# ---------------------------------
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
        return Adherent(row[0], row[1], row[2], row[3] if len(row) > 3 else "")

    def __str__(self):
        email_str = f" | Email: {self.email}" if self.email else ""
        return f"{self.nom} {self.prenom}{email_str} (ID : {self.id})"

# ---------------------------------
# Classe Emprunt
# ---------------------------------
class Emprunt:
    def __init__(self, id_emprunt, id_adherent, id_livre, date_emprunt, date_retour):
        self.id = id_emprunt
        self.id_adherent = id_adherent
        self.id_livre = id_livre
        self.date_emprunt = date_emprunt
        self.date_retour = date_retour

    def to_csv_row(self):
        return [
            self.id,
            self.id_adherent,
            self.id_livre,
            self.date_emprunt.isoformat(),
            self.date_retour.isoformat(),
        ]

    @staticmethod
    def from_csv_row(row):
        d1 = datetime.strptime(row[3], "%Y-%m-%d").date()
        d2 = datetime.strptime(row[4], "%Y-%m-%d").date()
        return Emprunt(row[0], row[1], row[2], d1, d2)

    def __str__(self):
        return f"Emprunt ID {self.id} | Adhérent {self.id_adherent} | Livre {self.id_livre} | Emprunt : {self.date_emprunt} | Retour : {self.date_retour}"

# ---------------------------------
# Classe Bibliotheque
# ---------------------------------
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
                self.adherents = [Adherent.from_csv_row(row) for row in csv.reader(f)]
        except:
            self.adherents = []

        try:
            with open("documents.csv", newline='', encoding="utf-8") as f:
                self.documents = [Document.from_csv_row(row) for row in csv.reader(f)]
        except:
            self.documents = []

        try:
            with open("emprunts.csv", newline='', encoding="utf-8") as f:
                self.emprunts = [Emprunt.from_csv_row(row) for row in csv.reader(f)]
        except:
            self.emprunts = []

    def sauvegarder_csv(self):
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

    # --- Adhérents ---
    def ajouter_adherent(self, nom, prenom, email=""):
        id_ad = self.nouvelle_id(self.adherents)
        self.adherents.append(Adherent(id_ad, nom, prenom, email))
        print("Adhérent ajouté.")

    def supprimer_adherent(self, id_ad):
        before = len(self.adherents)
        self.adherents = [a for a in self.adherents if a.id != id_ad]
        print("Adhérent supprimé." if len(self.adherents) != before else "ID introuvable.")

    def afficher_adherents(self):
        if not self.adherents:
            print("Aucun adhérent.")
        else:
            for idx, a in enumerate(self.adherents, 1):
                print(f"{idx}. {a}")

    # --- Documents ---
    def ajouter_document(self, doc):
        self.documents.append(doc)
        print("Document ajouté.")

    def supprimer_document(self, id_doc):
        before = len(self.documents)
        self.documents = [d for d in self.documents if d.id != id_doc]
        print("Document supprimé." if len(self.documents) != before else "ID introuvable.")

    def afficher_documents(self):
        if not self.documents:
            print("Aucun document.")
        else:
            for idx, d in enumerate(self.documents, 1):
                print(f"{idx}. {d}")

    # --- Emprunts ---
    def ajouter_emprunt(self, id_ad, id_livre):
        adherent = next((a for a in self.adherents if a.id == id_ad), None)
        if not adherent:
            print("Adhérent introuvable.")
            return

        livre = next((l for l in self.documents if l.id == id_livre and isinstance(l, Livre)), None)
        if not livre:
            print("Livre introuvable.")
            return

        if not livre.est_disponible:
            print("Livre non disponible.")
            return

        date_emprunt = date.today()
        date_retour = date_emprunt + timedelta(days=15)
        id_e = self.nouvelle_id(self.emprunts)

        self.emprunts.append(Emprunt(id_e, id_ad, id_livre, date_emprunt, date_retour))
        livre.est_disponible = False
        print("Emprunt ajouté.")

    def retour_emprunt(self, id_e):
        emprunt = next((e for e in self.emprunts if e.id == id_e), None)
        if not emprunt:
            print("Emprunt introuvable.")
            return

        livre = next((l for l in self.documents if l.id == emprunt.id_livre), None)
        if livre:
            livre.est_disponible = True

        self.emprunts = [e for e in self.emprunts if e.id != id_e]
        print("Livre retourné.")

    def afficher_emprunts(self):
        if not self.emprunts:
            print("Aucun emprunt.")
        else:
            for idx, e in enumerate(self.emprunts, 1):
                print(f"{idx}. {e}")

# ---------------------------------
# Menu Principal
# ---------------------------------
class MenuPrincipal:
    def __init__(self, bibliotheque):
        self.biblio = bibliotheque

    def afficher(self):
        while True:
            print("\n" + "*"*40)
            print("        MENU PRINCIPAL")
            print("*"*40)
            print("1. Gérer les adhérents")
            print("2. Gérer les documents")
            print("3. Gérer les emprunts")
            print("4. Sauvegarder")
            print("5. Quitter")
            print("*"*40)

            choix = saisie_str("Votre choix : ")

            if choix == "1":
                self.menu_adherents()
            elif choix == "2":
                self.menu_documents()
            elif choix == "3":
                self.menu_emprunts()
            elif choix == "4":
                self.biblio.sauvegarder_csv()
                print("Sauvegarde effectuée.")
            elif choix == "5":
                print("Au revoir !")
                break
            else:
                print("Choix invalide.")

    def menu_adherents(self):
        print("\n--- Gestion des adhérents ---")
        print("1. Ajouter")
        print("2. Afficher")
        print("3. Supprimer")
        choix = saisie_str("Choix : ")

        if choix == "1":
            nom = saisie_str("Nom : ")
            prenom = saisie_str("Prénom : ")
            email = saisie_str("Email (optionnel) : ", facultatif=True)
            self.biblio.ajouter_adherent(nom, prenom, email)

        elif choix == "2":
            self.biblio.afficher_adherents()

        elif choix == "3":
            id_ad = saisie_str("ID adhérent : ")
            self.biblio.supprimer_adherent(id_ad)

    def menu_documents(self):
        print("\n--- Gestion des documents ---")
        print("1. Ajouter")
        print("2. Afficher")
        print("3. Supprimer")
        choix = saisie_str("Choix : ")

        if choix == "1":
            print("Types : 1-Livre | 2-BD | 3-Dictionnaire | 4-Journal")
            type_doc = saisie_str("Type : ")

            titre = saisie_str("Titre : ")
            auteur = saisie_str("Auteur : ", facultatif=True)
            id_doc = self.biblio.nouvelle_id(self.biblio.documents)

            if type_doc == "1":
                self.biblio.ajouter_document(Livre(id_doc, titre, auteur))
            elif type_doc == "2":
                dess = saisie_str("Dessinateur : ")
                self.biblio.ajouter_document(BandeDessinee(id_doc, titre, auteur, dess))
            elif type_doc == "3":
                self.biblio.ajouter_document(Dictionnaire(id_doc, titre, auteur))
            elif type_doc == "4":
                d = date.today()
                self.biblio.ajouter_document(Journal(id_doc, titre, auteur, d))

        elif choix == "2":
            self.biblio.afficher_documents()

        elif choix == "3":
            id_doc = saisie_str("ID document : ")
            self.biblio.supprimer_document(id_doc)

    def menu_emprunts(self):
        print("\n--- Gestion des emprunts ---")
        print("1. Ajouter un emprunt")
        print("2. Afficher les emprunts")
        print("3. Retourner un emprunt")
        choix = saisie_str("Choix : ")

        if choix == "1":
            id_ad = saisie_str("ID adhérent : ")
            id_l = saisie_str("ID livre : ")
            self.biblio.ajouter_emprunt(id_ad, id_l)

        elif choix == "2":
            self.biblio.afficher_emprunts()

        elif choix == "3":
            id_e = saisie_str("ID emprunt : ")
            self.biblio.retour_emprunt(id_e)

# ---------------------------------
# Programme principal
# ---------------------------------
if __name__ == "__main__":
    b = Bibliotheque()
    b.charger_csv()
    menu = MenuPrincipal(b)
    menu.afficher()
# fin