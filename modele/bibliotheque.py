from __future__ import annotations

from typing import List, Optional

from .document import Document
from .livre import Livre
from .adherent import Adherent
from .emprunt import Emprunt


class Bibliotheque:
    """Gère les documents, adhérents et emprunts."""

    def __init__(self) -> None:
        self.documents: List[Document] = []
        self.adherents: List[Adherent] = []
        self.emprunts: List[Emprunt] = []

    # --- gestion des adhérents ---

    def ajouter_adherent(self, adherent: Adherent) -> None:
        self.adherents.append(adherent)

    def supprimer_adherent(self, nom: str, prenom: str) -> bool:
        for a in self.adherents:
            if a.nom == nom and a.prenom == prenom:
                self.adherents.remove(a)
                return True
        return False

    def lister_adherents(self) -> List[Adherent]:
        return list(self.adherents)

    # --- gestion des documents ---

    def ajouter_document(self, doc: Document) -> None:
        self.documents.append(doc)

    def supprimer_document(self, titre: str) -> bool:
        for d in self.documents:
            if d.titre == titre:
                self.documents.remove(d)
                return True
        return False

    def lister_documents(self) -> List[Document]:
        return list(self.documents)

    def trouver_livre_disponible(self, titre: str) -> Optional[Livre]:
        for d in self.documents:
            if isinstance(d, Livre) and d.titre == titre and d.est_disponible():
                return d
        return None

    # --- gestion des emprunts ---

    def emprunter_livre(
        self, adherent: Adherent, titre_livre: str, date_emprunt
    ) -> bool:
        livre = self.trouver_livre_disponible(titre_livre)
        if livre is None:
            return False

        livre.est_dispo = False
        emprunt = Emprunt(adherent, livre, date_emprunt)
        self.emprunts.append(emprunt)
        return True

    def retourner_livre(
        self, adherent: Adherent, titre_livre: str, date_retour
    ) -> bool:
        for e in self.emprunts:
            if (
                e.adherent is adherent
                and e.livre.titre == titre_livre
                and e.date_retour is None
            ):
                e.marquer_retour(date_retour)
                e.livre.est_dispo = True
                return True
        return False

    def lister_emprunts(self) -> List[Emprunt]:
        return list(self.emprunts)
