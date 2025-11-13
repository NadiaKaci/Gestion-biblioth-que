from abc import ABC, abstractmethod

class Document(ABC):
    def __init__(self, nom, auteur):
        self.nom = nom
        self.auteur = auteur

    def __str__(self):
        return f"[Document: {self.nom} | Auteur: {self.auteur}]"