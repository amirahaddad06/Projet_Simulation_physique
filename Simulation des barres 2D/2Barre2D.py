from univers import Univers
from Barre2D import Barre2D
from liaison import LiaisonPivot, LiaisonPrismatique
from vector3D import Vector3D as V3D

U = Univers(name="Test_Final_Liaisons", game=True)

B1 = Barre2D(centre=V3D(20, 20, 0), orientation=0.0, longueur=10.0, masse=1000000)
B1.vitesse_lin = V3D(0, 0, 0)
B1.vitesse_ang = 0.0

extremite_B1 = B1.getExtremities()[1]
centre_B2 = extremite_B1 + V3D(5, 0, 0)
B2 = Barre2D(centre=centre_B2, orientation=0.0, longueur=10.0, masse=1.0)
B2.controlable = True

pivot = LiaisonPivot(B1, B2, point_pivot=extremite_B1)
prismatique = LiaisonPrismatique(B1, B2, direction=V3D(1, 0, 0))

U.addBarre(B1, B2)
U.addLiaison(pivot)
U.addLiaison(prismatique)

U.simulateRealTime()
