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



Entity(name="mur haut", model="quad", position=Vec2(0, 5), scale=(10, 1), collider="box")
Entity(name="mur bas", model="quad", position=Vec2(0, -5), scale=(10, 1), collider="box")
Entity(name="mur droite", model="quad", position=Vec2(5, 0), scale=(1, 10), collider="box")
Entity(name="mur gauche", model="quad", position=Vec2(-5, 0), scale=(1, 10), collider="box")



#######################################
#               CAMERA                #
#######################################

#Change le parent de la camera pour qu'elle puisse se déplacé et ainsi pouvoir avoir un monde 
Camera_follower = Entity()
camera_info = {"init_fov" : 60, "mouse_effect" : 1.5}

#Initialisation des paramètres de la camera
camera.parent = Camera_follower
camera.fov = camera_info["init_fov"]

def Camera_follow_player(Camera_follower, Player) :
    Camera_follower.position = Player.position + mouse.position * camera_info["mouse_effect"]



#######################################
#               COMMUN                #
#######################################

#ATTENTION : movement doit avoir une norme de 1
def can_move(Entity, movement, marge_erreur) :
    size_x = Entity.scale.x / 2
    size_y = Entity.scale.y / 2
    hit_info1 = raycast(Entity.position, Vec2(movement.y + movement.x - marge_erreur * movement.y, movement.y + movement.x - marge_erreur * movement.x), distance=0.5,ignore= [Entity], debug= True)
    hit_info2 = raycast(Entity.position, Vec2(-movement.y + movement.x + marge_erreur * movement.y, movement.y - movement.x - marge_erreur * movement.x), distance=0.5,ignore= [Entity], debug= True)
    if hit_info1.hit or hit_info2.hit:
        return False
    return True



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
            if can_move(Player_ent, input_actions["Movement"][input], 0.2) :
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
#               ENNEMI                #
#######################################

#code ici ---



#######################################
#          FONCTIONS URSINA           #
#######################################

def input(key) :
    if key in input_actions["Attack"] :
        raycast(Player.position, Player.up, ignore=[Player], debug = True)

#Dans update(), essayer de mettre que des fonctions
def update() :
    Player_update(Player)
    Camera_follow_player(Camera_follower, Player)

app.run()