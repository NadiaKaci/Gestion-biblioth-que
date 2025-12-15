from .volume import Volume


class BandeDessinee(Volume):


    def __init__(self, titre: str, auteur: str, dessinateur: str) -> None:
        super().__init__(titre, auteur)
        self.dessinateur = dessinateur

    def __str__(self) -> str:
        return (
            f"BD : {self.titre} ({self.auteur}) - Dessinateur : {self.dessinateur}"
        )
