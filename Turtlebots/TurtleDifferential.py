import math
import pygame

class TurtleDifferential:
    def __init__(self, x=0.0, y=0.0, theta=0.0, L=0.2, R=0.03, color=(0, 100, 255)):
        self.x = x                  # Position en mètres
        self.y = y
        self.theta = theta          # Orientation en radians

        self.L = L                  # Distance entre les roues (m)
        self.R = R                  # Rayon des roues (m)

        self.vg = 0.0               # Vitesse linéaire roue gauche (m/s)
        self.vd = 0.0               # Vitesse linéaire roue droite (m/s)

        self.color = color
        self.traj = []              

    def setWheelSpeeds(self, vg, vd):
        self.vg = vg
        self.vd = vd

    def simule(self, dt):
        v = (self.vd + self.vg) / 2
        w = (self.vd - self.vg) / self.L

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
            points = [(origin[0] + int(x * scale), origin[1] - int(y * scale)) for (x, y) in self.traj]
            pygame.draw.lines(screen, (200, 200, 200), False, points, 1)
