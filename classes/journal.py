from datetime import date
from .document import Document


class Journal(Document):
    """Journal avec date de parution."""

    def __init__(self, titre: str, date_paru: date) -> None:
        super().__init__(titre)
        self.date_paru = date_paru

    def __str__(self) -> str:
        return f"Journal : {self.titre} - Paru le {self.date_paru.isoformat()}"
