import pygame
import math

# ----- Paramètres physiques -----
g = 9.81                 # gravité
L = 1.0                  # longueur pendule (m)
dt = 0.001               # pas de temps (s)
damping = 0.2            # amortissement pendule
base_accel = 500.0       # accélération base (px/s²)
max_base_speed = 600.0   # vitesse max base (px/s)

# ----- État initial -----
theta = math.radians(175)  # angle de départ (presque vertical)
omega = 0.0
x_base = 400
v_base = 0.0
a_base = 0.0

# ----- Initialisation Pygame -----
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Étape 2 – Pendule inversé (manuel)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# ----- Fonction de dessin -----
def draw_pendulum(theta, x_base):
    origin = (int(x_base), HEIGHT // 2)
    x = origin[0] + int(L * 200 * math.sin(theta))
    y = origin[1] - int(L * 200 * math.cos(theta))  # haut = vertical
    pygame.draw.line(screen, (0, 0, 0), origin, (x, y), 4)
    pygame.draw.circle(screen, (200, 0, 0), (x, y), 10)
    pygame.draw.rect(screen, (100, 100, 255), (x_base - 30, origin[1] - 10, 60, 20))

# ----- Boucle principale -----
running = True
while running:
    screen.fill((240, 240, 240))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ----- Contrôle clavier ← →
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        a_base = -base_accel
    elif keys[pygame.K_RIGHT]:
        a_base = base_accel
    else:
        a_base = -v_base * 5.0  # freinage base

    # ----- Mise à jour base -----
    v_base += a_base * dt
    v_base = max(-max_base_speed, min(max_base_speed, v_base))
    x_base += v_base * dt
    x_base = max(100, min(WIDTH - 100, x_base))  # limites écran

    # ----- Dynamique pendule avec base mobile -----
    alpha = -(g / L) * math.sin(theta) + (a_base / L) * math.cos(theta)
    alpha -= damping * omega
    omega += alpha * dt
    theta += omega * dt

    # ----- Affichage -----
    draw_pendulum(theta, x_base)

    # Normalisation de l’angle pour affichage lisible
    angle_affiche = math.degrees(theta) % 360
    if angle_affiche > 180:
        angle_affiche -= 360
    txt = font.render(f"θ = {angle_affiche:.1f}°", True, (0, 0, 0))
    screen.blit(txt, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
