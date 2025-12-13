from .document import Document


class Volume(Document):
    """Volume : document avec un auteur."""

    def __init__(self, titre: str, auteur: str) -> None:
        super().__init__(titre)
        self.auteur = auteur

    def __str__(self) -> str:
        return f"{self.titre} ({self.auteur})"
