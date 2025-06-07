# ressort.py

from vector3D import Vector3D as V3D
from torseur import Torseur

class Ressort:
    def __init__(self, point_ancrage, objet, longueur_repos, raideur):
        self.point_ancrage = point_ancrage  # Point fixe où est accroché le ressort
        self.objet = objet                  # Objet relié au ressort
        self.longueur_repos = longueur_repos
        self.k = raideur                    # Raideur du ressort (N/m)

    def appliquer(self, objet):
        if objet != self.objet:
            return None

        # Vecteur entre ancrage et l'objet
        vecteur = objet.position - self.point_ancrage
        distance = vecteur.mod()
        if distance == 0:
            return None  # Éviter division par zéro

        direction = vecteur.norm()

        # Loi de Hooke : F = -k (x - x0)
        force_magnitude = -self.k * (distance - self.longueur_repos)
        force = direction * force_magnitude

        return Torseur(P=objet.position, R=force, M=V3D(0, 0, 0))  # Force sans moment
