# Complex Snake Game 🐍

Un jeu Snake avancé avec de nombreuses fonctionnalités complexes créé avec Pygame.

## Fonctionnalités

### Fonctionnalités de Base
- ✅ Mouvement fluide du serpent avec les flèches ou WASD
- ✅ Détection de collision (murs et auto-collision)
- ✅ Animations fluides
- ✅ Système de score avec sauvegarde du meilleur score

### Fonctionnalités Avancées
- 🎮 **3 Niveaux de Difficulté** (Facile, Moyen, Difficile)
- 🍎 **4 Types de Nourriture**:
  - Verte (normale) - +10 points, fait grandir le serpent
  - Dorée (bonus) - +50 points
  - Cyan (boost de vitesse) - +20 points, augmente temporairement la vitesse
  - Violette (ralentissement) - +15 points, ralentit temporairement
- ⚡ **Power-ups**:
  - Invincibilité (orange) - 5 secondes d'immunité aux collisions
  - Multiplicateur de score (jaune) - Double les points pendant 10 secondes
- 🧱 **Obstacles** (sur difficultés moyenne et difficile)
- ❤️ **Système de vies** - 3 vies avant game over
- 📊 **Système de niveaux** - La vitesse augmente tous les 200 points
- ⏸️ **Pause/Reprise** - Appuyez sur P ou ESC
- ✨ **Effets visuels**:
  - Serpent avec dégradé de couleurs
  - Effets de particules lors de la collecte d'objets
  - Yeux animés sur la tête du serpent
  - Grille subtile en arrière-plan

### Interface Utilisateur
- 📋 Menu principal avec sélection de difficulté
- 📊 HUD en jeu (score, meilleur score, vies, niveau)
- ℹ️ Écran d'instructions détaillé
- 🎯 Écran de game over avec option de redémarrage
- 💾 Sauvegarde automatique du meilleur score

## Installation

1. Assurez-vous d'avoir Python 3.7+ installé
2. Installez les dépendances:

```bash
pip install -r requirements.txt
```

Ou installez pygame directement:

```bash
pip install pygame
```

## Lancement du Jeu

```bash
python snake_game.py
```

## Contrôles

### Menu Principal
- **1** - Difficulté Facile
- **2** - Difficulté Moyenne
- **3** - Difficulté Difficile
- **I** - Instructions
- **ESC** - Quitter

### En Jeu
- **Flèches directionnelles** ou **WASD** - Déplacer le serpent
- **P** ou **ESC** - Pause/Reprise
- **ENTER** - Redémarrer (écran game over)

## Types de Nourriture

| Couleur | Type | Points | Effet |
|---------|------|--------|-------|
| 🟢 Vert | Normal | +10 | Fait grandir le serpent |
| 🟡 Doré | Bonus | +50 | Fait grandir le serpent |
| 🔵 Cyan | Speed Boost | +20 | Augmente la vitesse pendant 5s |
| 🟣 Violet | Slow Down | +15 | Ralentit pendant 5s |

## Power-ups

| Couleur | Type | Durée | Effet |
|---------|------|-------|-------|
| 🟠 Orange | Invincibilité | 5s | Immunité aux collisions |
| 🟡 Jaune | Multiplicateur | 10s | Double les points |

## Niveaux de Difficulté

- **Facile**: Vitesse lente, pas d'obstacles
- **Moyen**: Vitesse moyenne, 5 obstacles
- **Difficile**: Vitesse rapide, 10 obstacles

## Système de Progression

- Le niveau augmente tous les 200 points
- La vitesse augmente progressivement avec les niveaux
- Les power-ups apparaissent aléatoirement
- Le meilleur score est sauvegardé automatiquement dans `snake_highscore.json`

## Architecture du Code

Le jeu est structuré en classes orientées objet:

- **Game**: Classe principale gérant la boucle de jeu
- **Snake**: Gestion du serpent et de ses mouvements
- **Food**: Gestion de la nourriture avec différents types
- **PowerUp**: Gestion des power-ups
- **Particle**: Effets visuels de particules
- **Position**: Structure de données pour les coordonnées
- **Enums**: GameState, Difficulty, FoodType, PowerUpType

## Fichiers Générés

- `snake_highscore.json` - Sauvegarde du meilleur score

## Conseils de Jeu

1. 🎯 Collectez la nourriture dorée pour des points bonus
2. ⚡ Utilisez les power-ups stratégiquement
3. 🛡️ L'invincibilité vous donne 3 secondes après avoir perdu une vie
4. 📈 Le multiplicateur de score est très utile pour battre le record
5. 🎮 Commencez en mode facile pour vous familiariser avec les mécaniques

## Améliorations Futures Possibles

- 🎵 Effets sonores et musique de fond
- 🏆 Tableau des meilleurs scores
- 🌈 Thèmes de couleurs personnalisables
- 👥 Mode multijoueur
- 🎨 Skins pour le serpent
- 📱 Support mobile/tactile

## Crédits

Créé avec Python et Pygame
Développé pour démontrer des concepts avancés de programmation de jeux

---

Amusez-vous bien! 🎮🐍
