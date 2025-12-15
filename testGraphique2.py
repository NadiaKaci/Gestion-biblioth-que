# ---------------------------------
# Bibliothèque GUI avec PyQt6
# ---------------------------------
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QHBoxLayout, QTextEdit,
    QComboBox, QTabWidget, QInputDialog
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
from datetime import date, timedelta, datetime
import sys

# ---------------------------------
# Classes de données
# ---------------------------------
class Document:
    def __init__(self, id_doc, titre, auteur=""):
        self.id = id_doc
        self.titre = titre
        self.auteur = auteur
        self.est_disponible = True  # Tous les documents sont disponibles par défaut

class Livre(Document):
    def __init__(self, id_doc, titre, auteur=""):
        super().__init__(id_doc, titre, auteur)

class BandeDessinee(Document):
    def __init__(self, id_doc, titre, auteur, dessinateur):
        super().__init__(id_doc, titre, auteur)
        self.dessinateur = dessinateur

class Journal(Document):
    def __init__(self, id_doc, titre, auteur, date_parution):
        super().__init__(id_doc, titre, auteur)
        self.date_parution = date_parution

class Dictionnaire(Document):
    pass

class Adherent:
    def __init__(self, id_ad, nom, prenom, email=""):
        self.id = id_ad
        self.nom = nom
        self.prenom = prenom
        self.email = email

class Emprunt:
    def __init__(self, id_em, id_ad, id_doc, date_emprunt, date_retour):
        self.id = id_em
        self.id_ad = id_ad
        self.id_doc = id_doc
        self.date_emprunt = date_emprunt
        self.date_retour = date_retour

# ---------------------------------
# Gestion de la bibliothèque
# ---------------------------------
class Bibliotheque:
    def __init__(self):
        self.adherents = []
        self.documents = []
        self.emprunts = []

    def nouvelle_id(self, collection):
        if collection:
            return str(int(max([obj.id for obj in collection], key=int)) + 1)
        return "1"

    # Adhérents
    def ajouter_adherent(self, nom, prenom, email=""):
        id_ad = self.nouvelle_id(self.adherents)
        self.adherents.append(Adherent(id_ad, nom, prenom, email))
        return id_ad

    def supprimer_adherent(self, id_ad):
        before = len(self.adherents)
        self.adherents = [a for a in self.adherents if a.id != id_ad]
        return len(self.adherents) != before

    # Documents
    def ajouter_document(self, doc):
        self.documents.append(doc)
        return doc.id

    def supprimer_document(self, id_doc):
        before = len(self.documents)
        self.documents = [d for d in self.documents if d.id != id_doc]
        return len(self.documents) != before

    # Emprunts
    def ajouter_emprunt(self, id_ad, id_doc):
        adherent = next((a for a in self.adherents if a.id == id_ad), None)
        doc = next((d for d in self.documents if d.id == id_doc), None)
        if not adherent:
            return None  # Adhérent introuvable
        if not doc:
            return None  # Document introuvable
        if not doc.est_disponible:
            return None  # Document déjà emprunté
        id_em = self.nouvelle_id(self.emprunts)
        date_e = date.today()
        date_r = date_e + timedelta(days=15)
        self.emprunts.append(Emprunt(id_em, id_ad, id_doc, date_e, date_r))
        doc.est_disponible = False
        return id_em

    def retour_emprunt(self, id_em):
        emprunt = next((e for e in self.emprunts if e.id == id_em), None)
        if emprunt:
            doc = next((d for d in self.documents if d.id == emprunt.id_doc), None)
            if doc:
                doc.est_disponible = True
            self.emprunts = [e for e in self.emprunts if e.id != id_em]
            return True
        return False

