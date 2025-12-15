# outils/verification.py
# Fonctions de validation pour les entrées utilisateur (console)


def lire_choix_menu(options_valides: set[str]) -> str:
    """
    Lit un choix au clavier pour le menu (1..9, Q).
    Redemande tant que l'utilisateur n'entre pas une valeur valide.
    """
    while True:
        choix = input("Choisissez une action : ").strip().upper()
        if choix in options_valides:
            return choix
        print("Choix erroné!")  # message demandé dans l'énoncé


def lire_entier(message: str, minimum=None, maximum=None) -> int:
    """
    Lit un entier au clavier avec gestion d'erreur.
    Optionnellement limite la valeur entre minimum et maximum.
    """
    while True:
        saisie = input(message).strip()
        if not saisie.isdigit():
            print("Saisie erronée! Entrez un nombre entier.")
            continue

        valeur = int(saisie)
        if minimum is not None and valeur < minimum:
            print(f"Saisie erronée! La valeur doit être >= {minimum}.")
            continue
        if maximum is not None and valeur > maximum:
            print(f"Saisie erronée! La valeur doit être <= {maximum}.")
            continue

        return valeur


def lire_chaine_non_vide(message: str) -> str:
    """
    Lit une chaîne non vide au clavier.
    Redemande tant que l'utilisateur n'entre que des espaces ou rien.
    """
    while True:
        saisie = input(message).strip()
        if saisie == "":
            print("Saisie erronée! Veuillez entrer une valeur non vide.")
        else:
            return saisie
