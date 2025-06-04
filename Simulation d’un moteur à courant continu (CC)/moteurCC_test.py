import matplotlib.pyplot as plt
from MoteurCC import MoteurCC

# --- Créer un moteur avec des paramètres réalistes ---
m = MoteurCC(
    R=1.0,       # résistance (ohms)
    L=0.0,       # négligé (optionnel)
    kc=0.1,      # constante couple (↗ plus = plus de puissance)
    ke=0.01,     # constante FEM (↘ plus = démarre vite)
    J=0.01,      # inertie
    f=0.01       # frottement (↘ plus = plus fluide)
)

# --- Appliquer une tension constante ---
m.setVoltage(6.0)

# --- Simulation dynamique ---
omegas = []
intensites = []
times = []
dt = 0.01
t = 0.0
for _ in range(500):
    m.simule(dt)
    omegas.append(m.getSpeed())
    intensites.append(m.getIntensity())
    times.append(t)
    t += dt

# --- Affichage des résultats ---
plt.figure(figsize=(10, 5))

plt.subplot(2, 1, 1)
plt.plot(times, omegas, label="Vitesse (rad/s)")
plt.ylabel("Vitesse ω")
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(times, intensites, label="Courant (A)", color="orange")
plt.xlabel("Temps (s)")
plt.ylabel("Courant i")
plt.grid(True)
plt.legend()

plt.suptitle("Réponse du moteur CC à 6 V")
plt.tight_layout()
plt.show()
