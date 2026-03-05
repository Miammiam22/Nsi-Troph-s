from ursina import *
app = Ursina()

window.fullscreen = True

#Inspiré de Unity où on peut assigner des valeurs à des inputs comme des vecteurs 2d, float, bool etc
input_actions = {
    "Movement" : {                      # Touches pour le déplacement du joueur
        "left arrow"  : Vec2(-1, 0),    # |
        "right arrow" : Vec2(1, 0),     # |
        "up arrow"    : Vec2(0, 1),     # |
        "down arrow"  : Vec2(0, -1)     # |
    },
    "Attack" : [                        # Touches pour utiliser l'arme équipé
        "left mouse down",              # |
        "space"                         # |
    ]
    
}


wall = Entity(model="quad", position=Vec2(0, 2), scale=Vec2(5, 1), collider="box")



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

def can_move(Entity, movement, marge_erreur) :
    size_x = Entity.scale.x / 2
    size_y = Entity.scale.y / 2
    hit_info1 = raycast(Entity.position + Vec2(movement.y * size_x * marge_erreur, movement.x * size_x * marge_erreur), movement, distance=0.5,ignore= [Entity])
    hit_info2 = raycast(Entity.position - Vec2(movement.y * size_y * marge_erreur, movement.x * size_y * marge_erreur), movement, distance=0.5,ignore= [Entity])
    if hit_info1.hit or hit_info2.hit:
        return False
    return True



#######################################
#               JOUEUR                #
#######################################

Player = Entity(model = "quad", collider = "sphere", texture = "assets/player_sprite.png")
player_info = {"speed" : 5}

def Player_movement(Player):
    for input in input_actions["Movement"].keys() :
        if held_keys[input] :
            direction = input_actions["Movement"][input] * player_info["speed"]
            if can_move(Player, input_actions["Movement"][input], 0.9) :
                Player.position += direction * time.dt

def Player_look_at_cursor(Player) :
    Player.look_at_2d(mouse.position + Player.position)



#######################################
#          FONCTIONS URSINA           #
#######################################

def input(key) :
    if key in input_actions["Attack"] :
        raycast(Player.position, Player.up, debug = True)

#Dans update(), essayer de mettre que des fonctions
def update() :
    Player_movement(Player)
    Player_look_at_cursor(Player)
    Camera_follow_player(Camera_follower, Player)

app.run()