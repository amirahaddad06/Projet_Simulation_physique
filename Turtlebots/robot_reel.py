import pygame
import matplotlib.pyplot as plt
from TurtleDifferential_moteur import TurtleDifferentialMotor
from ControlPID_vitesse import ControlPID_vitesse

def get_vg_vd(t):
    if t < 3:
        return 0.4, 0.4
    elif t < 6:
        return 0.2, 0.4
    elif t < 9:
        return 0.4, 0.2
    else:
        return 0.0, 0.0

# --- Init Pygame ---
pygame.init()
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot RÉEL (PID) — Avance + Virages")
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

robot = TurtleDifferentialMotor()
dt = 0.01
t = 0.0
scale = 300
origin = (WIDTH // 2, HEIGHT // 2)

pid_g = ControlPID_vitesse(robot.moteur_g, Kp=5.0, Ki=1.0, Kd=0.0)
pid_d = ControlPID_vitesse(robot.moteur_d, Kp=5.0, Ki=1.0, Kd=0.0)

vg_list, vd_list, t_list = [], [], []

running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or t > 10:
            running = False

    vg_ref, vd_ref = get_vg_vd(t)
    R = robot.R
    pid_g.setTarget(vg_ref / R)
    pid_d.setTarget(vd_ref / R)

    Ug = pid_g.getVoltage(dt)
    Ud = pid_d.getVoltage(dt)

    robot.setVoltages(Ug, Ud)
    robot.simule(dt)
    robot.draw(screen, scale=scale, origin=origin)

    vg = robot.moteur_g.getSpeed() * R
    vd = robot.moteur_d.getSpeed() * R

    txt = font.render(f"[RÉEL] vg={vg:.2f} vd={vd:.2f}  Ug={Ug:.1f}V Ud={Ud:.1f}V", True, (200, 80, 0))
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
plt.plot(t_list, vg_list, label="vg réel", color="blue")
plt.plot(t_list, vd_list, label="vd réel", color="red")
plt.xlabel("Temps (s)")
plt.ylabel("Vitesse (m/s)")
plt.title("Robot RÉEL — vitesses des roues")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
