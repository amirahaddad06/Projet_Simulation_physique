import math
import pygame
from MoteurCC import MoteurCC

class TurtleDifferentialMotor:
    def __init__(self, x=0.0, y=0.0, theta=0.0, L=0.2, R=0.03, color=(255, 100, 0)):
        self.x = x
        self.y = y
        self.theta = theta  # orientation (rad)

        self.L = L  # distance entre les roues
        self.R = R  # rayon des roues

        self.color = color
        self.traj = []

        # 🧠 Deux moteurs CC (un par roue)
        self.moteur_g = MoteurCC()
        self.moteur_d = MoteurCC()

    def setVoltages(self, Ug, Ud):
        self.moteur_g.setVoltage(Ug)
        self.moteur_d.setVoltage(Ud)

    def simule(self, dt):
        # Mise à jour des moteurs
        self.moteur_g.simule(dt)
        self.moteur_d.simule(dt)

        # Récupère vitesse angulaire des moteurs
        w_g = self.moteur_g.getSpeed()  # rad/s
        w_d = self.moteur_d.getSpeed()

        # Convertir en vitesse linéaire
        vg = w_g * self.R
        vd = w_d * self.R

        # Cinématique robot
        v = (vd + vg) / 2
        w = (vd - vg) / self.L

        self.x += v * math.cos(self.theta) * dt
        self.y += v * math.sin(self.theta) * dt
        self.theta += w * dt

        self.traj.append((self.x, self.y))

    def draw(self, screen, scale=100, origin=(400, 300)):
        px = origin[0] + int(self.x * scale)
        py = origin[1] - int(self.y * scale)

        pygame.draw.circle(screen, self.color, (px, py), 10)
        dx = int(15 * math.cos(self.theta))
        dy = int(-15 * math.sin(self.theta))
        pygame.draw.line(screen, (0, 0, 0), (px, py), (px + dx, py + dy), 2)

        if len(self.traj) > 1:
            pts = [(origin[0] + int(x * scale), origin[1] - int(y * scale)) for (x, y) in self.traj]
            pygame.draw.lines(screen, (180, 180, 180), False, pts, 1)
