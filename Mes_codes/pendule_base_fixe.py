import pygame
import math

# ----- Paramètres physiques -----
g = 9.81              # gravité (m/s²)
L = 1.0               # longueur du pendule (m)
m = 1.0               # masse du pendule (kg)
dt = 0.01             # pas de temps (s)

# ----- État initial -----
theta = math.radians(180-5)  # angle initial en radians
omega = 0.0               # vitesse angulaire
x_base = 400              # position horizontale de la base (pixels, fixe)

# ----- Initialisation Pygame -----
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendule inversé - Étape 1 (libre)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# ----- Dessin du système -----
def draw_pendulum(theta, x_base):
    origin = (int(x_base), HEIGHT // 2)
    x = origin[0] + int(L * 200 * math.sin(theta))
    y = origin[1] + int(L * 200 * math.cos(theta))
    pygame.draw.line(screen, (0, 0, 0), origin, (x, y), 4)
    pygame.draw.circle(screen, (150, 0, 0), (x, y), 10)
    pygame.draw.rect(screen, (100, 100, 255), (x_base - 30, origin[1] - 10, 60, 20))  # base

# ----- Boucle principale -----
running = True
while running:
    screen.fill((240, 240, 240))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ----- Dynamique du pendule (équation de la chute) -----
    alpha = -(g / L) * math.sin(theta)  # accélération angulaire
    omega += alpha * dt                # mise à jour de la vitesse
    theta += omega * dt               # mise à jour de l’angle

    # ----- Affichage -----
    draw_pendulum(theta, x_base)
    txt = font.render(f"θ = {math.degrees(theta):.2f}°", True, (0, 0, 0))
    screen.blit(txt, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
