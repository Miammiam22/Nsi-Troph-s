from ursina import *
app = Ursina()

# cam setup basique
camera.orthographic = True
camera.fov = 20
camera.position = (0,0,-10)

# les entités du jeu
joueur = {"ent": Entity(model='quad', color=color.green, position=(0,0,0), scale=(1,1), collider='box'), "speed":5}
ennemie = {"ent": Entity(model='quad', color=color.red, position=(6,0,0), scale=(1,1), collider='box'), "speed":5}
obstacle = Entity(model='quad', color=color.blue, position=(4,5,0), scale=(1,5), collider='box')

def deplacer_joueur(objet, direction):
    d = objet["speed"] * time.dt
    # jsp si y'a un meilleur moyen de faire ça mais ça marche
    if direction == 'right': objet['ent'].x += d
    if direction == 'left': objet['ent'].x -= d
    if direction == 'up': objet['ent'].y += d
    if direction == 'down': objet['ent'].y -= d

def les_controles():
    if held_keys['w']: deplacer_joueur(joueur, "up")
    if held_keys['a']: deplacer_joueur(joueur, "left")
    if held_keys['d']: deplacer_joueur(joueur, "right")
    if held_keys['s']: deplacer_joueur(joueur, "down")

def vers_le_joueur():
    dir_vector = joueur["ent"].position - ennemie["ent"].position
    if dir_vector.length() > 0:
        dir_vector = dir_vector.normalized() * ennemie["speed"] * time.dt
        ennemie["ent"].position += Vec3(dir_vector.x, dir_vector.y, 0)

# TODO: améliorer la vision, là c'est trop simple
def peut_voir_joueur():
    directions = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0)]
    for d in directions:
        hit = raycast(origin=ennemie["ent"].position, direction=d, distance=1, ignore=(ennemie["ent"],), debug=True)
        if hit.hit:
            return True
    return False

def update():
    les_controles()
    old_pos = Vec3(ennemie["ent"].position.x, ennemie["ent"].position.y, ennemie["ent"].position.z)
    vers_le_joueur()
    # annule le mouvement si collision
    if ennemie["ent"].intersects(obstacle).hit or peut_voir_joueur():
        ennemie["ent"].position = old_pos
    if ennemie["ent"].intersects(joueur["ent"]).hit:
        ennemie["ent"].position = old_pos

app.run()