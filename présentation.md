# HOTLINE BZH

*Top-down Shooter 2D · Projet NSI · Concours*

*Réalisé à 99 % par 4 lycéens — IA utilisée uniquement en support (précisé dans le code)*

---

##  Présentation du projet

Hotline BZH est un jeu vidéo top-down shooter 2D développé de zéro par une équipe de 4 lycéens dans le cadre d'un concours NSI. Le jeu tourne sous Python avec Ursina Engine. Aucun asset externe : sprites, map, sons et code sont entièrement originaux.

>  **Transparence IA** — Le recours à l'IA (Claude / ChatGPT) a été limité à la résolution de bugs ponctuels.
>
> Chaque ligne assistée est signalée par un commentaire `#AI` dans le code source.
>
> L'architecture, la logique de jeu et tous les assets sont à 100 % humains.

---

##  Gameplay

### Contrôles

- **ZQSD / WASD** — Déplacement en 4 directions
- **Souris** — Visée libre (le sprite tourne vers le curseur en temps réel)
- **Clic gauche** — Tir au fusil à pompe (raycast instantané)
- **Clic droit maintenu** — Zoom de visée (réduction du FOV caméra)
- **Shift gauche** — Sprint (consomme la barre de stamina)

### Mécaniques clés

- **Tir raycast** — collision pixel-perfect, effet d'impact visuel (`shot_vfx`)
- **Stamina** — barre qui se vide en sprintant, se régénère au repos
- **Sang procédural** — 5 textures de flaques tirées aléatoirement à chaque mort
- **Son de pas dans le sang** — déclenché si le joueur passe sur une flaque
- **Vagues infinies** — respawn automatique dès que tous les ennemis sont éliminés

---

##  Fonctionnement des fonctions principales

### `Player_update()` — Boucle joueur

Appelée à chaque frame dans `update()`. Elle orchestre toutes les sous-fonctions du joueur :

```
① Player_movement()  →  ② Player_look_at_cursor()  →  ③ Player_stamina()  →  FIN frame suivante
   Déplace le joueur       Oriente le sprite vers          Gère la barre de
   selon les touches       la position de la souris        stamina (regen / consomme)
   appuyées
```

#### ① `Player_movement()` — Détail

Pour chaque touche de déplacement maintenue (a/d/w/s) :

```
Touche maintenue ?  →  can_move() ? 2 raycasts diagonaux  →  Oui → déplace position += direction × speed × dt
                                                            →  Non → blocage mur
```

>  `can_move()` lance 2 raycasts légèrement décalés (±0.9 en perpendiculaire) pour éviter que le joueur se bloque sur les coins de murs. Si l'un des deux touche un collider → blocage.

#### ② `Player_look_at_cursor()`

Appelle `look_at_2d(mouse.position + Player.position)` — Ursina calcule l'angle entre le sprite et le curseur, puis applique une rotation sur l'axe Z. Le sprite pointe toujours vers la souris.

#### ③ `Player_stamina()`

```
stamina < max ? → stamina += dt (régénération passive)
running ET stamina > 0 ? → stamina -= 3×dt (consommation)
stamina < 0 ? → speed = init_speed (fin du sprint)
```

---

### `attaque()` — IA des ennemis

Appelée à chaque frame. Boucle sur tous les ennemis vivants et gère deux comportements selon la distance au joueur :

```
Calculer distance joueur→ennemi  →  distance < 5 ?
                                     OUI → POURSUITE : look_at_2d(joueur) + can_move() → avancer
                                     NON → PATROUILLE : raycast devant, si mur → tourner 90°, sinon → avancer
```

**Mode Poursuite (distance < 5)**

- `look_at_2d(Player.position)` — l'ennemi tourne vers le joueur
- `can_move()` vérifie qu'il n'y a pas de mur entre eux
- Si passage libre → `position += dir_normalisé × 5 × dt`

**Mode Patrouille (distance ≥ 5)**

- Raycast de 0.6 unités vers l'avant (`ent.up` = direction du sprite)
- Si obstacle détecté → `rotation_z -= 90°` (tourne à droite)
- Sinon → avance à vitesse 4 dans la direction courante

>  `normalized()` convertit le vecteur de direction en vecteur unitaire (longueur = 1) pour que la vitesse de déplacement soit constante quelle que soit la distance.

---

### `ennemie_shoot()` — Tir ennemi sur le joueur

Boucle sur les ennemis vivants. Pour chacun, lance un raycast en direction du joueur sur 2 unités :

```
Vecteur ennemi → joueur normalisé  →  raycast() distance=2 ignore=[ennemi]
  →  touche Player ? Oui → joueur mort + son + sang + destroy
  →  Non → rien ne se passe
```

---

### `input('left mouse down')` — Tir joueur

Déclenché par le clic gauche dans la fonction `input(key)` :

```
raycast() Player.position → Player.up (droit devant)
  →  shot_vfx() à point d'impact (entité flash détruite en 0.05s)
  →  hit.entity == ennemi ? Oui → mort ennemi + sang + son
  →  nombre_ennemi -= 1 + nouvel appel init ?
```

---

##  Architecture technique

### Stack

- **Python 3 + Ursina Engine** — moteur 2D/3D open-source
- **Système de raycasts** — tous les tirs et collisions de mouvement
- **Audio** : objets `Audio` Ursina pré-chargés, activés à la demande
- **Assets 100 % originaux** : sprites pixel-art, map, effets sonores

### Installation

```bash
# Installer la dépendance
pip install ursina

# Lancer le jeu
python main.py
```

### Structure du projet

- `main.py` — code source complet (commentaires `#AI` sur les lignes assistées)
- `assets/` — sprites PNG (joueur, ennemi, sang×5, shot_vfx, stamina, world)
- `song/` — effets sonores MP3 (tirs, rechargement, impact, pas, ambient)

---

##  L'équipe

*Projet réalisé en totale autonomie. L'IA n'a servi qu'à débloquer des erreurs techniques précises, signalées dans le code.*

| Prénom | Rôle | Contributions détaillées |
|---|---|---|
| **Youn** | Gameplay & Audio | IA ennemis (attaque, patrouille, tir), système audio (sons de tir, impact, sang), flaques de sang procédurales, game over, spawn des vagues |
| **Lilian** | Programmeur principal | Moteur du jeu, caméra dynamique, déplacements joueur, système de tir (raycast), collisions, interface stamina, système de contrôles |
| **Membre 3** | Assets visuels & Map | Création des sprites (joueur, ennemis, sang, VFX), conception de la map et placement des collisions |
| **Membre 4** | Tests & Équilibrage | Playtests, rapports de bugs, équilibrage des vitesses / portées, vérification des assets |

---

*Hotline BZH · Projet NSI Concours · Équipe de 4 lycéens · Tous droits réservés*
