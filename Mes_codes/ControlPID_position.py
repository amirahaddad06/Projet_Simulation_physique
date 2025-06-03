import matplotlib.pyplot as plt

class ControlPID_position:
    def __init__(self, moteur, Kp=1.0, Kd=0.0):
        self.moteur = moteur          # moteur à contrôler
        self.Kp = Kp                  # gain proportionnel
        self.Kd = Kd                  # gain dérivateur
        self.target = 0.0            # position cible (θ)
        self.prev_error = 0.0        # pour le dérivé
        self.voltages = []           # historique des tensions appliquées
        self.positions = []          # historique des positions θ(t)
        self.times = [0.0]           # historique du temps

    def setTarget(self, position):
        self.target = position  # position désirée (rad)

    def simule(self, step):
        # Calcul de l'erreur de position
        error = self.target - self.moteur.getPosition()
        # Calcul du terme dérivé
        derivative = (error - self.prev_error) / step
        self.prev_error = error
        # Calcul de la tension avec PD
        voltage = self.Kp * error + self.Kd * derivative
        # Appliquer la tension et simuler le moteur
        self.moteur.setVoltage(voltage)
        self.moteur.simule(step)
        # Enregistrer les valeurs
        self.voltages.append(voltage)
        self.positions.append(self.moteur.getPosition())
        self.times.append(self.times[-1] + step)

    def plot(self):
        # Tracé position et tension
        plt.figure(figsize=(10, 5))

        # Position angulaire θ(t)
        plt.subplot(2, 1, 1)
        plt.plot(self.times[1:], self.positions, label="Position θ(t)")
        plt.axhline(y=self.target, color='gray', linestyle='--', label="Consigne")
        plt.ylabel("Position (rad)")
        plt.legend()
        plt.grid(True)

        # Tension Um(t)
        plt.subplot(2, 1, 2)
        plt.plot(self.times[1:], self.voltages, label="Tension U_m(t)", color="orange")
        plt.xlabel("Temps (s)")
        plt.ylabel("Tension (V)")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()
