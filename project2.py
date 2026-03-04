from ursina import *
from random import uniform

app = Ursina()
camera.orthographic = True
camera.fov = 20
#parametre de base
def appliquer_texture(objet, fichier):
    """
    Applique une texture (image) à l'entité Ursina associée à un objet du jeu.

    Paramètres :
    - objet (dict)   : dictionnaire représentant l’objet du jeu
                       (doit contenir la clé 'ent')
    - fichier (str)  : nom du fichier image (ex : "vaisseau.png")

    Effet :
    - associe l’image à objet["ent"].texture
    - fixe la couleur à blanc pour ne pas teinter la texture
    """
    objet["ent"].texture = fichier
    objet["ent"].color = color.white

joueur = {"ent": Entity(model='cube', color=color.green,collider='box'),"speed": 5}#joueurddd
ennemie = Entity(model='cube', color=color.red, position=(6,0,0),collider='box')#ennemie qui suis le joueur
obstacle= Entity(model='cube', color=color.blue,position=(4,5,0),scale=(1,5),collider='box')#obstacle

def deplacer_joueur(objet, direction):
    "deplace le joueur (project fusée avant)"
    d = objet["speed"] * time.dt
    if direction == 'right':
        objet['ent'].x += d
    if direction == 'left':
        objet['ent'].x -= d
    if direction == 'up':
        objet['ent'].y += d
    if direction == 'down':
        objet['ent'].y -= d

def les_controles():
    "c du wasd mais ursina pas ça en zqsd de base"
    if held_keys['w']:
        deplacer_joueur(joueur, "up")
    if held_keys['a']:
        deplacer_joueur(joueur, "left")
    if held_keys['d']:
        deplacer_joueur(joueur, "right")
    if held_keys['s']:
        deplacer_joueur(joueur, "down") #pour les deplacement tkt on s'en fous c juste pour tester les fonction des ennemie

def vers_le_joueur():
    "l'ennemie regarde le joueur puis avance vers l'avant a une vitesse de 4"
    direction = ennemie.look_at(joueur["ent"])
    ennemie.position += ennemie.forward * time.dt * 4
    
def update():
    les_controles()
    ancienne_position = ennemie.position
    vers_le_joueur()
    if ennemie.intersects(obstacle).hit:    #colision avec le mur
        ennemie.position = ancienne_position
    if ennemie.intersects(joueur["ent"]).hit:    #colision avec le joueur
        ennemie.position = ancienne_position
app.run()