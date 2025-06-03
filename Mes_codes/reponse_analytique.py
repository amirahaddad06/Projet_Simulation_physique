import numpy as np
import matplotlib.pyplot as plt

# Paramètres physiques du moteur
R = 1.0          # résistance [ohms]
kc = 0.01        # constante de couple [N.m/A]
ke = 0.01        # constante de FCEM [V.s/rad]
J = 0.01         # inertie [kg.m²]
f = 0.1          # frottement visqueux [N.m.s]
U0 = 1.0         # échelon de tension [V]

# Calcul du gain statique K et de la constante de temps τ
K = kc / (f + (kc * ke) / R)
tau = J / (f + (kc * ke) / R)

# Temps de simulation
T = 2.0
dt = 0.01
t = np.arange(0, T + dt, dt)

# Réponse analytique
omega = K * U0 * (1 - np.exp(-t / tau))

# Affichage
plt.figure(figsize=(8,5))
plt.plot(t, omega, label="Réponse analytique")
plt.xlabel("Temps (s)")
plt.ylabel("Vitesse ω (rad/s)")
plt.title("Réponse analytique à un échelon de tension (Moteur CC)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
