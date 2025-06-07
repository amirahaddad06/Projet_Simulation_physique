# liaison.py

from abc import ABC, abstractmethod
from vector3D import Vector3D as V3D

# --- Base abstraite pour toutes les liaisons ---
class Liaison(ABC):
    def __init__(self, barre1, barre2):
        self.barre1 = barre1
        self.barre2 = barre2

    @abstractmethod
    def appliquerContrainte(self):
        pass

# --- Liaison Pivot : autoriser la rotation autour d'un point fixe ---
class LiaisonPivot(Liaison):
    def __init__(self, barre1, barre2, point_pivot):
        super().__init__(barre1, barre2)
        self.point_pivot = point_pivot  # Point fixe où est attachée l'extrémité A de la barre 2

    def appliquerContrainte(self):
        A2, _ = self.barre2.getExtremities()

        # Corriger la position du centre de la barre pour que A2 reste collé au pivot
        correction = self.point_pivot - A2
        self.barre2.position += correction
        # Remarque : on laisse la barre tourner librement (pas de correction d'orientation ici)

# --- Liaison Prismatique : autoriser seulement le glissement dans une direction ---
class LiaisonPrismatique(Liaison):
    def __init__(self, barre1, barre2, direction):
        super().__init__(barre1, barre2)
        self.direction = direction.norm()  # Direction du coulissement autorisé (normalisée)

    def appliquerContrainte(self):
        # Correction uniquement perpendiculaire à la direction de glissement
        dp = self.barre2.position - self.barre1.position

        # Projeté sur la direction autorisée
        projection = (dp ** self.direction) * self.direction
        correction = projection - dp

        # Appliquer la correction
        self.barre2.position += correction
