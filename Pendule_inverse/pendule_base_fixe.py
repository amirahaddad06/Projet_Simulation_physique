import pygame
import math
import matplotlib.pyplot as plt

# Constantes physiques
g = 9.81
l = 1.0
m = 1.0
theta = math.radians(20)
omega = 0.0
dt = 0.01
t = 0.0

 
t_hist = []
theta_hist = []
theta_lin_hist = []

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Pendule simple — Base fixe avec base visible")
clock = pygame.time.Clock()

def to_screen(x, y):
    return int(300 + x * 100), int(200 - y * 100)

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Équation du pendule
    alpha = - (g / l) * math.sin(theta)
    omega += alpha * dt
    theta += omega * dt
    t += dt

    # Enregistrement
    t_hist.append(t)
    theta_hist.append(math.degrees(theta))
    theta_lin = math.radians(15) * math.cos(math.sqrt(g / l) * t)
    theta_lin_hist.append(math.degrees(theta_lin))

    # Dessin du pendule
    x = l * math.sin(theta)
    y = l * math.cos(theta)
    base_pos = to_screen(0, 0)
    bob_pos = to_screen(x, y)

    # Dessiner la base  
    pygame.draw.rect(screen, (100, 100, 100), (base_pos[0] - 20, base_pos[1] - 5, 40, 10))
    pygame.draw.line(screen, (0, 0, 0), base_pos, bob_pos, 3)
    pygame.draw.circle(screen, (0, 0, 255), bob_pos, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# Tracé matplotlib
plt.figure(figsize=(10, 4))
plt.plot(t_hist, theta_hist, label="Simulation numérique")
plt.plot(t_hist, theta_lin_hist, '--', label="Solution analytique linéarisée")
plt.xlabel("Temps (s)")
plt.ylabel("Angle θ (°)")
plt.title("Pendule simple avec base fixe")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()