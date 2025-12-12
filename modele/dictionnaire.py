from .volume import Volume


class Dictionnaire(Volume):
    """Dictionnaire spécialisé de Volume."""

    def __str__(self) -> str:
        return f"Dictionnaire : {self.titre} ({self.auteur})"
