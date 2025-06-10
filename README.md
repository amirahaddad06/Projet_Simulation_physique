#  Projet de Simulation Physique

Ce projet est réalisé dans le cadre du Master 1 SAR à Sorbonne Université. Il a pour objectif de modéliser, simuler et contrôler divers systèmes dynamiques, notamment des moteurs à courant continu (CC), des robots différentiels, des pendules inversés et des systèmes mécaniques rigides.


##  Fonctionnalités principales

###  Moteur CC (moteur_cc.py)
- Modèle physique avec équations électriques et mécaniques
- Simulation discrète via Euler explicite
- Prise en compte des effets : inductance, frottements, couples extérieurs

###  Régulation PID
- **Vitesse (pid_vitesse.py)** : PID pour stabiliser la vitesse à une consigne
- **Position (pid_position.py)** : Contrôleur PD/PID pour atteindre une position angulaire cible
- Analyse des performances : erreur statique, temps de réponse, saturation de tension

###  TurtleBot (turtlebot.py)
- Simulateur de robot différentiel (2 roues indépendantes)
- Deux modes :
  - Idéal (vitesses imposées)
  - Réaliste (moteurs CC + contrôleurs PID)
- Comparaison trajectoires, effets dynamiques

###  Centrifugeuse (centrifugeuse_simulation.py)
- Particule sur bras tournant avec ressort + amortisseur
- Étude de la stabilité selon la vitesse de rotation
- Visualisation interactive (via clavier)

###  Pendule Inversé (pendule_inverse.py)
- Simulation libre (base fixe vs base mobile)
- Stabilisation automatique via PID + moteur CC
- Interaction clavier pour perturbation

###  Barres rigides 2D (barre2d.py)
- Simulation de solides rigides en 2D
- Application de torseurs, gravité, ressorts
- Système modulaire avec gestion des liaisons mécaniques

##  Interactions utilisateur
- Pygame permet de piloter certains systèmes en temps réel :
  - \[←/→\] : modifier la tension ou perturber un système
  - \[A/Z\] : augmenter ou réduire la vitesse d'entrée
  - Interface graphique interactive

##  Tests et validations
- Comparaison entre réponse théorique et simulation numérique
- Études de l’influence des paramètres (inductance, frottement…)
- Courbes de vitesses, positions, tensions, couples

##  Résultats
- Figures et courbes enregistrées dans le dossier `figures/`
- Réponses typiques : exponentielles, oscillations amorties, erreurs statiques corrigées

##  Dépendances
- Python ≥ 3.7
- `pygame`
- `numpy`
- `matplotlib`

Installation :
```bash
pip install pygame numpy matplotlib


