from ursina import *
app = Ursina()

window.fullscreen = False

#Inspiré de Unity où on peut assigner des valeurs à des inputs comme des vecteurs 2d, float, bool etc
input_actions = {
    "Movement" : {                      # Touches pour le déplacement du joueur
        "a" :           Vec2(-1, 0),    # |
        "d" :           Vec2(1, 0),     # |
        "w" :           Vec2(0, 1),     # |
        "s" :           Vec2(0, -1)     # |
    },
    "Attack" : [                        # Touches pour utiliser l'arme équipé
        "left mouse down",              # |
        "space"                         # |
    ]
    
}




wall = Entity(model="quad", position=Vec2(0, 2), scale=Vec2(5, 1), collider="box")

ennemie = Entity(model="quad",position=(5,0),scale=(1,1),collider="box",texture = "assets/ennemie_sprite.png")


#######################################
#               CAMERA                #
#######################################

#Change le parent de la camera pour qu'elle puisse se déplacé et ainsi pouvoir avoir un monde 
Camera_follower = Entity()
camera_info = {"init_fov" : 60, "mouse_effect" : 1.6, "shot_effect" : 1.1}

#Initialisation des paramètres de la camera
camera.parent = Camera_follower
camera.fov = camera_info["init_fov"]

def Camera_follow_player(Camera_follower, Player) :
    Camera_follower.position = Player.position + mouse.position * camera_info["mouse_effect"]



#######################################
#               COMMUN                #
#######################################

def can_move(Entity, movement, marge_erreur) :
    hit_info1 = raycast(Entity.position, Vec2(movement.y, -movement.x) * marge_erreur + movement, distance=0.5,ignore= [Entity], debug= True)
    hit_info2 = raycast(Entity.position, Vec2(-movement.y, movement.x) * marge_erreur + movement, distance=0.5,ignore= [Entity], debug= True)
    if hit_info1.hit or hit_info2.hit:
        return False
    return True

def shot_vfx(position) :
    if position :
        vfx = Entity(model = "quad", scale = (0.5, 0.5), position = position + Vec3(0,0,-0.1), texture = "assets/shot_vfx.png")
        destroy(vfx, 0.05)



#######################################
#                MONDE                #
#######################################

#code ici ---



#######################################
#               JOUEUR                #
#######################################

Player = Entity(model = "quad", collider = "box", texture = "assets/player_sprite.png")
player_info = {"speed" : 5}

def Player_movement(Player_ent):
    for input in input_actions["Movement"].keys() :
        if held_keys[input] :
            direction = input_actions["Movement"][input] * player_info["speed"]
            if can_move(Player_ent, input_actions["Movement"][input], 0.9) :
                Player_ent.position += direction * time.dt

def Player_look_at_cursor(Player_ent) :
    Player_ent.look_at_2d(mouse.position + Player_ent.position)

def Player_update(Player_ent):
    Player_movement(Player_ent)
    Player_look_at_cursor(Player_ent)



#######################################
#              INTERFACE              #
#######################################

#code ici ---



#######################################
#               ENNEMIE               #
#######################################

def vers_le_joueur():
    if ennemie.enabled:
        dir_vector = Player.position - ennemie.position
        print(dir_vector)
        if dir_vector.length() > 0:
            if can_move(ennemie,dir_vector, 0.9):
                dir_vector = dir_vector.normalized() * 2 * time.dt
                ennemie.position += Vec3(dir_vector.x, dir_vector.y, 0)

def ennemie_look_at_player():
    ennemie.look_at_2d(Player.position)



#######################################
#          FONCTIONS URSINA           #
#######################################

def input(key) :
    if key in input_actions["Attack"] :
        hit_shoot = raycast(Player.position, Player.up, ignore=[Player])
        shot_vfx(hit_shoot.world_point)
        if hit_shoot.entity == ennemie:
            destroy(ennemie)


#Dans update(), essayer de mettre que des fonctions
def update() :
    Player_update(Player)
    Camera_follow_player(Camera_follower, Player)

    if ennemie :
        ennemie_look_at_player()
        vers_le_joueur()

app.run()