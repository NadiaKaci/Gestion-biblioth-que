#classe Document:
from abc import ABC, abstractmethod

class Document(ABC):
    def __init__(self, nom, auteur):
        self.nom = nom
        self.auteur = auteur

    def __str__(self):
        return f"[Document: {self.nom} | Auteur: {self.auteur}]"

#classe adherant:
class Adherent:
    def __init__(self, id, nom, prenom):
        self.id = id
        self.nom = nom
        self.prenom = prenom

    def __str__(self):
        return f"[Adhérent {self.id}: {self.nom} {self.prenom}]"

