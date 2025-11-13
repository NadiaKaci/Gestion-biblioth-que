class GestionAdherents:
    FICHIER = "adherents.csv"

    @staticmethod
    def charger():
        adherents = []
        try:
            with open(GestionAdherents.FICHIER, "r") as f:
                next(f)  # sauter l’en-tête
                for ligne in f:
                    id, nom, prenom = ligne.strip().split(",")
                    adherents.append(Adherent(int(id), nom, prenom))
        except FileNotFoundError:
            # fichier n’existe pas encore
            with open(GestionAdherents.FICHIER, "w") as f:
                f.write("id,nom,prenom\n")
        return adherents

    @staticmethod
    def ajouter(adherents, nom, prenom):
        if adherents:
            nouveau_id = max(a.id for a in adherents) + 1
        else:
            nouveau_id = 1
        nouvel_adherent = Adherent(nouveau_id, nom, prenom)
        adherents.append(nouvel_adherent)

        # Sauvegarder dans le CSV
        with open(GestionAdherents.FICHIER, "a") as f:
            f.write(f"{nouvel_adherent.id},{nom},{prenom}\n")
        return nouvel_adherent