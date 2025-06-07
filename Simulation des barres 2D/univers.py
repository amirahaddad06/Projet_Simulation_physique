# univers.py

from random import random, randint
from vector3D import Vector3D as V3D
from particule import Particule
from torseur import Torseur
import pygame
from pygame.locals import *
from types import MethodType
from math import cos, sin

class Univers(object):
    def __init__(self, name='ici', t0=0, step=0.1, dimensions=(100, 100), game=False, gameDimensions=(1024, 780), fps=60):
        self.name = name
        self.time = [t0]
        self.population = []  # Liste de particules
        self.barres = []      # Liste de barres
        self.liaisons = []    # Liste de liaisons
        self.generators = []  # Liste de générateurs de forces
        self.step = step

        self.dimensions = dimensions
        self.game = game
        self.gameDimensions = gameDimensions
        self.gameFPS = fps

        self.scale = gameDimensions[0] / dimensions[0]

    def __str__(self):
        return 'Univers (%s, %g, %g)' % (self.name, self.time[0], self.step)

    def __repr__(self):
        return str(self)

    # --- Ajout d'éléments ---
    def addParticule(self, *members):
        for i in members:
            self.population.append(i)

    def addBarre(self, *members):
        for b in members:
            self.barres.append(b)

    def addGenerators(self, *members):
        for g in members:
            self.generators.append(g)

    def addLiaison(self, *members):
        for l in members:
            self.liaisons.append(l)

    # --- Simulation ---
    def simulateAll(self):
        # Appliquer les contraintes des liaisons avant de simuler
        for liaison in self.liaisons:
            liaison.appliquerContrainte()

        # Simuler toutes les particules
        for p in self.population:
            for source in self.generators:
                source.setForce(p)
            p.simulate(self.step)

        # Simuler toutes les barres
        for b in self.barres:
            for source in self.generators:
                if hasattr(source, 'appliquer'):
                    torseur = source.appliquer(b)
                    if torseur is not None:
                        b.applyTorseur(torseur)
            b.simulate(self.step)

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

    # --- Interaction Clavier ---
    def gameInteraction(self, events, keys):
        force_value = 5   # Force appliquée par flèche
        moment_value = 5   # Moment appliqué par touches A/D

        for b in self.barres:
            if hasattr(b, 'controlable') and b.controlable:
                force = V3D()
                moment = 0.0

                # Appliquer forces par flèches
                if keys[pygame.K_UP]:
                    force += V3D(0, 1, 0) * force_value
                if keys[pygame.K_DOWN]:
                    force += V3D(0, -1, 0) * force_value
                if keys[pygame.K_LEFT]:
                    force += V3D(-1, 0, 0) * force_value
                if keys[pygame.K_RIGHT]:
                    force += V3D(1, 0, 0) * force_value

                # Appliquer moment par touches A/D
                if keys[pygame.K_a]:
                    moment += moment_value
                if keys[pygame.K_d]:
                    moment -= moment_value

                # Appliquer via TORSEUR
                if force.mod() > 0:
                    torseur_force = Torseur(P=b.position, R=force, M=V3D(0, 0, 0))
                    b.applyTorseur(torseur_force)

                if moment != 0:
                    torseur_moment = Torseur(P=b.position, R=V3D(0, 0, 0), M=V3D(0, 0, moment))
                    b.applyTorseur(torseur_moment)

    # --- Boucle principale ---
    def simulateRealTime(self):
        running = self.game
        successes, failures = pygame.init()
        W, H = self.gameDimensions
        screen = pygame.display.set_mode((W, H))
        clock = pygame.time.Clock()

        while running:
            screen.fill((240, 240, 240))

            pygame.event.pump()
            keys = pygame.key.get_pressed()
            events = pygame.event.get()

            if keys[pygame.K_ESCAPE]:
                running = False
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            # Interaction utilisateur
            self.gameInteraction(events, keys)

            # Avancer la simulation
            self.simulateFor(1 / self.gameFPS)

            # Dessiner toutes les particules
            for p in self.population:
                p.gameDraw(self.scale, screen)

            # Dessiner toutes les barres
            for b in self.barres:
                b.gameDraw(self.scale, screen)

            # Dessiner les torseurs appliqués
            for b in self.barres:
                b.drawTorseur(screen, self.scale)

            # Afficher le temps simulé
            flip_surface = pygame.transform.flip(screen, False, True)
            screen.blit(flip_surface, (0, 0))

            font_obj = pygame.font.Font('freesansbold.ttf', 12)
            text_surface_obj = font_obj.render(('time: %.2f' % self.time[-1]), True, 'green', (240, 240, 240))
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.topleft = (0, 0)
            screen.blit(text_surface_obj, text_rect_obj)

            pygame.display.flip()
            clock.tick(self.gameFPS)

        pygame.quit()
