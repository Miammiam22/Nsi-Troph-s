from ursina import *
from random import uniform, randint
app = Ursina()

window.entity_counter.visible = False
window.collider_counter.visible = False
window.fullscreen = False
#######################################
#                MUSIQUES             #
#######################################
#partie fait par youn
# musique= Audio('song/Spit It Out.mp3', loop=False, autoplay=False,volume=0.1)
# musique.play()
#mort
sang_bruit=Audio('song/sf_jet_sang_02.mp3', loop=False, autoplay=False,volume=1.5)
corp_bruit=Audio('song/sf_decapitation.mp3', loop=False, autoplay=False,volume=5)
#weapons
shootgun_shoot1=Audio('song/shootgun_shoot1.mp3', loop=False, autoplay=False,volume=0.5)
shootgun_shoot2=Audio('song/shootgun_shoot2.mp3', loop=False, autoplay=False,volume=0.3)
shootgun_recharge=Audio('song/shootgun_rechargement.mp3', loop=False, autoplay=False,volume=0.3)
shootgun_blanc=Audio('song/shootgun_blanc.mp3', loop=False, autoplay=False,volume=0.1)
#Entités
pas=Audio('song/pas.mp3', loop=False, autoplay=False,volume=1)





#######################################
#                CONTROLE             #
#######################################
#partie fait par lilian
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
    ],
    "Aim" : {                           # Touches pour visée
        "right mouse down" : 1,         # |
        "right mouse up" : 0            # |
    },
    "Run" : {                           # Touches pour courir
        "left shift" : 1,               # |
        "left shift up" : 0             # |
    }
}



#######################################
#                MONDE                #
#######################################

#Sprite du monde
Entity(model="quad", scale=(28, 21), position = Vec3(0,0,0.01), texture = "assets/world.png")

#Créer une boîte de collision en fonction de la taille et de la position
def creer_collision(taille_x, taille_y, position_x, position_y):
    Entity(
        model="quad",
        visible=False,
        collider = "box",
        scale=(taille_x, taille_y),
        position=Vec2(position_x, position_y)
    )


#Frontière du monde
creer_collision(28, 1, 0, 10)
creer_collision(28, 1, 0, -10)
creer_collision(1,  21, 13.5, 0)
creer_collision(1,  21, -13.5, 0)

# --- Murs intérieurs ---
#Salle Nord
creer_collision(4, 1, -2, 3)
creer_collision(1, 1, 3.5, 3)
creer_collision(1, 8, 4.5, 6.5)

#Salle Ouest
creer_collision(1, 10, -4.5, 5.5)
creer_collision(10, 1, -9, -3)

#Salle Nord-Est
creer_collision(10, 1, 9, -3)
creer_collision(1, 3, 4.5, -2)

#Salle Sud-Est
creer_collision(1, 4, 4.5, -8.5)



#######################################
#               CAMERA                #
#######################################
#partie fait par lilian

#Change le parent de la camera pour qu'elle puisse se déplacé et ainsi pouvoir avoir un monde 
Camera_follower = Entity()
camera_info = {"init_fov" : 60, "mouse_effect" : 1.6, "aim_fov_effect" : 15}

#Initialisation des paramètres de la camera
camera.parent = Camera_follower
camera.fov = camera_info["init_fov"]

#fonction qui permet de suivre le joueur
def Camera_follow_player(Camera_follower, Player) :
    Camera_follower.position = Player.position + mouse.position * camera_info["mouse_effect"]

#fonction qui permet de viser (elle diminue juste le champ de vision de la camera )
def Camera_aim(facteur):
    camera.fov = camera_info["init_fov"] - camera_info["aim_fov_effect"] * facteur



#######################################
#               COMMUN                #
#######################################
#partie fait par lilian et youn
sang_timer = 0
flaques = []

#Fonction qui permet de savoir si l'entité peut se déplacer (si il y a un collider box il ne peut pas)
def can_move(Entity, movement, marge_erreur) :
    hit_info1 = raycast(Entity.position, Vec2(movement.y, -movement.x) * marge_erreur + movement, distance=0.5,ignore= [Entity]) #La diagonale droite
    hit_info2 = raycast(Entity.position, Vec2(-movement.y, movement.x) * marge_erreur + movement, distance=0.5,ignore= [Entity]) #La diagonale gauche
    if hit_info1.hit or hit_info2.hit:  #Si l'un des 2 raycasts diagonaux touche une collision on renvoie False (il ne peut pas bouger) sinon True
        return False
    return True

#Fonction qui créer un effet à la position de l'impacte du tir
def shot_vfx(position) :
    if position :
        vfx = Entity(model = "quad", scale = (0.5, 0.5), position = position + Vec3(0,0,-0.1), texture = "assets/shot_vfx.png")
        destroy(vfx, 0.05)

