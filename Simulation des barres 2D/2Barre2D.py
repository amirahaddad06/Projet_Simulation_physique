# test_final.py

from univers import Univers
from Barre2D import Barre2D
from liaison import LiaisonPivot, LiaisonPrismatique
from vector3D import Vector3D as V3D

# Créer l'univers
U = Univers(name="Test_Final_Liaisons", game=True)

# --- Barre 1 fixe (ancrée) ---
B1 = Barre2D(centre=V3D(20, 20, 0), orientation=0.0, longueur=10.0, masse=1000000)
B1.vitesse_lin = V3D(0, 0, 0)
B1.vitesse_ang = 0.0

# --- Barre 2 mobile (contrôlée)
# Position initiale : extrémité droite de B1 + décalage sur X
extremite_B1 = B1.getExtremities()[1]  # point B
centre_B2 = extremite_B1 + V3D(5, 0, 0)  # décalage horizontal
B2 = Barre2D(centre=centre_B2, orientation=0.0, longueur=10.0, masse=1.0)
B2.controlable = True  # Permet le contrôle clavier

# --- Liaisons séparées ---
# 1) Pivot entre extrémité de B1 et extrémité A de B2
pivot = LiaisonPivot(B1, B2, point_pivot=extremite_B1)

# 2) Prismatique autorisant le glissement horizontal
prismatique = LiaisonPrismatique(B1, B2, direction=V3D(1, 0, 0))  # glissement en X uniquement

# --- Ajouter à l'univers
U.addBarre(B1, B2)
U.addLiaison(pivot)
U.addLiaison(prismatique)

# --- Lancer la simulation en temps réel
U.simulateRealTime()
