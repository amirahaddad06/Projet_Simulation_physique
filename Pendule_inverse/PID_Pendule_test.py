import pygame, math
from MoteurCC import MoteurCC
from ControlPID_Pendule import ControlPID_Pendule

#  Constantes physiques et de simulation 
g, L, dt = 9.81, 1.0, 0.0001
pixels_per_m = 200
UM_MAX = 12.0
RESTIT = 0.85
MARGE = 60

# État initial 
theta = math.radians(2)  # pendule presque vertical  
omega = 0.0
moteur = MoteurCC()
v_prev = 0.0
pid = ControlPID_Pendule(Kp=250, Kd=20, Ki=2, setpoint=0.0)   

  
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendule inversé — PID + moteur CC") 
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
 # Dessin pendule + base  
def draw_pendulum(theta, x_pix):
    origin = (x_pix, HEIGHT // 2)
    xt = origin[0] + int(L * pixels_per_m * math.sin(theta))
    yt = origin[1] - int(L * pixels_per_m * math.cos(theta))
    pygame.draw.line(screen, (0, 0, 0), origin, (xt, yt), 5)
    pygame.draw.circle(screen, (200, 0, 0), (xt, yt), 10)
    pygame.draw.rect(screen, (0, 100, 255), (x_pix - 35, origin[1] - 12, 70, 24))

 
running = True
t = 0.0
while running:
    screen.fill((240, 240, 240))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

     
    x_b = moteur.getPosition()
    v_b = moteur.getSpeed()

    #  Erreur par rapport à la verticale
    theta_eff = theta - math.pi

    #  Commande PID → tension moteur
    Um = pid.compute(theta_eff, omega, dt)
    Um = max(-UM_MAX, min(UM_MAX, Um))
    moteur.setVoltage(Um)
    moteur.simule(dt)

    #  Dynamique du pendule
    a_b = (moteur.getSpeed() - v_prev) / dt
    v_prev = moteur.getSpeed()
    alpha = (g / L) * math.sin(theta) + (a_b / L) * math.cos(theta) - 0.15 * omega
    omega += alpha * dt
    theta += omega * dt

    #  Rebond aux bords
    x_pix = WIDTH // 2 + int(x_b * pixels_per_m)
    if x_pix < MARGE:
        x_pix = MARGE
        x_b = (x_pix - WIDTH // 2) / pixels_per_m
        moteur._theta = x_b
        moteur.omega *= -RESTIT
        if abs(moteur.omega) < 0.2:
            moteur.omega = 2.0
    elif x_pix > WIDTH - MARGE:
        x_pix = WIDTH - MARGE
        x_b = (x_pix - WIDTH // 2) / pixels_per_m
        moteur._theta = x_b
        moteur.omega *= -RESTIT
        if abs(moteur.omega) < 0.2:
            moteur.omega = -2.0

    # === Affichage
    draw_pendulum(theta, x_pix)
    ang = math.degrees(theta_eff)
    screen.blit(font.render(f"θ={ang:+6.1f}°  Um={Um:+6.2f} V  x={x_b:+.2f} m", True, (0, 0, 0)), (10, 10))
    screen.blit(font.render("Stabilisation automatique avec PID", True, (50, 50, 50)), (10, 35))

    pygame.display.flip()
    clock.tick(120)
    t += dt

pygame.quit()
