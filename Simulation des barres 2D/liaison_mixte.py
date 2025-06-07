# liaison_mixte.py

from vector3D import Vector3D as V3D
from liaison import Liaison
from math import atan2

class LiaisonMixte(Liaison):
    def __init__(self, barre1, barre2, point_reference, direction_prismatique):
        super().__init__(barre1, barre2)
        self.point_reference = point_reference  # Point d'accrochage fixe
        self.direction = direction_prismatique.norm()  # Direction du glissement autorisé

    def appliquerContrainte(self):
        # Recalculer la position de l’extrémité A de la barre 2
        A2, B2 = self.barre2.getExtremities()

        # Correction translation : déplacer l’extrémité A sur la ligne
        dp = A2 - self.point_reference
        distance_along = dp ** self.direction
        point_corrige = self.point_reference + distance_along * self.direction

        # Calcul du vecteur de correction
        deplacement = point_corrige - A2

        # Déplacer toute la barre
        self.barre2.position += deplacement

        # Correction rotation : réaligner la barre par rapport à la direction de glissement
        A2_corrige, B2_corrige = self.barre2.getExtremities()
        vecteur_barre = B2_corrige - A2_corrige

        angle_barre = atan2(vecteur_barre.y, vecteur_barre.x)
        angle_direction = atan2(self.direction.y, self.direction.x)

        # Déterminer l'angle relatif
        correction_angle = angle_direction - angle_barre

        # Appliquer la correction de rotation
        self.barre2.orientation += correction_angle

        # Correction des vitesses (optionnel mais mieux)
        v = self.barre2.vitesse_lin
        self.barre2.vitesse_lin = (v ** self.direction) * self.direction
