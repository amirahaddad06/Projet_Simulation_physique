import matplotlib.pyplot as plt

# Paramètres
params = dict(R=1.0, L=0.001, kc=0.01, ke=0.01, J=0.01, f=0.1)
U = 1.0
dt = 0.001
T = 1.5
N = int(T / dt)

# Sans L (L ≈ 0)
from MoteurCC import MoteurCC
m0 = MoteurCC(**params)
m0.setVoltage(U)
t0 = [0.0]
omega0 = [m0.getSpeed()]
for _ in range(N):
    m0.simule(dt)
    t0.append(t0[-1] + dt)
    omega0.append(m0.getSpeed())

# Avec L réel
m1 = MoteurCC_L(**params)
m1.setVoltage(U)
for _ in range(N):
    m1.simule(dt)

# Plot
plt.figure(figsize=(8, 5))
plt.plot(t0, omega0, label="L ≈ 0", linestyle='--')
plt.plot(m1.t, m1.omega_hist, label="L ≠ 0 (réel)", linewidth=2)
plt.xlabel("Temps (s)")
plt.ylabel("Vitesse ω (rad/s)")
plt.title("Comparaison de la réponse du moteur CC (avec vs sans L)")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
