import pygame
from MoteurCC import MoteurCC
from math import cos, sin

# Initialiser le moteur CC
moteur = MoteurCC(
    R=1.0, L=0.001, kc=0.01, ke=0.01,
    J=0.01, f=0.1
)

# Paramètres simulation
dt = 0.01  # pas de temps
Umax = 12  # tension max pour sécurité

# Initialiser Pygame
pygame.init()
W, H = 600, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Commande temps réel du Moteur CC")
clock = pygame.time.Clock()
center = (W // 2, H // 2)
rayon = 100
font = pygame.font.SysFont("Arial", 18)
running = True

# Boucle principale
while running:
    screen.fill((240, 240, 240))
    keys = pygame.key.get_pressed()

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

    # Commande clavier : changer la tension
    if keys[pygame.K_UP]:
        moteur.setVoltage(min(moteur.Um + 0.1, Umax))
    if keys[pygame.K_DOWN]:
        moteur.setVoltage(max(moteur.Um - 0.1, -Umax))

    # Simulation du moteur
    moteur.simule(dt)

    # Position angulaire -> coordonnées de l'extrémité
    theta = moteur.getPosition()
    x = int(center[0] + rayon * cos(theta))
    y = int(center[1] + rayon * sin(theta))

    # Dessin
    pygame.draw.circle(screen, (0, 0, 0), center, 5)
    pygame.draw.line(screen, (0, 100, 200), center, (x, y), 4)

    # Afficher la tension et la vitesse
    txt_um = font.render(f"Tension Um = {moteur.Um:.2f} V", True, (0, 0, 0))
    txt_omega = font.render(f"Vitesse ω = {moteur.getSpeed():.2f} rad/s", True, (0, 0, 0))
    screen.blit(txt_um, (10, 10))
    screen.blit(txt_omega, (10, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
