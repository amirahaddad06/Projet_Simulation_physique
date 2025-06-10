import matplotlib.pyplot as plt 

class ControlPID_vitesse:
    def __init__(self, moteur, Kp=1.0, Ki=0.0, Kd=0.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.moteur = moteur
        self.target_speed = 0.0
        self.integral = 0.0
        self.prev_error = 0.0
        self.voltages = []
        self.speeds = []

    def __str__(self):
        return f"ControlPID_vitesse(Kp={self.Kp}, Ki={self.Ki}, Kd={self.Kd}, target={self.target_speed})"

    def __repr__(self):
        return self.__str__()

    def setTarget(self, vitesse):
        self.target_speed = vitesse    # la consigne 

    def getVoltage(self, dt=0.01):
        error = self.target_speed - self.moteur.getSpeed()    
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        voltage = self.Kp * error + self.Ki * self.integral + self.Kd * derivative 
        return voltage   # tension 

    def simule(self, step):
        V = self.getVoltage(step)
        self.moteur.setVoltage(V)
        self.moteur.simule(step)
        self.voltages.append(V)
        self.speeds.append(self.moteur.getSpeed())

    def plot(self):
        time = [i * 0.01 for i in range(len(self.speeds))]

        plt.figure(figsize=(10, 5))
        plt.subplot(2,1,1)
        plt.plot(time, self.speeds, label="Vitesse")
        plt.ylabel("Vitesse (rad/s)")
        plt.legend()
        plt.grid(True)

        plt.subplot(2,1,2)
        plt.plot(time, self.voltages, label="Tension", color='orange')
        plt.ylabel("Tension (V)")
        plt.xlabel("Temps (s)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
