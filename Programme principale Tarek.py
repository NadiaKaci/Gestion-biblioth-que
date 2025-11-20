# Livres (ISBN, annee)
class Livre(Document):
    def __init__(self, nom, auteur, ISBN, annee):
        super().__init__(nom, auteur)
        self.ISBN = ISBN
        self.annee = annee