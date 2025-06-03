import matplotlib.pyplot as plt
from ControlPID_vitesse import ControlPID_vitesse
from MoteurCC import MoteurCC  # classe moteur déjà définie ailleurs

def validation_PID(Kp=1.0, Ki=0.0, title="Correcteur PID"):
    # Définir les paramètres de simulation
    step = 0.01      # pas de temps (en secondes)
    t = 0            # temps initial
    T_end = 8.0      # durée totale de la simulation

    # Création des deux moteurs :
    # m_bo = moteur en boucle ouverte (sans régulation)
    # m_bf = moteur en boucle fermée (avec PID)
    m_bo = MoteurCC()
    m_bf = MoteurCC()

    # Création du contrôleur PID appliqué à m_bf
    control = ControlPID_vitesse(m_bf, Kp, Ki, 0)

    # Initialisation des listes pour stocker les résultats
    t_hist = [0]                      # temps
    omega_bo = [m_bo.getSpeed()]     # vitesse boucle ouverte
    omega_bf = [m_bf.getSpeed()]     # vitesse boucle fermée
    voltage_pid = [m_bf.Um]          # tension envoyée par le PID

    # Boucle de simulation jusqu’à T_end
    while t < T_end:
        t += step
        t_hist.append(t)

        # Boucle ouverte : on fixe une tension constante
        m_bo.setVoltage(1 / Kp)  # permet d’avoir même vitesse cible sans régulation
        m_bo.simule(step)

        # Boucle fermée : on fixe la vitesse cible à 1 rad/s
        control.setTarget(1)
        control.simule(step)

        # On enregistre les valeurs pour tracer plus tard
        omega_bo.append(m_bo.getSpeed())
        omega_bf.append(m_bf.getSpeed())
        voltage_pid.append(m_bf.Um)

    # --- Tracés des courbes ---
    plt.figure(figsize=(10, 6))

    # Courbe de vitesse comparée
    plt.subplot(2, 1, 1)
    plt.plot(t_hist, omega_bo, '--', label="Boucle ouverte")
    plt.plot(t_hist, omega_bf, '-', label="Boucle fermée (PID)")
    plt.axhline(y=1, color='gray', linestyle=':', label="Consigne")
    plt.ylabel("Vitesse ω (rad/s)")
    plt.title(title)
    plt.grid(True)
    plt.legend()

    # Courbe de la tension envoyée par le PID
    plt.subplot(2, 1, 2)
    plt.plot(t_hist, voltage_pid, color='orange', label="Tension U_m(t)")
    plt.xlabel("Temps (s)")
    plt.ylabel("Tension (V)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

# Tests avec P seul puis PI
validation_PID(Kp=1.0, Ki=0.0, title="Réponse avec correcteur P seul")
validation_PID(Kp=1.0, Ki=2.0, title="Réponse avec correcteur PI")
