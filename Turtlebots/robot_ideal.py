import pygame
import matplotlib.pyplot as plt
from TurtleDifferential import TurtleDifferential

# Trajectoire : avance + virage gauche + virage droit + stop
def get_vg_vd(t):
    if t < 3:
        return 0.4, 0.4          # ligne droite
    elif t < 6:
        return 0.2, 0.4          # virage à gauche
    elif t < 9:
        return 0.4, 0.2          # virage à droite
    else:
        return 0.0, 0.0          # arrêt

# --- Init Pygame ---
pygame.init()
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot IDÉAL — Avance + Virages")
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

robot = TurtleDifferential()
dt = 0.01
t = 0.0
scale = 300
origin = (WIDTH // 2, HEIGHT // 2)

vg_list, vd_list, t_list = [], [], []

running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or t > 10:
            running = False

    vg, vd = get_vg_vd(t)
    robot.setWheelSpeeds(vg, vd)
    robot.simule(dt)
    robot.draw(screen, scale=scale, origin=origin)

    txt = font.render(f"[IDÉAL] vg={vg:.2f}  vd={vd:.2f}", True, (0, 0, 255))
    screen.blit(txt, (20, 20))

    vg_list.append(vg)
    vd_list.append(vd)
    t_list.append(t)

    pygame.display.flip()
    clock.tick(int(1 / dt))
    t += dt

pygame.quit()

# --- Plot ---
plt.figure()
plt.plot(t_list, vg_list, label="vg (m/s)", color="blue")
plt.plot(t_list, vd_list, label="vd (m/s)", color="red")
plt.xlabel("Temps (s)")
plt.ylabel("Vitesse (m/s)")
plt.title("Robot IDÉAL — vitesses des roues")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
