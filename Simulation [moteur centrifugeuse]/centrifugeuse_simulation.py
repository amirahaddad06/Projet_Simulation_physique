import pygame
import matplotlib.pyplot as plt
from univers import Univers, SpringDamper
from particule import Particule
from vector3D import Vector3D as V3D
from MoteurCC import MoteurCC
from types import MethodType

#   Univers  
univ = Univers(name="centrifugeuse", step=0.001, dimensions=(60, 60), game=True, gameDimensions=(900, 800), fps=60)

# Moteur CC 
moteur = MoteurCC(kc=0.01, ke=0.01, J=0.01, f=0.02)
moteur.setVoltage(0.0)

#  Particules 
centre = V3D(30, 30, 0)
direction_init = V3D(0, 1, 0)
d_init = 0.1
P_centre = Particule(p0=centre, fix=True, mass=1)
P_mobile = Particule(p0=centre + direction_init * d_init, mass=1.0, color='blue')

#  Ressort + amortisseur 
ressort = SpringDamper(P_centre, P_mobile, k=30.0, c=0.3, l0=0.0)
univ.addParticule(P_centre, P_mobile)
univ.addGenerators(ressort)

#  Enregistrement des données 
omega_list = []
d_list = []

#  Interaction clavier simplifiée 
def interaction(self, events, keys):
    screen = pygame.display.get_surface()

    if keys[pygame.K_a]:  # touche A pour augmenter
        moteur.setVoltage(moteur.Um + 0.05)

    self.simulateAll()
    moteur.simule(self.step)

    theta = moteur.getPosition()
    direction = V3D(0, 1, 0).rotZ(theta)
    r = P_mobile.getPosition() - P_centre.getPosition()
    d = r.mod()

    P_mobile.position[-1] = P_centre.getPosition() + direction * d
    P_mobile.speed[-1] = moteur.getSpeed() * direction * d

    omega_list.append(moteur.getSpeed())
    d_list.append(d)

    # Affichage
    pygame.font.init()
    font = pygame.font.SysFont(None, 22)
    lines = [
        "A : augmenter la tension",
        "ESC : quitter",
        f"Tension U = {moteur.Um:.2f} V",
        f"Vitesse ω = {moteur.getSpeed():.2f} rad/s",
        f"Distance d = {d:.2f} m"
    ]
    for i, line in enumerate(lines):
        txt = font.render(line, True, (0, 0, 0))
        screen.blit(txt, (20, 20 + i * 22))

univ.gameInteraction = MethodType(interaction, univ)

 
univ.simulateRealTime()

 
plt.figure(figsize=(8, 5))
plt.plot(omega_list, d_list, '.', alpha=0.6, label="d(t) vs ω(t)")
plt.xlabel("Vitesse ω (rad/s)")
plt.ylabel("Distance d (m)")
plt.title("Distance radiale vs vitesse ")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

