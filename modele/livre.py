from .volume import Volume


class Livre(Volume):
    """Livre empruntable, avec disponibilité."""

    def __init__(self, titre: str, auteur: str, est_dispo: bool = True) -> None:
        super().__init__(titre, auteur)
        self.est_dispo = est_dispo

    def est_disponible(self) -> bool:
        return self.est_dispo

    def __str__(self) -> str:
        etat = "disponible" if self.est_dispo else "non disponible"
        return f"Livre : {self.titre} ({self.auteur}) - {etat}"
