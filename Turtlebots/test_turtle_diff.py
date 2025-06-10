import pygame
import math
from TurtleDifferential import TurtleDifferential   

# Pygame init
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TurtleBot – Contrôle directionnel des roues")
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

# Robot
robot = TurtleDifferential()
dt = 0.01
origin = (WIDTH // 2, HEIGHT // 2)
vg, vd = 0.0, 0.0
delta_v = 0.01

running = True
while running:
    screen.fill((250, 250, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #  Contrôle clavier flèches
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        vg += delta_v
        vd += delta_v
    if keys[pygame.K_DOWN]:
        vg -= delta_v
        vd -= delta_v
    if keys[pygame.K_LEFT]:
        vg -= delta_v
        vd += delta_v
    if keys[pygame.K_RIGHT]:
        vg += delta_v
        vd -= delta_v
    if keys[pygame.K_SPACE]:
        vg = vd = 0.0

    # Limites
    vg = max(-0.3, min(0.3, vg))
    vd = max(-0.3, min(0.3, vd))

    # Appliquer au robot
    robot.setWheelSpeeds(vg, vd)
    robot.simule(dt)
    robot.draw(screen, scale=100, origin=origin)

    # Affichage
    txt = font.render(f"vg = {vg:.2f} m/s     vd = {vd:.2f} m/s", True, (0, 0, 0))
    screen.blit(txt, (20, 20))

    pygame.display.flip()
    clock.tick(int(1 / dt))

pygame.quit()
