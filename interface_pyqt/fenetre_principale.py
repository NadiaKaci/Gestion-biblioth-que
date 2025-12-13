import sys
from datetime import date

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QListWidget,
    QMessageBox,
    QDialog,
    QComboBox,
)
from PyQt6.QtCore import Qt

from classes.bibliotheque import Bibliotheque
from classes.adherent import Adherent
from classes.document import Document
from outils.gestion_csv import charger_bibliotheque, sauvegarder_bibliotheque
from classes.livre import Livre


# ================== Fenêtre adhérents ==================
class FenetreAdherents(QDialog):
    """Fenêtre pour gérer les adhérents."""

    def __init__(self, biblio: Bibliotheque) -> None:
        super().__init__()
        self.biblio = biblio
        self.setWindowTitle("Gestion des adhérents")
        self.resize(500, 400)
        self._configurer_ui()
        # Remplir les champs quand on change la sélection (facultatif)
        self.liste_adherents.itemSelectionChanged.connect(
            self._remplir_champs_depuis_selection
        )

    def _configurer_ui(self) -> None:
        layout = QVBoxLayout()

        self.liste_adherents = QListWidget()
        layout.addWidget(QLabel("Liste des adhérents :"))
        layout.addWidget(self.liste_adherents)

        form_adh = QHBoxLayout()
        self.input_prenom = QLineEdit()
        self.input_nom = QLineEdit()
        self.input_email = QLineEdit()
        self.input_prenom.setPlaceholderText("Prénom")
        self.input_nom.setPlaceholderText("Nom")
        self.input_email.setPlaceholderText("Email (optionnel)")
        form_adh.addWidget(self.input_prenom)
        form_adh.addWidget(self.input_nom)
        form_adh.addWidget(self.input_email)

        btn_ajout = QPushButton("Ajouter adhérent")
        btn_supprimer = QPushButton("Supprimer adhérent")
        btn_afficher = QPushButton("Recharger la liste")

        btn_ajout.clicked.connect(self.ajouter_adherent)
        btn_supprimer.clicked.connect(self.supprimer_adherent)
        btn_afficher.clicked.connect(self.rafraichir_liste)

        layout.addLayout(form_adh)
        layout.addWidget(btn_ajout)
        layout.addWidget(btn_supprimer)
        layout.addWidget(btn_afficher)

        self.setLayout(layout)

    def rafraichir_liste(self) -> None:
        """Recharge la liste à partir de la biblio."""
        self.liste_adherents.clear()
        for a in self.biblio.adherents:
            self.liste_adherents.addItem(str(a))

    def ajouter_adherent(self) -> None:
        prenom = self.input_prenom.text().strip()
        nom = self.input_nom.text().strip()
        email = self.input_email.text().strip() or None
        if not prenom or not nom:
            QMessageBox.warning(self, "Erreur", "Prénom et nom sont obligatoires.")
            return
        adh = Adherent(nom, prenom, email)
        self.biblio.ajouter_adherent(adh)
        QMessageBox.information(self, "Succès", "Adhérent ajouté.")
        self.input_prenom.clear()
        self.input_nom.clear()
        self.input_email.clear()
        # On ne recharge pas automatiquement : la liste se met à jour
        # seulement si l'utilisateur clique sur "Recharger la liste".

    def _remplir_champs_depuis_selection(self) -> None:
        """Remplit les QLineEdit à partir de l'élément sélectionné (optionnel)."""
        item = self.liste_adherents.currentItem()
        if item is None:
            return
        texte = item.text()
        # suppose que __str__ de Adherent renvoie "NOM Prenom"
        parts = texte.split()
        if len(parts) >= 2:
            nom = parts[0]
            prenom = " ".join(parts[1:])
            self.input_nom.setText(nom)
            self.input_prenom.setText(prenom)

    def supprimer_adherent(self) -> None:
        """Supprime l'adhérent sélectionné dans la liste."""
        item = self.liste_adherents.currentItem()
        if item is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionnez un adhérent dans la liste avant de supprimer."
            )
            return

        texte = item.text()          # ex : "Hamrouni Tarek"
        parts = texte.split()
        if len(parts) < 2:
            QMessageBox.warning(self, "Erreur", "Format d'adhérent inconnu.")
            return

        nom = parts[0]
        prenom = " ".join(parts[1:])

        if self.biblio.supprimer_adherent(nom, prenom):
            QMessageBox.information(self, "Succès", f"Adhérent '{texte}' supprimé.")
            self.rafraichir_liste()
        else:
            QMessageBox.warning(self, "Erreur", "Adhérent introuvable.")


# ================== Fenêtre documents ==================
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QLineEdit, QPushButton, QMessageBox, QComboBox
)

from classes.bibliotheque import Bibliotheque
from classes.document import Document
from classes.livre import Livre


