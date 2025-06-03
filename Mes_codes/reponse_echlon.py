
from MoteurCC import MoteurCC

# Création du moteur avec les paramètres donnés
m = MoteurCC(
    R=1.0,
    L=0.001,  # sera ignorée dans le modèle
    kc=0.01,
    ke=0.01,
    J=0.01,
    f=0.1
)

# Configuration de la simulation
step = 0.01
temps_total = 2.0
n_steps = int(temps_total / step)

# Appliquer un échelon de tension à 1V
m.setVoltage(1.0)

# Boucle de simulation
for i in range(n_steps):
    m.simule(step)

# Affichage des résultats
m.plot_v()
