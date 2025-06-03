
import matplotlib.pyplot as plt
from MoteurCC import MoteurCC
from ControlPID_position import ControlPID_position

def validation_PID_position(Kp=1.0, Kd=0.0, target=1.5, title="Commande en position PID"):
    # Paramètres de simulation
    step = 0.01
    T_end = 3.0
    t = 0

    # Initialisation du moteur et du contrôleur
    moteur = MoteurCC()
    controleur = ControlPID_position(moteur, Kp=Kp, Kd=Kd)
    controleur.setTarget(target)

    # Simulation
    while t < T_end:
        t += step
        controleur.simule(step)

    # Tracé des courbes
    controleur.plot()

# Exemples de validation
validation_PID_position(Kp=5.0, Kd=0.0, target=1.5, title="Position : correcteur P seul")
validation_PID_position(Kp=5.0, Kd=1.0, target=1.5, title="Position : correcteur PD")
