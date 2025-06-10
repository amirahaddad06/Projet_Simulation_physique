# Barre2D.py

from random import random, randint
from vector3D import Vector3D as V3D
from torseur import Torseur
import pygame
from pygame.locals import *
from types import MethodType
from math import cos, sin

class Barre2D:
    def __init__(self, centre=V3D(0, 0, 0), orientation=0.0, longueur=10.0, masse=1.0, nom="Barre"):
        self.nom = nom
        self.position = centre
        self.orientation = orientation
        self.longueur = longueur
        self.masse = masse
        self.vitesse_lin = V3D(0, 0, 0)
        self.vitesse_ang = 0.0
        self.inertie = (1/12) * self.masse * (self.longueur ** 2)
        self.forces = []

    def applyTorseur(self, torseur: Torseur):
        self.forces.append(torseur)

    def simulate(self, dt):
        force_total = V3D(0, 0, 0)
        moment_total = 0.0

        for T in self.forces:
            r = T.P - self.position
            force_total += T.R
            moment_total += (r * T.R).z + T.M.z

        accel = force_total * (1 / self.masse)
        self.vitesse_lin += accel * dt
        self.position += self.vitesse_lin * dt

        ang_accel = moment_total / self.inertie
        self.vitesse_ang += ang_accel * dt
        self.orientation += self.vitesse_ang * dt

        
        frein_lin = 0.98
        frein_ang = 0.98
        self.vitesse_lin = self.vitesse_lin * frein_lin
        self.vitesse_ang = self.vitesse_ang * frein_ang

        self.forces = []  # Réinitialiser après simulation

    def getExtremities(self):
        dx = (self.longueur / 2) * cos(self.orientation)
        dy = (self.longueur / 2) * sin(self.orientation)
        A = V3D(self.position.x - dx, self.position.y - dy)
        B = V3D(self.position.x + dx, self.position.y + dy)
        return A, B

    def gameDraw(self, scale, screen):
        A, B = self.getExtremities()
        x1, y1 = int(A.x * scale), int(screen.get_height() - A.y * scale)
        x2, y2 = int(B.x * scale), int(screen.get_height() - B.y * scale)

        pygame.draw.line(screen, (0, 0, 255), (x1, y1), (x2, y2), 5)
        pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x * scale), int(screen.get_height() - self.position.y * scale)), 5)

    def drawTorseur(self, screen, scale):
        # Dessiner les torseurs appliqués pendant la frame
        for T in self.forces:
            start = (int(self.position.x * scale), int(screen.get_height() - self.position.y * scale))
            end = (int((self.position.x + T.R.x * 0.2) * scale), int(screen.get_height() - (self.position.y + T.R.y * 0.2) * scale))
            pygame.draw.line(screen, (255, 0, 0), start, end, 3)  # Force en rouge
            pygame.draw.circle(screen, (255, 0, 0), end, 5)

            if abs(T.M.z) > 0.01:
                center = start
                radius = 15
                color = (0, 255, 0)  # Moment en vert
                pygame.draw.circle(screen, color, center, radius, 2)
