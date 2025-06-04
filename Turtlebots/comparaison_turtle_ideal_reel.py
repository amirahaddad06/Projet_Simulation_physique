 

import math
import pygame
import matplotlib.pyplot as plt
from TurtleDifferential import TurtleDifferential
from TurtleDifferential_moteur import TurtleDifferentialMotor
from ControlPID_vitesse import ControlPID_vitesse

# ---------------------------------------------------------------------------
# Trajectoire : ligne droite (v constant) puis virage circulaire rayon Rc
# ---------------------------------------------------------------------------

V_LONG   = 0.3      # vitesse linéaire (m/s)
T_TURN   = 6.0      # instant où commence le virage (s)
R_CURVE  = 0.4      # rayon du virage (m)
OMEGA    = V_LONG / R_CURVE   # vitesse angulaire durant le virage

# pré‑calcul du point de raccord
X_TURN = V_LONG * T_TURN
CENTER_X = X_TURN
CENTER_Y = -R_CURVE            # centre du cercle sous l’axe x


def trajectory_line_curve(t: float):
    """Retourne (x, y) en m pour la trajectoire mixte."""
    if t < T_TURN:
        return V_LONG * t, 0.0
    else:
        theta = OMEGA * (t - T_TURN)  # angle parcouru depuis le début du virage
        # cercle sens horaire autour du centre (CENTER_X, CENTER_Y)
        x = CENTER_X + R_CURVE * math.sin(theta)
        y = CENTER_Y + R_CURVE * (1 - math.cos(theta))
        return x, y


def compute_target_wheel_speeds(t, dt, L=0.2):
    """Renvoie (vg_ref, vd_ref, v_ref) en m/s pour le robot différentiel."""
    x1, y1 = trajectory_line_curve(t)
    x2, y2 = trajectory_line_curve(t + dt)

    dx = (x2 - x1) / dt
    dy = (y2 - y1) / dt
    v  = math.hypot(dx, dy)

    theta = math.atan2(dy, dx)
    x0, y0 = trajectory_line_curve(t - dt)
    theta0 = math.atan2(y1 - y0, x1 - x0)
    omega  = (theta - theta0) / dt

    vg = v - (L/2) * omega
    vd = v + (L/2) * omega
    return vg, vd, v

# ---------------------------------------------------------------------------
# Paramètres généraux
# ---------------------------------------------------------------------------

dt      = 0.005
T_MAX   = 22           # durée sim (s)
R_WHEEL = 0.03

# ---------------------------------------------------------------------------
# Pygame
# ---------------------------------------------------------------------------
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TurtleBot : ligne + virage")
font  = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
origin = (WIDTH//4, HEIGHT//2 + 60)  # décalé à gauche
scale  = 250

# ---------------------------------------------------------------------------
# Robots & PI
# ---------------------------------------------------------------------------
robot_ideal = TurtleDifferential()
robot_motor = TurtleDifferentialMotor()
for m in (robot_motor.moteur_g, robot_motor.moteur_d):
    m.kc = 0.18
    m.f  = 0.02
Kp, Ki = 20.0, 6.0
pid_g = ControlPID_vitesse(robot_motor.moteur_g, Kp, Ki, 0)
pid_d = ControlPID_vitesse(robot_motor.moteur_d, Kp, Ki, 0)

# ---------------------------------------------------------------------------
# Logs
# ---------------------------------------------------------------------------
T, V_IDEAL, V_REAL = [], [], []
VG_REF, VG_REAL, VD_REF, VD_REAL = [], [], [], []
UG, UD = [], []

# ---------------------------------------------------------------------------
# Simulation loop
# ---------------------------------------------------------------------------

t = 0.0
running = True
while running and t < T_MAX:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # ---- consigne ----
    vg_ref_lin, vd_ref_lin, v_ref_lin = compute_target_wheel_speeds(t, dt)

    # ideal
    robot_ideal.setWheelSpeeds(vg_ref_lin, vd_ref_lin)
    robot_ideal.simule(dt)

    # moteur
    pid_g.setTarget(vg_ref_lin / R_WHEEL)
    pid_d.setTarget(vd_ref_lin / R_WHEEL)
    Ug = pid_g.getVoltage(dt)
    Ud = pid_d.getVoltage(dt)
    robot_motor.setVoltages(Ug, Ud)
    robot_motor.simule(dt)

    vg_real_lin = robot_motor.moteur_g.getSpeed() * R_WHEEL
    vd_real_lin = robot_motor.moteur_d.getSpeed() * R_WHEEL
    v_real_lin  = (vg_real_lin + vd_real_lin)/2

    # ---- dessin trajectoire théorique (gris) ----
    for tau in [i*0.1 for i in range(int(T_MAX/0.1)+1)]:
        x, y = trajectory_line_curve(tau)
        px = origin[0] + int(x*scale)
        py = origin[1] - int(y*scale)
        screen.set_at((px, py), (220, 220, 220))

    # robots
    robot_ideal.draw(screen, scale, origin)
    robot_motor.draw(screen, scale, origin)

    # values (affichage minimal)
    info = [f"vg {vg_real_lin:+.3f}  vd {vd_real_lin:+.3f} m/s",
            f"Ug {Ug:+.2f}  Ud {Ud:+.2f} V"]
    for idx, line in enumerate(info):
        screen.blit(font.render(line, True, (0,0,0)), (10, 10+22*idx))

    pygame.display.flip()
    clock.tick(int(1/dt))

    # log
    T.append(t)
    V_IDEAL.append(v_ref_lin)
    V_REAL.append(v_real_lin)
    VG_REF.append(vg_ref_lin); VG_REAL.append(vg_real_lin)
    VD_REF.append(vd_ref_lin); VD_REAL.append(vd_real_lin)
    UG.append(Ug); UD.append(Ud)

    t += dt

pygame.quit()

# ---------------------------------------------------------------------------
# Figures séparées
# ---------------------------------------------------------------------------
plt.figure(figsize=(8,4))
plt.title("Vitesse linéaire moyenne")
plt.plot(T, V_IDEAL, label="Idéale")
plt.plot(T, V_REAL, label="Moteur")
plt.xlabel("Temps (s)")
plt.ylabel("v (m/s)")
plt.grid(); plt.legend(); plt.tight_layout()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9,6), sharex=True)
ax1.plot(T, VG_REF, "--", label="vg_ref")
ax1.plot(T, VG_REAL, label="vg_réel")
ax1.set_ylabel("v_g (m/s)"); ax1.grid(); ax1.legend()
ax2.plot(T, VD_REF, "--", label="vd_ref")
ax2.plot(T, VD_REAL, label="vd_réel")
ax2.set_xlabel("Temps (s)"); ax2.set_ylabel("v_d (m/s)")
ax2.grid(); ax2.legend()
fig.suptitle("Vitesses de roue")
fig.tight_layout(rect=[0,0,1,0.95])

plt.figure(figsize=(8,4))
plt.title("Tensions Ug / Ud")
plt.plot(T, UG, label="Ug", color="red")
plt.plot(T, UD, label="Ud", color="green")
plt.xlabel("Temps (s)"); plt.ylabel("Tension (V)")
plt.grid(); plt.legend(); plt.tight_layout()

plt.show()
