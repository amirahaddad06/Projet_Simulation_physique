import pygame
from TurtleDifferential_Moteur import TurtleDifferentialMotor

# --- Pygame init ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TurtleBot – Contrôle par tension moteur")
font = pygame.font.SysFont(None, 26)
clock = pygame.time.Clock()

# --- Robot moteur ---
robot = TurtleDifferentialMotor()
dt = 0.02
origin = (WIDTH // 2, HEIGHT // 2)

Ug = 0.0  # tension moteur gauche
Ud = 0.0  # tension moteur droit
dU = 0.2  # pas d'incrément
U_MAX = 12.0

running = True
while running:
    screen.fill((240, 240, 240))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 🎮 Contrôle clavier
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        Ug += dU
        Ud += dU
    if keys[pygame.K_DOWN]:
        Ug -= dU
        Ud -= dU
    if keys[pygame.K_LEFT]:
        Ug -= dU
        Ud += dU
    if keys[pygame.K_RIGHT]:
        Ug += dU
        Ud -= dU
    if keys[pygame.K_SPACE]:
        Ug = Ud = 0.0

    # Saturation tension
    Ug = max(-U_MAX, min(U_MAX, Ug))
    Ud = max(-U_MAX, min(U_MAX, Ud))

    # Appliquer
    robot.setVoltages(Ug, Ud)
    robot.simule(dt)
    robot.draw(screen, scale=100, origin=origin)

    # Affichage info
    txt = font.render(f"Ug = {Ug:.1f} V    Ud = {Ud:.1f} V", True, (0, 0, 0))
    screen.blit(txt, (20, 20))

    w_g = robot.moteur_g.getSpeed() * robot.R
    w_d = robot.moteur_d.getSpeed() * robot.R
    txt2 = font.render(f"vg = {w_g:.2f} m/s   vd = {w_d:.2f} m/s", True, (50, 50, 0))
    screen.blit(txt2, (20, 50))

    pygame.display.flip()
    clock.tick(int(1 / dt))

pygame.quit()
