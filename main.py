import pygame
import Assets.Scripts.framework as framework
import Assets.Scripts.background as backg
import Assets.Scripts.bg_particles as bg_particles
import Assets.Scripts.Sword as Sword
import Assets.Scripts.grass as g
import math
import random 
import time as t
from pygame.locals import *
pygame.init()
s_width = 1000
s_height = 600
screen = pygame.display.set_mode((s_width,s_height))
display = pygame.Surface((s_width//2, s_height//2))
def blit_tree(display, tree_img, tree_locs, scroll):
    tree_screen = display.copy()
    for loc in tree_locs:
        tree_screen.blit(tree_img, (loc[0] - scroll[0], loc[1] - scroll[1] - 160))
    tree_screen.set_alpha(170)
    display.blit(tree_screen, (0,0))

def create_drones(drones, drone_loc, drone_animation, snow_ball_img):
    for loc in drone_loc:
        drones.append(framework.Drones(loc[0], loc[1], drone_animation[0].get_width(), drone_animation[0].get_height(), drone_animation, snow_ball_img))
    return drones

def blit_drones(drones, display, scroll, player, time, dt):
    for pos, drone in sorted(enumerate(drones), reverse=True):
        if drone.alive:
            drone.move(scroll, player, time, display, dt)
            drone.draw(display, scroll)
        else:
            drones.pop(pos)

def blit_grass(grasses, display, scroll, player):
    for grass in grasses:
        if grass.get_rect().colliderect(player.get_rect()):
            grass.colliding()
        grass.draw(display, scroll)
    

def get_image(sheet, frame, width, height, scale, colorkey):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colorkey)
    return image

#Game Variables
run = True
clock = pygame.time.Clock()
#Loading Images
tile_1 = pygame.image.load("./Assets/Tiles/tile1.png").convert_alpha()
tile_2 = pygame.image.load("./Assets/Tiles/tile2.png").convert_alpha()
tile_3 = tile_1.copy()
tile_3 = pygame.transform.flip(tile_3, True, False)
tile_4 = pygame.image.load("./Assets/Tiles/tile4.png").convert_alpha()
tile_5 = tile_4.copy()
tile_5 = pygame.transform.flip(tile_5, True, False)
tile_6 = pygame.image.load("./Assets/Tiles/tile5.png").convert_alpha()
tiles = [tile_1, tile_2, tile_3, tile_4, tile_5, tile_6]
tree_img = pygame.image.load("./Assets/Sprites/tree.png").convert_alpha()
tree_img_copy = tree_img.copy()
tree_img = pygame.transform.scale(tree_img_copy, (tree_img_copy.get_width() * 3, tree_img_copy.get_height()*3))
player_img = pygame.image.load("./Assets/Sprites/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_img.get_width()*1.5, player_img.get_height()*1.5))
player_img.set_colorkey((255,255,255))
player_idle_img = pygame.image.load("./Assets/Sprites/player_idle.png").convert_alpha()
player_run_img = pygame.image.load("./Assets/Sprites/player_run.png").convert_alpha()
drone_img = pygame.image.load("./Assets/Sprites/drone.png").convert_alpha()
katana_img = pygame.image.load("./Assets/Sprites/katana.png").convert_alpha()
katana = katana_img.copy()
katana = pygame.transform.scale(katana_img, (katana_img.get_width()*1.5, katana_img.get_height()*1.5))
katana.set_colorkey((255,255,255))
snow_ball_img = pygame.image.load("./Assets/Sprites/snow_ball.png").convert_alpha()
snow_ball_img.set_colorkey((0,0,0))
#Map
map = framework.Map("./Assets/Maps/level1.txt", tiles)
#Player 
player_idle_animation = []
player_run_animation = []
for x in range(4):
    player_idle_animation.append(get_image(player_idle_img, x, 14, 28, 1.5, (255,255,255)))
    player_run_animation.append(get_image(player_run_img, x, 14, 28, 1.5, (255,255,255)))
player = framework.Player(160,50,player_img.get_width(),player_img.get_height(), player_idle_animation, player_run_animation)
dash = False
extra_dash = True
check_for_dash = True
#player_attacks = [[colliderect, current_time, time_delay]]
player_attacks  = []
#Scroll
true_scroll = [0,0]
scroll = [0,0]
#Drones
drones = []
drone_animation = []
drone_last_update = 0
drone_cooldown = 3000
#Grass
grasses = []
grass_loc = []
grass_spawn = True
grass_last_update = 0
grass_cooldown = 50
#Sword
p_sword = Sword.sword(50,50,katana.get_width(),katana.get_height(),katana)
for x in range(2):
    drone_animation.append(get_image(drone_img, x, 32,32,2, (0,0,0)))
#drone = framework.Drones(60, 30, drone_animation[0].get_width(), drone_animation[1].get_height(), drone_animation)
#Background Stripes 
bg = backg.background()
bg_particle_effect = bg_particles.Master()
#Sparks
sparks = []
#BackGround Settings
lightning = False
lightning_cooldown = 20000
lightning_colors = [[(0,64,0), (0,128,64), (0,255,0)], [(255,0,0), (128,0,0), (128,64,64)], [(255,255,0), (255,128,64), (255,255,128), (255,128,0)]]
lightning_color = 0
lightning_last_update = 0
lightning_alpha = 255
#Time
last_time = t.time()
while run:
    clock.tick(60)
    dt = t.time() - last_time
    dt *= 60
    last_time = t.time()
    time = pygame.time.get_ticks()
    #Checking For Lightning
    if not lightning:
        if time - lightning_last_update > lightning_cooldown:
            lightning = False
            lightning_alpha = 255
            lightning_color = lightning_colors[random.randint(0,len(lightning_colors) - 1)]
            lightning_last_update = time
        display.fill((15,27,55))
        blur_surf = display.copy()
        bg.recursive_call(blur_surf)
        blur_surf.set_alpha(80)
    else:
        display.fill(lightning_color[random.randint(0,len(lightning_color) - 1)])
        blur_surf = display.copy()
        blur_surf.set_alpha(lightning_alpha)
        lightning_alpha -= 5
        if lightning_alpha < 100:
            lightning = False
    display.blit(blur_surf, (0,0))
    #Blitting The Map
    tile_rects, tree_locs, drone_loc, grass_loc = map.blit_map(display, scroll)
    #Creating Items
    if time - drone_last_update > drone_cooldown:
        drones = create_drones(drones, drone_loc, drone_animation, snow_ball_img)
        drone_last_update = time
    if grass_spawn:
        for loc in grass_loc:
            x_pos = loc[0]
            while x_pos < loc[0] + 32:
                x_pos += 2.5
                grasses.append(g.grass([x_pos, loc[1]+14], 2, 18))
        grass_spawn = False
    #Blitting Items before Blitting Player
    blit_tree(display, tree_img, tree_locs, scroll)
    blit_drones(drones, display, scroll, player, time, dt)
    #Movement of grass
    if time - grass_last_update > grass_cooldown:
        for grass in grasses:
            grass.move()
        grass_last_update = time
    #Calculating scroll
    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 241) / 20
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 166) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    #Checking For Player Attack
    if player_attacks != []:
        for pos, attack in sorted(enumerate(player_attacks), reverse=True):
            if time - attack[1] < attack[2]:
                if drones != []:
                    for drone in drones:
                        if attack[0].colliderect(drone.get_rect()):
                            drone.health -= 2
                            dt = 0.2
                            scroll[0] += random.randint(-5,5)
                            scroll[1] += random.randint(-5,5)
                            for x in range(20):
                                sparks.append(framework.Spark([drone.get_rect().x - scroll[0] + drone_animation[0].get_width()//2, drone.get_rect().y - scroll[1] + drone_animation[0].get_height()//2],math.radians(random.randint(0,360)), random.randint(2, 5),(121, 36, 36), 1, 0))
            else:
                player_attacks.pop(pos)
    #Player Dash
    if dash:
        #Getting the mouse position
        mx , my = pygame.mouse.get_pos()
        mx = mx/2
        my = my/2
        m_pos = []
        m_pos.append(mx)
        m_pos.append(my)
        #Getting the 3rd vertex of the triangle
        point = (m_pos[0], player.get_rect().y + 16 - scroll[1])
        #Calculating distance between the points
        l1 = math.sqrt(math.pow((point[1] - (player.get_rect().y + 16 - scroll[1])), 2) + math.pow((point[0] - (player.get_rect().x + 20 - scroll[0])), 2))
        l2 = math.sqrt(math.pow((m_pos[1] - point[1]),2) + math.pow((m_pos[0] - point[0]),2))
        #Calculating the angle between them
        angle = math.atan2(l2,l1)
        angle = math.degrees(angle)
        #pygame.draw.line(display,(255,0,0), m_pos, point)
        #pygame.draw.line(display, (255,0,255), point, ((player.get_rect().x + 20 - scroll[0]), (player.get_rect().y + 16 - scroll[1])))
        player.dash(angle, m_pos, scroll, time)
        dash = not dash
    #Moving the Player
    player.move(tile_rects, time, dt)
    #Drawing the Player
    facing_left = player.draw(display, scroll)
    #Sword
    p_sword.update((player.get_rect().x, player.get_rect().y), facing_left)
    p_sword.blit(display, scroll)
    #Background Particles
    bg_particle_effect.recursive_call(time, display, scroll, dt)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_attacks.append(list((p_sword.attack(), time, 500)))
    #Sparks Blitting
    if sparks != []:
        for i, spark in sorted(enumerate(sparks), reverse=True):
            spark.move(dt)
            spark.draw(display)
            if not spark.alive:
                sparks.pop(i)
    #Blitting Items After Blitting The Player
    blit_grass(grasses, display, scroll, player)
    surf = pygame.transform.scale(display, (s_width, s_height))
    screen.blit(surf, (0,0))
    pygame.display.update()