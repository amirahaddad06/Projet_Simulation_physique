import matplotlib.pyplot as plt   

class MoteurCC:
    def __init__(self, R=1.0, L=0.001, kc=0.01, ke=0.01, J=0.01, f=0.1,
                 charge_inertie=0.0, couple_externe=0.0, viscosite_suppl=0.0):
        # --- Caractéristiques physiques ---
        self.R = R                          # Résistance de l'induit
        self.L = L                          # Inductance (sera ignorée car L ≈ 0)
        self.kc = kc                        # Constante de couple
        self.ke = ke                        # Constante de FCEM
        self.J = J + charge_inertie         # Inertie totale (rotor + charge)
        self.f = f + viscosite_suppl        # Frottement visqueux total
        self.couple_externe = couple_externe  # Couple résistant externe

        # --- États internes du moteur ---
        self.Um = 0.0       # Tension appliquée
        self.i = 0.0        # Courant dans l’induit
        self.omega = 0.0    # Vitesse angulaire (rad/s)
        self.theta = 0.0    # Position angulaire (rad)

        # --- Historique pour visualisation ---
        self.historique_temps = [0.0]
        self.historique_omega = [0.0]
        self.historique_i = [0.0]
        self.historique_theta = [0.0]
        self.historique_couple = [0.0]

    def __str__(self):
        # Affichage lisible de l’état actuel
        return f"MoteurCC(omega={self.omega:.3f}, i={self.i:.3f}, theta={self.theta:.3f})"

    def __repr__(self):
        return self.__str__()

    def setVoltage(self, V):
        # Appliquer une tension au moteur
        self.Um = V

    def getPosition(self):
        # Retourner la position actuelle
        return self.theta

    def getSpeed(self):
        # Retourner la vitesse actuelle
        return self.omega

    def getTorque(self):
        # Retourner le couple généré
        return self.kc * self.i

    def getIntensity(self):
        # Retourner le courant électrique
        return self.i

    def simule(self, step):
        # --- Simulation d’un pas de temps ---

        # Calcul de la force contre-électromotrice
        E = self.ke * self.omega

        # Loi d’Ohm : calcul du courant (L ≈ 0)
        self.i = (self.Um - E) / self.R

        # Calcul du couple moteur
        couple_moteur = self.kc * self.i

        # Équation différentielle de la vitesse angulaire
        domega = (couple_moteur - self.f * self.omega - self.couple_externe) / self.J

        # Intégration d’Euler : mise à jour de la vitesse
        self.omega += domega * step

        # Intégration de la position
        self.theta += self.omega * step

        # Enregistrement des données pour affichage
        t = self.historique_temps[-1] + step
        self.historique_temps.append(t)
        self.historique_omega.append(self.omega)
        self.historique_i.append(self.i)
        self.historique_theta.append(self.theta)
        self.historique_couple.append(couple_moteur)

    def plot_v(self):
        # --- Tracé de la vitesse ---
        plt.figure(figsize=(8,5))
        plt.plot(self.historique_temps, self.historique_omega, label='Vitesse (rad/s)')
        plt.xlabel('Temps (s)')
        plt.ylabel('Vitesse ω')
        plt.title('Vitesse du moteur CC au cours du temps')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()


    def plot(self):
        # --- Tracé des courbes ---
        plt.figure(figsize=(10,6))

        # Vitesse
        plt.subplot(2,2,1)
        plt.plot(self.historique_temps, self.historique_omega, label='Vitesse (rad/s)')
        plt.xlabel('Temps (s)')
        plt.ylabel('Vitesse ω')
        plt.legend()

        # Courant
        plt.subplot(2,2,2)
        plt.plot(self.historique_temps, self.historique_i, label='Courant (A)', color='orange')
        plt.xlabel('Temps (s)')
        plt.ylabel('Courant i')
        plt.legend()  

        # Position
        plt.subplot(2,2,3)
        plt.plot(self.historique_temps, self.historique_theta, label='Position (rad)', color='green')
        plt.xlabel('Temps (s)')
        plt.ylabel('Position θ')
        plt.legend()

        # Couple
        plt.subplot(2,2,4)
        plt.plot(self.historique_temps, self.historique_couple, label='Couple (Nm)', color='red')
        plt.xlabel('Temps (s)')
        plt.ylabel('Couple Γ')
        plt.legend()

        plt.tight_layout()
        plt.show()