def sang_song():
    global sang_timer#(ia)global était inconnu pour nous alors qu'il permet de modifier des variable dans des fonction(son utilistation a ete explique par l'ia puis on l'a applique nous même)
    sang_timer -= time.dt
    for flaque in flaques:
        dist = (Player.position - flaque.position).length()
        if dist < 0.8 and sang_timer <= 0:
            sang_bruit.play()
            sang_timer = 1
            break

def sang():
    choix=randint(1,5)
    if choix==1:
        return "assets/sang.png"
    elif choix==2:
        return "assets/sang2.png"
    elif choix==3:
        return "assets/sang3.png"
    elif choix==4:
        return "assets/sang4.png"
    elif choix==5:
        return "assets/sang5.png"



#######################################
#               JOUEUR                #
#######################################
#partie fait par lilian

#L'entité du joueur et ses infos
Player = Entity(model = "quad", collider = "box", texture = "assets/player_sprite.png")
player_info = {"vivant" : True,"running": False,"speed" : 3,"init_speed" : 3, "run_speed" : 4, "stamina" : 10, "max_stamina" : 10, "score" : 0}

#Fonction qui gère le déplacement du joueur
def Player_movement(Player_ent):
    #Parcours tout le dictionnaire des touches de mouvement
    for input in input_actions["Movement"].keys() :
        if held_keys[input] : #Si une correspond on récupére le vecteur associé à la touche
            direction = input_actions["Movement"][input] * player_info["speed"]
            if can_move(Player_ent, input_actions["Movement"][input], 0.9) : #Si le joueur peut bouger alors on le déplace
                Player_ent.position += direction * time.dt

#Fonction qui oriente le joueur vers le curseur
def Player_look_at_cursor(Player_ent) :
    Player_ent.look_at_2d(mouse.position + Player_ent.position)

#Fonction qui gère la stamina du joueur
def Player_stamina():
    #Si la stamina est en dessus du maximun on l'augmente
    if player_info["stamina"] < player_info["max_stamina"]:
        player_info["stamina"] += time.dt
    #Si le joueur court et a de la stamina on dimunie la stamina (plus vite que la régénération)
    if player_info["running"] and player_info["stamina"] > 0 :
        player_info["stamina"] -= 3 * time.dt
    # Si la stamina est à 0 le joueur ne peu pas courir (sa vitesse de marche reste)
    if player_info["stamina"] < 0 :
        player_info["speed"] = player_info["init_speed"]

#Fonction qui est appelé a chaque appelle de update()
def Player_update(Player_ent):
    Player_movement(Player_ent)
    Player_look_at_cursor(Player_ent)
    Player_stamina()



#######################################
#              INTERFACE              #
#######################################
#partie fait par youn et lilian
# Stamina
stamina_barre = Entity(
    model='quad',
    texture="stamina.png",
    scale=(1, 0.06),
    position=(0, 0.45),
    parent=camera.ui
)

#Fonction qui met à jour l'interface de la stamina
def stamina_ui():
    stamina_barre.scale = (player_info["stamina"] / player_info["max_stamina"], 0.06)

game_over = Text(
    "GAME OVER/SCORE: ",
    parent = camera.ui,
    position =(-0.6,0.1),
    scale=(5,5),
    color = color.orange
)
game_over.enabled = False



#######################################
#               ENNEMIE               #
#######################################
#partie fait par youn
armee = [] #tout les ennemies sont regrouper dedant pour pouvoir appliquer les fonction a chaque ennemie

def cree_ennemie(position_x, position_y):
    #creation de l'ennemie en forme de dico pour pouvoir ajouter notre variable True,False de ennemie(pour voir si il est vivant)
    nouvel_ennemie = {"ent":Entity(model="quad", position=(position_x, position_y), scale=(1,1), collider="box", texture="assets/ennemie_sprite.png"), "vivant":True}
    armee.append(nouvel_ennemie)#pour les ajouter a la liste ligne 223
    return nouvel_ennemie
    
def attaque():
    "defini le comportement des ennemie"
    for nouvel_ennemie in armee:#on boot sur tout les ennemie
        if nouvel_ennemie["vivant"] and player_info["vivant"]:#on verifie que les 2 son vivant grâce au dico vivant
            dir_vector = Player.position - nouvel_ennemie["ent"].position#on recupere la positon du joueur
            distance = dir_vector.length()#on cree un veteur qui point toujours vers lui
            if distance < 5:#si ça distance est de moins de 5(vecteur su dessus)
                nouvel_ennemie["ent"].look_at_2d(Player.position)#l'ennemie regarde le joueur
                if can_move(nouvel_ennemie["ent"], dir_vector.normalized(), 0.9):#il se dirige vers lui si il n'y a pas de mur entre eux 2
                    mouvement = dir_vector.normalized() * 5 * time.dt#(ia)normalized ma été expliquer par ia et je l'ai ensuite appliquer
                    nouvel_ennemie["ent"].position += Vec3(mouvement.x, mouvement.y, 0)#il avance vers lui(normalized() prend un vecteur et le transforme en vecteur de longueur 1, mais qui garde la même direction.)
            else:#si jamais il ne detecte rien
                ent = nouvel_ennemie["ent"]#on fait des petit racourci pour que ce soit plus lisible
                forward = ent.up#on definie la dirction vers l'avant(le haut du jour)pour allez vers l'avant
                hit = raycast(ent.position, forward, distance=2, ignore=[ent])#on verifie si il y a un mur devant lui
                if hit.hit:#si oui
                    ent.rotation_z -= 90#on tourne a 90 degrer vers la droite
                else:#si nn
                    mouvement = forward * 4 * time.dt#on fait des petit racourci pour que ce soit plus lisible
                    ent.position += Vec3(mouvement.x, mouvement.y, 0)#on avance a la vitesse de 4 tout droit


