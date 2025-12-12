class Adherent:
    """Adhérent de la bibliothèque."""

    def __init__(self, nom: str, prenom: str, email: str | None = None) -> None:
        self.nom = nom
        self.prenom = prenom
        self.email = email

    def __str__(self) -> str:
        return f"{self.prenom} {self.nom}"
