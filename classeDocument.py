from abc import ABC, abstractmethod

class Document(ABC):
    def __init__(self, nom, auteur):
        self.nom = nom
        self.auteur = auteur

    def __str__(self):
Br-nadia1
        return f"[Document: {self.nom} | Auteur: {self.auteur}]"
=======
        return f"[Document  {self.nom}   {self.auteur}]"
# to confirm

#/3éééé
main
