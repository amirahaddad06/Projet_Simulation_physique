from random import random
from vector3D import Vector3D as V3D
from particule import Particule
import pygame
from pygame.locals import *
from types import MethodType

class Univers(object):
    def __init__(self, name='ici', t0=0, step=0.1, dimensions=(100,100), game=False, gameDimensions=(1024,780), fps=60):
        self.name = name
        self.time = [t0]
        self.population = []
        self.generators = []
        self.step = step
        self.dimensions = dimensions
        self.game = game
        self.gameDimensions = gameDimensions
        self.gameFPS = fps
        self.scale = gameDimensions[0] / dimensions[0]

    def __str__(self):
        return f'Univers ({self.name}, {self.time[0]}, {self.step})'

    def __repr__(self):
        return str(self)

    def addParticule(self, *members):
        self.population.extend(members)

    def addGenerators(self, *members):
        self.generators.extend(members)

    def simulateAll(self):
        for p in self.population:
            for source in self.generators:
                source.setForce(p)
            p.simulate(self.step)
        self.time.append(self.time[-1] + self.step)

    def simulateFor(self, duration):
        while duration > 0:
            self.simulateAll()
            duration -= self.step

    def plot(self):
        from pylab import figure, legend, show
        figure(self.name)
        for agent in self.population:
            agent.plot()
        legend()
        show()

    def gameInteraction(self, events, keys):
        pass  # à surcharger

    def simulateRealTime(self):
        pygame.init()
        screen = pygame.display.set_mode(self.gameDimensions)
        clock = pygame.time.Clock()
        running = self.game

        while running:
            screen.fill((240,240,240))

            pygame.event.pump()
            keys = pygame.key.get_pressed()
            events = pygame.event.get()

            if keys[pygame.K_ESCAPE]:
                running = False

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            self.gameInteraction(events, keys)
            self.simulateFor(1 / self.gameFPS)

            for t in self.population:
                t.gameDraw(self.scale, screen)

            # Texte affiché non retourné
            font_obj = pygame.font.Font('freesansbold.ttf', 12)
            time_text = font_obj.render(f'time: {self.time[-1]:.2f}', True, 'green', (240,240,240))
            screen.blit(time_text, (10, 10))

            pygame.display.flip()
            clock.tick(self.gameFPS)

        pygame.quit()

# === Forces ===
class Force:
    def __init__(self, force=V3D(), name='force', active=True):
        self.force = force
        self.name = name
        self.active = active

    def __str__(self):
        return f"Force ({self.force}, {self.name})"

    def setForce(self, particule):
        if self.active:
            particule.applyForce(self.force)

class Gravity(Force):
    def __init__(self, g=V3D(0,-9.8), name='gravity', active=True):
        self.g = g
        self.name = name
        self.active = active

    def setForce(self, particule):
        if self.active:
            particule.applyForce(self.g * particule.mass)

class SpringDamper(Force):
    def __init__(self, P0, P1, k=0, c=0, l0=0, active=True, name="spring_and_damper"):
        super().__init__(V3D(), name, active)
        self.k = k
        self.c = c
        self.P0 = P0
        self.P1 = P1
        self.l0 = l0

    def setForce(self, particule):
        vec = self.P1.getPosition() - self.P0.getPosition()
        v_n = vec.norm()
        flex = vec.mod() - self.l0
        vit = self.P1.getSpeed() - self.P0.getSpeed()
        vit_n = vit ** v_n * self.c
        force = (self.k * flex + vit_n) * v_n
        if particule == self.P0:
            particule.applyForce(force)
        elif particule == self.P1:
            particule.applyForce(-force)

class Link(SpringDamper):
    def __init__(self, P0, P1, name="link"):
        l0 = (P0.getPosition() - P1.getPosition()).mod()
        super().__init__(P0, P1, 1000, 100, l0, True, name)
