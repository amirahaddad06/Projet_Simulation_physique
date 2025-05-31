from MoteurCC import MoteurCC 
from ControlPID_vitesse import ControlPID_vitesse

# Création du moteur et du contrôleur PID
moteur = MoteurCC()
control = ControlPID_vitesse(moteur, Kp=2.0, Ki=1.0, Kd=0.1)

# Configuration de la consigne
control.setTarget(1.0)  # 1 rad/s

# Simulation
t = 0
dt = 0.01
while t < 2.0:
    control.simule(dt)
    t += dt

# Affichage des résultats
control.plot()