class FenetreDocuments(QWidget):
    """Fenêtre pour gérer les documents (simple QWidget, ne se ferme pas toute seule)."""

    def __init__(self, biblio: Bibliotheque) -> None:
        super().__init__()
        self.biblio = biblio
        self.setWindowTitle("Gestion des documents")
        self.resize(500, 400)
        self._configurer_ui()

    def _configurer_ui(self) -> None:
        layout = QVBoxLayout()

        self.liste_documents = QListWidget()
        layout.addWidget(QLabel("Liste des documents :"))
        layout.addWidget(self.liste_documents)

        # Choix du type
        type_layout = QHBoxLayout()
        type_label = QLabel("Type :")
        self.combo_type = QComboBox()
        self.combo_type.addItems([
            "Livre",
            "Volume",
            "Dictionnaire",
            "Journal",
            "Bande dessinée ",
        ])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.combo_type)
        layout.addLayout(type_layout)

        # Titre + auteur
        form_doc = QHBoxLayout()
        self.input_titre = QLineEdit()
        self.input_auteur = QLineEdit()
        self.input_titre.setPlaceholderText("Titre")
        self.input_auteur.setPlaceholderText("Auteur")
        form_doc.addWidget(self.input_titre)
        form_doc.addWidget(self.input_auteur)

        btn_ajout = QPushButton("Ajouter document")
        btn_supprimer = QPushButton("Supprimer document")
        btn_afficher = QPushButton("Recharger la liste")

        btn_ajout.clicked.connect(self.ajouter_document)
        btn_supprimer.clicked.connect(self.supprimer_document)
        btn_afficher.clicked.connect(self.rafraichir_liste)

        layout.addLayout(form_doc)
        layout.addWidget(btn_ajout)
        layout.addWidget(btn_supprimer)
        layout.addWidget(btn_afficher)

        self.setLayout(layout)

    def rafraichir_liste(self) -> None:
        """Affiche les documents avec le type choisi entre crochets."""
        self.liste_documents.clear()
        for d in self.biblio.documents:
            # d.titre contient déjà le titre brut, on n'utilise plus __class__.__name__
            if hasattr(d, "auteur"):
                texte = f"{d.titre} ({d.auteur})"
            else:
                texte = d.titre
            self.liste_documents.addItem(texte)

    def ajouter_document(self) -> None:
        """Ajoute un document avec le type choisi et met à jour la liste."""
        titre = self.input_titre.text().strip()
        auteur = self.input_auteur.text().strip()
        if not titre or not auteur:
            QMessageBox.warning(self, "Erreur", "Titre et auteur sont obligatoires.")
            return

        type_doc = self.combo_type.currentText()  # Livre, Dictionnaire, etc.
        # On encode le type dans le titre pour l'affichage
        titre_complet = f"[{type_doc}] {titre}"

        # On reste avec Livre comme classe concrète (pour emprunts),
        # mais le type visible sera celui choisi dans le titre.
        doc = Livre(titre_complet, auteur, True)
        self.biblio.ajouter_document(doc)

        QMessageBox.information(self, "Succès", f"{type_doc} ajouté.")
        self.input_titre.clear()
        self.input_auteur.clear()
        self.rafraichir_liste()

    def supprimer_document(self) -> None:
        """Supprime le document sélectionné dans la liste."""
        item = self.liste_documents.currentItem()
        if item is None:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un document dans la liste.")
            return

        texte = item.text()   # ex : "[Dictionnaire] Les Misérables (Victor Hugo)"
        # Récupérer la partie avant " (" -> le titre complet avec [Type]
        if " (" in texte:
            titre_complet = texte.split(" (", 1)[0]
        else:
            titre_complet = texte

        # Dans la biblio, d.titre == titre_complet
        for d in list(self.biblio.documents):
            if d.titre == titre_complet:
                self.biblio.documents.remove(d)
                QMessageBox.information(self, "Succès", f"Document '{titre_complet}' supprimé.")
                self.rafraichir_liste()
                return

        QMessageBox.warning(self, "Erreur", "Document introuvable dans la bibliothèque.")


