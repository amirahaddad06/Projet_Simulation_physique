import matplotlib.pyplot as plt

# Modèle avec L ≈ 0
class MoteurCC:
    def __init__(self, R=1.0, kc=0.01, ke=0.01, J=0.01, f=0.1):
        self.R = R
        self.kc = kc
        self.ke = ke
        self.J = J
        self.f = f
        self.Um = 0.0
        self.i = 0.0
        self.omega = 0.0
        self.theta = 0.0
        self.t_hist = [0.0]
        self.i_hist = [0.0]
        self.omega_hist = [0.0]
        self.torque_hist = [0.0]

    def setVoltage(self, V):
        self.Um = V

    def simule(self, step):
        E = self.ke * self.omega
        self.i = (self.Um - E) / self.R
        torque = self.kc * self.i
        domega = (torque - self.f * self.omega) / self.J
        self.omega += domega * step
        self.theta += self.omega * step
        self.t_hist.append(self.t_hist[-1] + step)
        self.i_hist.append(self.i)
        self.omega_hist.append(self.omega)
        self.torque_hist.append(torque)

# Modèle avec L ≠ 0 (réaliste)
class MoteurCC_L:
    def __init__(self, R=1.0, L=0.5, kc=0.01, ke=0.01, J=0.01, f=0.1):
        self.R = R
        self.L = L
        self.kc = kc
        self.ke = ke
        self.J = J
        self.f = f
        self.Um = 0.0
        self.i = 0.0
        self.omega = 0.0
        self.theta = 0.0
        self.t_hist = [0.0]
        self.i_hist = [0.0]
        self.omega_hist = [0.0]
        self.torque_hist = [0.0]

    def setVoltage(self, V):
        self.Um = V

    def simule(self, step):
        E = self.ke * self.omega
        di = (self.Um - self.R * self.i - E) / self.L
        self.i += di * step
        torque = self.kc * self.i
        domega = (torque - self.f * self.omega) / self.J
        self.omega += domega * step
        self.theta += self.omega * step
        self.t_hist.append(self.t_hist[-1] + step)
        self.i_hist.append(self.i)
        self.omega_hist.append(self.omega)
        self.torque_hist.append(torque)

# Paramètres de simulation
R, kc, ke, J, f = 1.0, 0.01, 0.01, 0.01, 0.1
L_real = 0.1  # inductance  
U0 = 1.0
dt = 0.001
T = 1.5
N = int(T / dt)

# Initialisation
m0 = MoteurCC(R=R, kc=kc, ke=ke, J=J, f=f)
mL = MoteurCC_L(R=R, L=L_real, kc=kc, ke=ke, J=J, f=f)
m0.setVoltage(U0)
mL.setVoltage(U0)

for _ in range(N):
    m0.simule(dt)
    mL.simule(dt)

# Tracé regroupé
plt.figure(figsize=(12, 8))
plt.suptitle("Comparaison Moteur CC avec L ≈ 0 vs L = 0.1", fontsize=14)

plt.subplot(3,1,1)
plt.plot(m0.t_hist, m0.omega_hist, '--', label="ω(t) L ≈ 0")
plt.plot(mL.t_hist, mL.omega_hist, '-', label="ω(t) L = 0.1")
plt.ylabel("Vitesse ω (rad/s)")
plt.grid(True)
plt.legend()

plt.subplot(3,1,2)
plt.plot(m0.t_hist, m0.i_hist, '--', label="i(t) L ≈ 0")
plt.plot(mL.t_hist, mL.i_hist, '-', label="i(t) L = 0.1")
plt.ylabel("Courant i (A)")
plt.grid(True)
plt.legend()

plt.subplot(3,1,3)
plt.plot(m0.t_hist, m0.torque_hist, '--', label="Γ(t) L ≈ 0")
plt.plot(mL.t_hist, mL.torque_hist, '-', label="Γ(t) L = 0.1")
plt.xlabel("Temps (s)")
plt.ylabel("Couple Γ (Nm)")
plt.grid(True)
plt.legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
