from ursina import *
app = Ursina()
# cam setup basique
camera.orthographic = True
camera.fov = 20
camera.position = (0,0,-10)
# les entités du jeu
joueur = {"ent": Entity(model='quad', color=color.green, position=(0,0,0), scale=(1,1), collider='box'), "speed":5}
ennemie = {"ent": Entity(model='quad', color=color.red, position=(6,0,0), scale=(1,1), collider='box'), "speed":5, "longe_mur": False, "dir_longe": None, "cote_mur": None, "timer_inertie": 0}
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
        hit = raycast(origin=ennemie["ent"].position, direction=d, distance=1, ignore=(ennemie["ent"], joueur["ent"]), debug=True)
        if hit.hit:
            return True
    return False

def detecter_direction_mur():
    # détecte exactement quel côté est bloqué
    hit_r = raycast(origin=ennemie["ent"].position, direction=(1,0,0), distance=1.2, ignore=(ennemie["ent"], joueur["ent"]), debug = True)
    hit_l = raycast(origin=ennemie["ent"].world_position, direction=(-1,0,0), distance=1.2, ignore=(ennemie["ent"], joueur["ent"]), debug = True)
    hit_u = raycast(origin=ennemie["ent"].position, direction=(0,1,0), distance=1.2, ignore=(ennemie["ent"], joueur["ent"]), debug = True)
    hit_d = raycast(origin=ennemie["ent"].position, direction=(0,-1,0), distance=1.2, ignore=(ennemie["ent"], joueur["ent"]), debug = True)
    print(hit_l.hit, hit_r.hit, hit_u.hit, hit_d.hit)
    if hit_r.hit: return ("vertical", "droite")    # mur à droite → longer sur Y
    if hit_l.hit: return ("vertical", "gauche")    # mur à gauche → longer sur Y
    if hit_u.hit: return ("horizontal", "haut")    # mur en haut → longer sur X
    if hit_d.hit: return ("horizontal", "bas")     # mur en bas → longer sur X
    return ("horizontal", "bas")

def longer_mur():
    d = ennemie["speed"] * time.dt
    dir_mur = ennemie["dir_longe"]
    cote = ennemie["cote_mur"]

    if dir_mur == "vertical":
        # mur sur le côté, on longe sur Y
        ennemie["ent"].y -= d
        hit = raycast(origin=ennemie["ent"].position, direction=(1,0,0) if cote == "droite" else (-1,0,0), distance=1.2, ignore=(ennemie["ent"], joueur["ent"]))
        mur_detecte = hit.hit
    else:
        # mur en haut/bas, on longe sur X
        ennemie["ent"].x += d
        hit = raycast(origin=ennemie["ent"].position, direction=(0,1,0) if cote == "haut" else (0,-1,0), distance=1.2, ignore=(ennemie["ent"], joueur["ent"]))
        mur_detecte = hit.hit
    
    if mur_detecte:
        ennemie["timer_inertie"] = 0.2
    else:
        ennemie["timer_inertie"] -= time.dt
        if ennemie["timer_inertie"] <= 0:
            ennemie["longe_mur"] = False

def update():
    les_controles()
    old_pos = Vec3(ennemie["ent"].position.x, ennemie["ent"].position.y, ennemie["ent"].position.z)

    if ennemie["longe_mur"]:
        longer_mur()
        if ennemie["ent"].intersects(obstacle).hit:
            ennemie["ent"].position = old_pos
    else:
        vers_le_joueur()
        # annule le mouvement si collision
        if ennemie["ent"].intersects(obstacle).hit:
            ennemie["ent"].position = old_pos
            ennemie["dir_longe"], ennemie["cote_mur"] = detecter_direction_mur()
            ennemie["longe_mur"] = True
            ennemie["timer_inertie"] = 0.5

    if ennemie["ent"].intersects(joueur["ent"]).hit:
        ennemie["ent"].position = old_pos

app.run()