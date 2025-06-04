import pygame
import math
import csv
import matplotlib.pyplot as plt
from TurtleDifferential import TurtleDifferential
from TurtleDifferential_moteur import TurtleDifferentialMotor
from ControlPID_vitesse import ControlPID_vitesse

# ---------- Trajectoire droite ----------
def trajectory_line(t, v=0.5):
    x = v * t
    y = 0
    return x, y

# ---------- Calcul des vitesses cibles ----------
def compute_target_wheel_speeds(t, dt, L=0.2):
    x1, y1 = trajectory_line(t)
    x2, y2 = trajectory_line(t + dt)

    dx = (x2 - x1) / dt
    dy = (y2 - y1) / dt
    v = math.sqrt(dx**2 + dy**2)

    omega = 0.0
    vg = v - (L / 2) * omega
    vd = v + (L / 2) * omega
    return vg, vd

# ---------- Init Pygame ----------
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Comparaison : robot idéal vs robot moteur (avec tension)")
font = pygame.font.SysFont(None, 26)
clock = pygame.time.Clock()

# ---------- Robots ----------
robot_ideal = TurtleDifferential()
robot_motor = TurtleDifferentialMotor()

#  PID plus agressif
pid_g = ControlPID_vitesse(robot_motor.moteur_g, Kp=20.0, Ki=10.0)
pid_d = ControlPID_vitesse(robot_motor.moteur_d, Kp=20.0, Ki=10.0)

# ---------- Simulation ----------
dt = 0.02
t = 0.0
origin = (WIDTH // 2, HEIGHT // 2)
scale = 200

# Stockage
temps, vitesse_ideal, vitesse_moteur = [], [], []
tension_g, tension_d = [], []

running = True
while running and t < 5:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. Vitesse cible
    vg, vd = compute_target_wheel_speeds(t, dt)

    # 2. Idéal
    robot_ideal.setWheelSpeeds(vg, vd)
    robot_ideal.simule(dt)
    v_id = (vg + vd) / 2

    # 3. PID moteur
    pid_g.setTarget(vg)
    pid_d.setTarget(vd)
    Ug = pid_g.getVoltage(dt)
    Ud = pid_d.getVoltage(dt)
    pid_g.simule(dt)
    pid_d.simule(dt)
    robot_motor.simule(dt)

    v_m = (robot_motor.moteur_g.getSpeed() + robot_motor.moteur_d.getSpeed()) * robot_motor.R / 2

    # 4. Stockage
    temps.append(t)
    vitesse_ideal.append(v_id)
    vitesse_moteur.append(v_m)
    tension_g.append(Ug)
    tension_d.append(Ud)

    # 5. Affichage
    robot_ideal.draw(screen, scale=scale, origin=origin)
    robot_motor.draw(screen, scale=scale, origin=origin)

    screen.blit(font.render("Idéal (BLEU)", True, (0, 0, 200)), (20, 20))
    screen.blit(font.render("Moteur (ORANGE)", True, (200, 100, 0)), (20, 50))

    pygame.display.flip()
    clock.tick(int(1 / dt))
    t += dt

pygame.quit()

# ---------- Graphique matplotlib ----------
plt.figure(figsize=(10, 6))

# Courbe vitesse
plt.subplot(2, 1, 1)
plt.plot(temps, vitesse_ideal, label="Vitesse Idéal (m/s)", color="blue")
plt.plot(temps, vitesse_moteur, label="Vitesse Moteur (m/s)", color="orange", linestyle='--')
plt.ylabel("Vitesse (m/s)")
plt.title("Comparaison des vitesses")
plt.grid(True)
plt.legend()

# Courbe tension
plt.subplot(2, 1, 2)
plt.plot(temps, tension_g, label="Tension moteur gauche (V)", color="red")
plt.plot(temps, tension_d, label="Tension moteur droite (V)", color="green")
plt.xlabel("Temps (s)")
plt.ylabel("Tension (V)")
plt.title("Tension appliquée aux moteurs")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