def ennemie_shoot():#tue le joueur
    for nouvel_ennemie in armee:#pour chaque ennemie
        if nouvel_ennemie["vivant"] and player_info["vivant"]:#on verifie pour pas qu'il n'y est d'erreur
            dir_vector = Player.position - nouvel_ennemie["ent"].position#on recupere la position du joueur
            dir_vector = Vec3(dir_vector.x, dir_vector.y, 0).normalized()#on cree les propriter du vecteur qui va le tuer si il le touche
            shoot = raycast(nouvel_ennemie["ent"].position, dir_vector, distance=2, ignore=[nouvel_ennemie["ent"]])#on cree le vecteur(raycast(si il touche True autrement False))
            if shoot.hit and shoot.entity == Player:
                shootgun_shoot1.play()#les different son
                corp_bruit.play()
                shot_vfx(shoot.world_point)#on cree un petit impacte defini au debut(119(partie de lilian))
                player_info["vivant"] = False#on dit bien que le jouer est mort pour empecher les erreur
                #on cree une entiter a la position de l'ennemie qui va avoir une texture aleatoire(sang()ligne 134 )
                falque_sang = Entity(model="quad", position=Vec3(Player.position.x, Player.position.y,0.001), scale=(uniform(1,3), uniform(1,3)), texture=sang())
                flaques.append(falque_sang)#on l'ajoute a la liste des flaques
                destroy(Player, 0.1)#on detruit le joueur avec mais on mais un delet de 0.1 pour eviter tout erreure
                game_over.text += str(player_info["score"])
                game_over.enabled = True#et on affiche le game over



#######################################
#          FONCTIONS URSINA           #
#######################################
#partie fait par youn et lilian

spawn_ennemie = {
    "timer" : 0
    }

def init_game(frequence):
    spawn_ennemie["timer"] += time.dt
    if spawn_ennemie["timer"] >= frequence :
        spawn_ennemie["timer"] = 0
        cree_ennemie(10, 3)
        cree_ennemie(-8, -2)
        cree_ennemie(11, -8)

def input(key) :

    if key in input_actions["Aim"] :
        Camera_aim(input_actions["Aim"][key])

    if key in input_actions["Attack"] and player_info["vivant"]:#si la touche attaque est presser defini ligne 22
        hit_shoot = raycast(Player.position, Player.up, ignore=[Player])#on cree un raycast qui part droit devant le joueur
        shot_vfx(hit_shoot.world_point)#au point de colision on cree un un petit impacte defini au debut(119(partie de lilian))
        Audio('song/shootgun_shoot1.mp3', loop=False, autoplay=True, volume=0.5)#on joue le son en sans passer par l'objet son deja cree au debut(si non l'ennmie l'utilise deja et il ne s'acrtive pas)
        for nouvel_ennemie in armee:
            if hit_shoot.entity == nouvel_ennemie["ent"]:#si le raycast touche un ennemie
                blood_position = nouvel_ennemie["ent"].position#on recuper la position de l'ennemie
                player_info["score"] += 1
                print(player_info["score"])
                corp_bruit.play()#son
                #on cree une entiter a la position de l'ennemie qui va avoir une texture aleatoire(sang()ligne 134 )
                falque_sang = Entity(model="quad", position=Vec3(blood_position.x,blood_position.y,0.001), scale=(uniform(1,3), uniform(1,3)), texture=sang())
                flaques.append(falque_sang)#on l'ajoute a la liste des flaques
                nouvel_ennemie["vivant"] = False#on dit bien que le jouer est mort pour empecher les erreur
                destroy(nouvel_ennemie["ent"], delay=0.1)#on detruit le joueur avec mais on mais un delet de 0.1 pour eviter tout erreure

    if key in input_actions["Run"]:
        if player_info["stamina"] < 0 :
            player_info["speed"] = player_info["init_speed"]
        else :
            player_info["speed"] = player_info["init_speed"] + player_info["run_speed"] * input_actions["Run"][key]
        player_info["running"] = input_actions["Run"][key]



#######################################
#               UPDATE                #
#######################################

def update():
    if player_info["vivant"]:
        init_game(5)
        Player_update(Player)
        Camera_follow_player(Camera_follower, Player)
        stamina_ui()
        sang_song()
        if armee:
            ennemie_shoot()
            attaque()

        
app.run()

