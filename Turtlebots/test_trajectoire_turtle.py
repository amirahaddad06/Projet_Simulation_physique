import pygame
import math
from TurtleDifferential import TurtleDifferential
from TurtleDifferential_moteur import TurtleDifferentialMotor
from ControlPID_vitesse import ControlPID_vitesse

# ---------- Trajectoire en 8 ----------
def trajectory_8(t, A=0.5, w=0.5):
    x = A * math.sin(w * t)
    y = A * math.sin(w * t) * math.cos(w * t)
    return x, y

# ---------- Calcul des vitesses cibles ----------
def compute_target_wheel_speeds(t, dt, L=0.2):
    x1, y1 = trajectory_8(t)
    x2, y2 = trajectory_8(t + dt)

    dx = (x2 - x1) / dt
    dy = (y2 - y1) / dt
    v = math.sqrt(dx**2 + dy**2)

    theta = math.atan2(dy, dx)

    x0, y0 = trajectory_8(t - dt)
    theta_prev = math.atan2(y1 - y0, x1 - x0)
    omega = (theta - theta_prev) / dt

    vg = v - (L / 2) * omega
    vd = v + (L / 2) * omega
    return vg, vd

# ---------- Init Pygame ----------
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Comparaison suivi de trajectoire – robot idéal vs moteur")
font = pygame.font.SysFont(None, 26)
clock = pygame.time.Clock()

# ---------- Robots ----------
robot_ideal = TurtleDifferential()
robot_motor = TurtleDifferentialMotor()

pid_g = ControlPID_vitesse(robot_motor.moteur_g, Kp=8.0, Ki=3.0)
pid_d = ControlPID_vitesse(robot_motor.moteur_d, Kp=8.0, Ki=3.0)

# ---------- Simulation ----------
dt = 0.02
t = 0.0
origin = (WIDTH // 2, HEIGHT // 2)
scale = 200

running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. Calcule la consigne de vitesses des roues
    vg, vd = compute_target_wheel_speeds(t, dt)

    # 2. Applique directement au robot idéal
    robot_ideal.setWheelSpeeds(vg, vd)
    robot_ideal.simule(dt)

    # 3. Applique la consigne aux PID des moteurs
    pid_g.setTarget(vg)
    pid_d.setTarget(vd)

    # 4. Met à jour les PID → tension moteur
    pid_g.simule(dt)
    pid_d.simule(dt)

    # 5. Met à jour le robot moteur (qui lit ses tensions)
    robot_motor.simule(dt)

    # 6. Trace la trajectoire théorique
    for i in range(500):
        x, y = trajectory_8(i * 0.01)
        px = origin[0] + int(x * scale)
        py = origin[1] - int(y * scale)
        pygame.draw.circle(screen, (220, 220, 220), (px, py), 1)

    # 7. Affiche les deux robots
    robot_ideal.draw(screen, scale=scale, origin=origin)
    robot_motor.draw(screen, scale=scale, origin=origin)

    screen.blit(font.render("Idéal (BLEU)", True, (0, 0, 200)), (20, 20))
    screen.blit(font.render("Moteur (ORANGE)", True, (200, 100, 0)), (20, 50))

    pygame.display.flip()
    clock.tick(int(1 / dt))
    t += dt

pygame.quit()