# ---------------------------------
# Interface graphique
# ---------------------------------
class BibliothequeGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.biblio = Bibliotheque()
        self.setWindowTitle("Bibliothèque")
        self.setGeometry(200, 200, 800, 600)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#34495e"))
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label_welcome = QLabel("Bienvenue à votre Bibliothèque")
        self.label_welcome.setFont(QFont("Arial", 20))
        self.label_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_welcome.setStyleSheet("color: white;")
        self.layout.addWidget(self.label_welcome)

        self.label_option = QLabel("Choisissez une option :")
        self.label_option.setFont(QFont("Arial", 16))
        self.label_option.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_option.setStyleSheet("color: white;")
        self.layout.addWidget(self.label_option)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.tab_adherents()
        self.tab_documents()
        self.tab_emprunts()

    # ------------------- Adhérents -------------------
    def tab_adherents(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.nom_ad = QLineEdit()
        self.nom_ad.setPlaceholderText("Nom")
        layout.addWidget(self.nom_ad)

        self.prenom_ad = QLineEdit()
        self.prenom_ad.setPlaceholderText("Prénom")
        layout.addWidget(self.prenom_ad)

        self.email_ad = QLineEdit()
        self.email_ad.setPlaceholderText("Email")
        layout.addWidget(self.email_ad)

        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        btn_add = QPushButton("Ajouter")
        btn_add.clicked.connect(self.ajouter_adherent)
        btn_layout.addWidget(btn_add)

        btn_show = QPushButton("Afficher")
        btn_show.clicked.connect(self.afficher_adherents)
        btn_layout.addWidget(btn_show)

        btn_del = QPushButton("Supprimer par ID")
        btn_del.clicked.connect(self.supprimer_adherent)
        btn_layout.addWidget(btn_del)

        self.text_adherents = QTextEdit()
        self.text_adherents.setReadOnly(True)
        layout.addWidget(self.text_adherents)

        self.tabs.addTab(tab, "Adhérents")

    def ajouter_adherent(self):
        nom = self.nom_ad.text().strip()
        prenom = self.prenom_ad.text().strip()
        email = self.email_ad.text().strip()
        if not nom or not prenom:
            QMessageBox.warning(self, "Erreur", "Nom et prénom obligatoires")
            return
        id_ad = self.biblio.ajouter_adherent(nom, prenom, email)
        QMessageBox.information(self, "Succès", f"Adhérent ajouté avec ID {id_ad}")
        self.nom_ad.clear()
        self.prenom_ad.clear()
        self.email_ad.clear()

    def afficher_adherents(self):
        self.text_adherents.clear()
        for a in self.biblio.adherents:
            self.text_adherents.append(f"ID {a.id} | {a.nom} {a.prenom} | {a.email}")

    def supprimer_adherent(self):
        id_ad, ok = QInputDialog.getText(self, "Supprimer adhérent", "ID :")
        if ok:
            id_ad = id_ad.strip()
            success = self.biblio.supprimer_adherent(id_ad)
            if success:
                QMessageBox.information(self, "Succès", "Adhérent supprimé")
            else:
                QMessageBox.warning(self, "Erreur", "ID introuvable")

    # ------------------- Documents -------------------
    def tab_documents(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.type_doc = QComboBox()
        self.type_doc.addItems(["Livre", "Bande Dessinée", "Journal", "Dictionnaire"])
        layout.addWidget(self.type_doc)

        self.titre_doc = QLineEdit()
        self.titre_doc.setPlaceholderText("Titre")
        layout.addWidget(self.titre_doc)

        self.auteur_doc = QLineEdit()
        self.auteur_doc.setPlaceholderText("Auteur")
        layout.addWidget(self.auteur_doc)

        self.dessinateur_doc = QLineEdit()
        self.dessinateur_doc.setPlaceholderText("Dessinateur (BD uniquement)")
        layout.addWidget(self.dessinateur_doc)

        self.date_doc = QLineEdit()
        self.date_doc.setPlaceholderText("Date parution YYYY-MM-DD (Journal uniquement)")
        layout.addWidget(self.date_doc)

        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        btn_add = QPushButton("Ajouter")
        btn_add.clicked.connect(self.ajouter_document)
        btn_layout.addWidget(btn_add)

        btn_show = QPushButton("Afficher")
        btn_show.clicked.connect(self.afficher_documents)
        btn_layout.addWidget(btn_show)

        btn_del = QPushButton("Supprimer par ID")
        btn_del.clicked.connect(self.supprimer_document)
        btn_layout.addWidget(btn_del)

        self.text_documents = QTextEdit()
        self.text_documents.setReadOnly(True)
        layout.addWidget(self.text_documents)

        self.tabs.addTab(tab, "Documents")

    def ajouter_document(self):
        type_doc = self.type_doc.currentText()
        titre = self.titre_doc.text().strip()
        auteur = self.auteur_doc.text().strip()
        dessinateur = self.dessinateur_doc.text().strip()
        date_parution = self.date_doc.text().strip()

        if not titre:
            QMessageBox.warning(self, "Erreur", "Titre obligatoire")
            return

        id_doc = self.biblio.nouvelle_id(self.biblio.documents)
        if type_doc == "Livre":
            doc = Livre(id_doc, titre, auteur)
        elif type_doc == "Bande Dessinée":
            doc = BandeDessinee(id_doc, titre, auteur, dessinateur)
        elif type_doc == "Journal":
            try:
                d = datetime.strptime(date_parution, "%Y-%m-%d").date()
            except:
                d = date.today()
            doc = Journal(id_doc, titre, auteur, d)
        else:
            doc = Dictionnaire(id_doc, titre, auteur)

        self.biblio.ajouter_document(doc)
        QMessageBox.information(self, "Succès", f"Document ajouté avec ID {id_doc}")
        self.titre_doc.clear()
        self.auteur_doc.clear()
        self.dessinateur_doc.clear()
        self.date_doc.clear()

    def afficher_documents(self):
        self.text_documents.clear()
        for d in self.biblio.documents:
            line = f"ID {d.id} | {type(d).__name__} | {d.titre} | Auteur: {getattr(d,'auteur','')}"
            if isinstance(d, BandeDessinee):
                line += f" | Dessinateur: {d.dessinateur}"
            if isinstance(d, Journal):
                line += f" | Parution: {d.date_parution}"
            line += f" | Disponible: {'Oui' if d.est_disponible else 'Non'}"
            self.text_documents.append(line)

    def supprimer_document(self):
        id_doc, ok = QInputDialog.getText(self, "Supprimer document", "ID :")
        if ok:
            id_doc = id_doc.strip()
            success = self.biblio.supprimer_document(id_doc)
            if success:
                QMessageBox.information(self, "Succès", "Document supprimé")
            else:
                QMessageBox.warning(self, "Erreur", "ID introuvable")

    # ------------------- Emprunts -------------------
    def tab_emprunts(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.id_ad_em = QLineEdit()
        self.id_ad_em.setPlaceholderText("ID Adhérent")
        layout.addWidget(self.id_ad_em)

        self.id_doc_em = QLineEdit()
        self.id_doc_em.setPlaceholderText("ID Document")
        layout.addWidget(self.id_doc_em)

        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        btn_add = QPushButton("Ajouter Emprunt")
        btn_add.clicked.connect(self.ajouter_emprunt)
        btn_layout.addWidget(btn_add)

        btn_show = QPushButton("Afficher Emprunts")
        btn_show.clicked.connect(self.afficher_emprunts)
        btn_layout.addWidget(btn_show)

        btn_retour = QPushButton("Retour Emprunt")
        btn_retour.clicked.connect(self.retour_emprunt)
        btn_layout.addWidget(btn_retour)

        self.text_emprunts = QTextEdit()
        self.text_emprunts.setReadOnly(True)
        layout.addWidget(self.text_emprunts)

        self.tabs.addTab(tab, "Emprunts")

    def ajouter_emprunt(self):
        id_ad = self.id_ad_em.text().strip()
        id_doc = self.id_doc_em.text().strip()
        if not id_ad or not id_doc:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer ID Adhérent et ID Document")
            return
        id_em = self.biblio.ajouter_emprunt(id_ad, id_doc)
        if id_em:
            QMessageBox.information(self, "Succès", f"Emprunt ajouté ID {id_em}")
            self.id_ad_em.clear()
            self.id_doc_em.clear()
        else:
            QMessageBox.warning(
                self, "Erreur",
                "Impossible d'ajouter l'emprunt\n- Vérifiez les ID\n- Vérifiez la disponibilité du document"
            )

    def afficher_emprunts(self):
        self.text_emprunts.clear()
        for e in self.biblio.emprunts:
            self.text_emprunts.append(
                f"ID Emprunt {e.id} | Adhérent {e.id_ad} | Document {e.id_doc} | Emprunt {e.date_emprunt} | Retour {e.date_retour}"
            )

    def retour_emprunt(self):
        id_em, ok = QInputDialog.getText(self, "Retour Emprunt", "ID Emprunt :")
        if ok:
            id_em = id_em.strip()
            success = self.biblio.retour_emprunt(id_em)
            if success:
                QMessageBox.information(self, "Succès", "Document retourné")
            else:
                QMessageBox.warning(self, "Erreur", "ID introuvable")

# ------------------- Programme principal -------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = BibliothequeGUI()
    gui.show()
    sys.exit(app.exec())
