class Adherent:
    def __init__(self, nom: str, prenom: str, email: str | None = None) -> None:
        self.nom = nom
        self.prenom = prenom
        self.email = email

    def __str__(self) -> str:
        # Doit être EXACTEMENT comme la version console
        return f"{self.nom} {self.prenom}"

