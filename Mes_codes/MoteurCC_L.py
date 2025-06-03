class MoteurCC_L:
    def __init__(self, R=1.0, L=0.001, kc=0.01, ke=0.01, J=0.01, f=0.1,
                 charge=0.0, couple_externe=0.0, viscosite_suppl=0.0):
        # Paramètres physiques
        self.R = R
        self.L = L
        self.kc = kc
        self.ke = ke
        self.J = J + charge
        self.f = f + viscosite_suppl
        self.couple_externe = couple_externe

        # États dynamiques
        self.Um = 0.0        # tension
        self.i = 0.0         # courant
        self.omega = 0.0     # vitesse
        self.theta = 0.0     # position

        # Historique pour courbes
        self.t_hist = [0.0]
        self.i_hist = [0.0]
        self.omega_hist = [0.0]
        self.theta_hist = [0.0]
        self.torque_hist = [0.0]

    def __str__(self):
        return f"MoteurCC_L(omega={self.omega:.3f}, i={self.i:.3f}, theta={self.theta:.3f})"

    def __repr__(self):
        return self.__str__()

    def setVoltage(self, V):
        self.Um = V

    def getSpeed(self):
        return self.omega

    def getPosition(self):
        return self.theta

    def getTorque(self):
        return self.kc * self.i

    def getIntensity(self):
        return self.i

    def simule(self, step):
        # FCEM
        E = self.ke * self.omega
        # Intégration du courant via L.di/dt
        di = (self.Um - self.R * self.i - E) / self.L
        self.i += di * step
        # Couple moteur
        torque = self.kc * self.i
        # Équation mécanique
        domega = (torque - self.f * self.omega - self.couple_externe) / self.J
        self.omega += domega * step
        self.theta += self.omega * step

        # Enregistrer pour tracé
        t = self.t_hist[-1] + step
        self.t_hist.append(t)
        self.i_hist.append(self.i)
        self.omega_hist.append(self.omega)
        self.theta_hist.append(self.theta)
        self.torque_hist.append(torque)
    
     