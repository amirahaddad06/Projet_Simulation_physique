class MoteurCC:
    def __init__(self, R=1.0, kc=0.01, ke=0.01, J=0.01, f=0.1):
        self.R = R          # résistance
        self.kc = kc        # constante de couple
        self.ke = ke        # constante de fcem
        self.J = J          # inertie
        self.f = f          # frottements

        self.voltage = 0.0
        self.current = 0.0
        self.omega = 0.0
        self.position = 0.0

    def __str__(self):
        return f"MoteurCC(Ω={self.omega:.3f} rad/s, I={self.current:.3f} A)"

    def __repr__(self):
        return self.__str__()

    def setVoltage(self, V):
        self.voltage = V

    def getSpeed(self):
        return self.omega

    def getTorque(self):
        return self.kc * self.current

    def getIntensity(self):
        return self.current

    def getPosition(self):
        return self.position

    def simule(self, dt):
        # Calcul de la fcem
        E = self.ke * self.omega

        # Courant instantané (L≈0)
        self.current = (self.voltage - E) / self.R

        # Couple moteur
        torque = self.kc * self.current

        # Équation mécanique : J * dΩ/dt = Γ - f*Ω
        domega = (torque - self.f * self.omega) / self.J
        self.omega += domega * dt

        # Intégration de la position
        self.position += self.omega * dt
