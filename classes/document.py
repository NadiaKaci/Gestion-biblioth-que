class Document:
    """Classe de base pour tous les documents de la bibliothèque."""

    def __init__(self, titre: str) -> None:
        self.titre = titre

    def __str__(self) -> str:
        return self.titre