# ================== Fenêtre emprunts ==================
class FenetreEmprunts(QDialog):
    """Fenêtre pour gérer les emprunts."""

    def __init__(self, biblio: Bibliotheque) -> None:
        super().__init__()
        self.biblio = biblio
        self.setWindowTitle("Gestion des emprunts")
        self.resize(500, 400)
        self._configurer_ui()

    def _configurer_ui(self) -> None:
        layout = QVBoxLayout()

        self.liste_emprunts = QListWidget()
        layout.addWidget(QLabel("Liste des emprunts :"))
        layout.addWidget(self.liste_emprunts)

        form_emp = QHBoxLayout()
        self.input_prenom_emp = QLineEdit()
        self.input_nom_emp = QLineEdit()
        self.input_titre_emp = QLineEdit()
        self.input_prenom_emp.setPlaceholderText("Prénom adhérent")
        self.input_nom_emp.setPlaceholderText("Nom adhérent")
        self.input_titre_emp.setPlaceholderText("Titre du livre")
        form_emp.addWidget(self.input_prenom_emp)
        form_emp.addWidget(self.input_nom_emp)
        form_emp.addWidget(self.input_titre_emp)

        btn_ajout = QPushButton("Emprunter")
        btn_retour = QPushButton("Retour livre")
        btn_afficher = QPushButton("Recharger la liste")

        btn_ajout.clicked.connect(self.ajouter_emprunt)
        btn_retour.clicked.connect(self.retourner_emprunt)
        btn_afficher.clicked.connect(self.rafraichir_liste)

        layout.addLayout(form_emp)
        layout.addWidget(btn_ajout)
        layout.addWidget(btn_retour)
        layout.addWidget(btn_afficher)

        self.setLayout(layout)

    def rafraichir_liste(self) -> None:
        self.liste_emprunts.clear()
        for e in self.biblio.lister_emprunts():
            self.liste_emprunts.addItem(str(e))

    def _trouver_adherent(self, nom: str, prenom: str) -> Adherent | None:
        for a in self.biblio.adherents:
            if a.nom == nom and a.prenom == prenom:
                return a
        return None

    def ajouter_emprunt(self) -> None:
        prenom = self.input_prenom_emp.text().strip()
        nom = self.input_nom_emp.text().strip()
        titre = self.input_titre_emp.text().strip()
        if not prenom or not nom or not titre:
            QMessageBox.warning(self, "Erreur", "Tous les champs sont obligatoires.")
            return
        adherent = self._trouver_adherent(nom, prenom)
        if adherent is None:
            QMessageBox.warning(self, "Erreur", "Adhérent introuvable.")
            return
        auj = date.today()
        if self.biblio.emprunter_livre(adherent, titre, auj):
            QMessageBox.information(self, "Succès", "Emprunt créé.")
            self.rafraichir_liste()
        else:
            QMessageBox.warning(self, "Erreur", "Livre introuvable ou non disponible.")

    def retourner_emprunt(self) -> None:
        prenom = self.input_prenom_emp.text().strip()
        nom = self.input_nom_emp.text().strip()
        titre = self.input_titre_emp.text().strip()
        if not prenom or not nom or not titre:
            QMessageBox.warning(self, "Erreur", "Tous les champs sont obligatoires.")
            return
        adherent = self._trouver_adherent(nom, prenom)
        if adherent is None:
            QMessageBox.warning(self, "Erreur", "Adhérent introuvable.")
            return
        auj = date.today()
        if self.biblio.retourner_livre(adherent, titre, auj):
            QMessageBox.information(self, "Succès", "Livre retourné.")
            self.rafraichir_liste()
        else:
            QMessageBox.warning(
                self, "Erreur", "Aucun emprunt correspondant trouvé."
            )


# ================== Fenêtre principale ==================
class FenetrePrincipale(QMainWindow):
    """Page d'accueil : menu coloré avec 3 boutons."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Bibliothèque - Menu principal")
        self.resize(500, 300)

        self.biblio = Bibliotheque()
        charger_bibliotheque(self.biblio)
        self._fen_adh = None
        self._fen_doc = None
        self._fen_emp = None

        self._configurer_ui()

    def _configurer_ui(self) -> None:
        widget_central = QWidget()
        layout = QVBoxLayout()

        titre = QLabel("Bienvenue à votre bibliothèque")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(titre)

        sous_titre = QLabel("Choisissez une action :")
        sous_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sous_titre)

        btn_adherents = QPushButton("Gérer les adhérents")
        btn_documents = QPushButton("Gérer les documents")
        btn_emprunts = QPushButton("Gérer les emprunts")

        btn_adherents.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
        btn_documents.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        btn_emprunts.setStyleSheet("background-color: #e67e22; color: white; padding: 10px;")

        btn_adherents.clicked.connect(self.ouvrir_adherents)
        btn_documents.clicked.connect(self.ouvrir_documents)
        btn_emprunts.clicked.connect(self.ouvrir_emprunts)

        layout.addWidget(btn_adherents)
        layout.addWidget(btn_documents)
        layout.addWidget(btn_emprunts)

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)

    def ouvrir_adherents(self) -> None:
        if self._fen_adh is None or not self._fen_adh.isVisible():
            self._fen_adh = FenetreAdherents(self.biblio)
            # on n'appelle PAS rafraichir_liste ici : liste vide au départ
            self._fen_adh.show()

    def ouvrir_documents(self) -> None:
        if self._fen_doc is None:
            self._fen_doc = FenetreDocuments(self.biblio)
        if not self._fen_doc.isVisible():
            self._fen_doc.show()  # reste visible après ajout

    def ouvrir_emprunts(self) -> None:
        if self._fen_emp is None or not self._fen_emp.isVisible():
            self._fen_emp = FenetreEmprunts(self.biblio)
            # idem
            self._fen_emp.show()

    def closeEvent(self, event) -> None:  # type: ignore[override]
        sauvegarder_bibliotheque(self.biblio)
        event.accept()


# = fonction globale pour lancer l'interface =
def lancer_interface() -> None:
    app = QApplication(sys.argv)
    fen = FenetrePrincipale()
    fen.show()
    app.exec()
