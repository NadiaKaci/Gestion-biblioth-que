class Adherent:
    def __init__(self, id, nom, prenom):
        self.id = id
        self.nom = nom
        self.prenom = prenom

    def __str__(self):
        return f"[Adhérent {self.id}: {self.nom} {self.prenom}]"