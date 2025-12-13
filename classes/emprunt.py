from datetime import date
from .adherent import Adherent
from .livre import Livre


class Emprunt:
    """Transaction d'emprunt d'un livre par un adhérent."""

    def __init__(
        self,
        adherent: Adherent,
        livre: Livre,
        date_emprunt: date,
        date_retour: date | None = None,
    ) -> None:
        self.adherent = adherent
        self.livre = livre
        self.date_emprunt = date_emprunt
        self.date_retour = date_retour

    def marquer_retour(self, date_retour: date) -> None:
        self.date_retour = date_retour

    def __str__(self) -> str:
        retour = self.date_retour.isoformat() if self.date_retour else "en cours"
        return (
            f"{self.adherent} ; {self.livre.titre} ; "
            f"{self.date_emprunt.isoformat()} ; {retour}"
        )
