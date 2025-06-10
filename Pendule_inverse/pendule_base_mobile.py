import pygame
import math
import matplotlib.pyplot as plt

# Constantes physiques
g = 9.81
l = 1.0
m = 1.0
theta =   math.radians(20)  # pendule inversé légèrement perturbé
omega = 0.0

# Base mobile libre
x_base = 0.0
v_base = 0.0
a_base = 0.0
k_friction = 0.3  # frottement visqueux

dt = 0.01
t = 0.0

# Historique
t_hist = []
theta_hist = []
x_base_hist = []

# Pygame init
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Pendule inversé — Base mobile libre ")
clock = pygame.time.Clock()

def to_screen(x, y):
    return int(300 + x * 100), int(300 - y * 100)

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calcul des forces sur la base : composante horizontale du pendule
    a_base = (m * l * omega**2 * math.sin(theta) - m * g * math.cos(theta) * math.sin(theta)) / m
    a_base -= k_friction * v_base

    v_base += a_base * dt
    x_base += v_base * dt

    # Dynamique du pendule
    alpha = - (g / l) * math.sin(theta) + (a_base / l) * math.cos(theta)
    omega += alpha * dt
    theta += omega * dt
    t += dt

    # Enregistrement
    t_hist.append(t)
    theta_hist.append(math.degrees(theta))
    x_base_hist.append(x_base)

    # Affichage
    pend_x = x_base + l * math.sin(theta)
    pend_y = l * math.cos(theta)
    base_pos = to_screen(x_base, 0)
    bob_pos = to_screen(pend_x, pend_y)

    pygame.draw.rect(screen, (100, 100, 100), (base_pos[0] - 20, base_pos[1] - 5, 40, 10))
    pygame.draw.line(screen, (0, 0, 0), base_pos, bob_pos, 3)
    pygame.draw.circle(screen, (255, 0, 0), bob_pos, 8)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# Affichage matplotlib
plt.figure(figsize=(10, 4))
plt.subplot(2, 1, 1)
plt.plot(t_hist, theta_hist, label="θ(t)")
plt.ylabel("Angle (°)")
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(t_hist, x_base_hist, label="x_base(t)")
plt.xlabel("Temps (s)")
plt.ylabel("Position base (m)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
