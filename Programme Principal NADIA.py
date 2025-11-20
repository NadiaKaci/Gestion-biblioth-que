#classe Document:
from abc import ABC, abstractmethod

class Document(ABC):
    def __init__(self, nom, auteur):
        self.nom = nom
        self.auteur = auteur

    def __str__(self):
        return f"[Document: {self.nom} | Auteur: {self.auteur}]"

#classe adherent:
class Adherent:
    def __init__(self, id, nom, prenom):
        self.id = id
        self.nom = nom
        self.prenom = prenom

    def __str__(self):
        return f"[Adhérent {self.id}: {self.nom} {self.prenom}]"

#gestion Adherents:

#Gestion d'adherents:

import csv
from adherent import Adherent

class GestionAdherents:

    def __init__(self, fichier_csv="adherents.csv"):
        self.fichier_csv = fichier_csv
        self.adherents = []
        self.chargerAdherents()

    def ajouterAdherent(self, adherent):
        self.adherents.append(adherent)
        self.sauvegarderAdherents()

    def enleverAdherent(self, id_adherent):
        for adherent in self.adherents:
            if adherent.id == id_adherent:
                self.adherents.remove(adherent)
                break  # on arrête la boucle après avoir trouvé
        self.sauvegarderAdherents()

    def chargerAdherents(self):
        try:
            with open(self.fichier_csv, newline='', encoding='utf-8') as f:
                lecteur = csv.DictReader(f)
                for ligne in lecteur:
                    a = Adherent(ligne["id"], ligne["nom"], ligne["prenom"])
                    self.adherents.append(a)
        except FileNotFoundError:
            pass

    def sauvegarderAdherents(self):
        with open(self.fichier_csv, "w", newline='', encoding='utf-8') as f:
            champs = ["id", "nom", "prenom"]
            writer = csv.DictWriter(f, fieldnames=champs)
            writer.writeheader()
            for a in self.adherents:
                writer.writerow({
                    "id": a.id,
                    "nom": a.nom,
                    "prenom": a.prenom
                })
