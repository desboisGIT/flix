from tiles import *
from spritesheet import Spritesheet
from player import Player
import math
################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
pygame.init()
DISPLAY_W, DISPLAY_H = 1920, 1080
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
clock = pygame.time.Clock()
TARGET_FPS = 144
################################# LOAD PLAYER AND SPRITESHEET###################################
spritesheet = Spritesheet('spritesheet.png')
player = Player()
#################################### LOAD THE LEVEL #######################################
map = TileMap('test_level.csv', spritesheet )
player.position.x, player.position.y = 0, 0#map.start_x, map.start_y
################################# MOUSE BUTTON ##########################
LEFT = 1
RIGHT = 3
################################# BULLET ##########################
mouse_x, mouse_y = pygame.mouse.get_pos()
bulletSpeed = 3
all_bullets = []
length = 50
start = pygame.math.Vector2(player.position.x+60,player.position.y+60)
end = start     
################################# GAME LOOP ##########################
while running:
    dt = clock.tick(144) * .001 * TARGET_FPS
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                player.LEFT_KEY = True
            elif event.key == pygame.K_d:
                player.RIGHT_KEY = True
            elif event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_s:
                player.velocity.y = 30
        if event.type == pygame.MOUSEMOTION:
            mouse = pygame.mouse.get_pos()
            try:
                end = start + (mouse - start).normalize() * length
            except:
                pass    

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                player.LEFT_KEY = False
            elif event.key == pygame.K_d:
                player.RIGHT_KEY = False
            elif event.key == pygame.K_SPACE:
                if player.is_jumping:
                    player.velocity.y *= .25
                    player.is_jumping = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                if len(all_bullets) < 3 :
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    distance_x = mouse_x - player.position.x
                    distance_y = mouse_y - player.position.y    
                    angle = math.atan2(distance_y, distance_x)
                    # speed_x, speed_y can be `float` but I don't convert to `int` to get better position
                    speed_x = bulletSpeed * math.cos(angle)
                    speed_y = bulletSpeed * math.sin(angle)
                    # I copy `player.x, player.y` because I will change these values directly on list
                    all_bullets.append([player.position.x+30, player.position.y-80, speed_x, speed_y])
                else:
                    del all_bullets[0]
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    distance_x = mouse_x - player.position.x
                    distance_y = mouse_y - player.position.y    
                    angle = math.atan2(distance_y, distance_x)
                    # speed_x, speed_y can be `float` but I don't convert to `int` to get better position
                    speed_x = bulletSpeed * math.cos(angle)
                    speed_y = bulletSpeed * math.sin(angle)
                    # I copy `player.x, player.y` because I will change these values directly on list
                    all_bullets.append([player.position.x+55, player.position.y-80, speed_x, speed_y])
    for item in all_bullets:
        # speed_x, speed_y can be `float` but I don't convert to `int` to get better position
        item[0] += item[2]  # pos_x += speed_x
        item[1] += item[3]  # pos_y -= speed_y


    ################################# UPDATE/ Animate SPRITE #################################
    player.update(dt, map.tiles)
    ################################# UPDATE WINDOW AND DISPLAY #################################
    canvas.fill((0, 180, 240)) # Fills the entire screen with light blue
    map.draw_map(canvas)
    player.draw(canvas)
    window.blit(canvas, (0,0))
    pygame.draw.line(window, (255,0,0), start, end)
    for pos_x, pos_y, speed_x, speed_y in all_bullets:
        # need to convert `float` to `int` because `screen` use only `int` values
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        
        pygame.draw.rect(window, (0,0,255), pygame.Rect(pos_x, pos_y, 10, 10))
        pygame.display.flip()
    pygame.display.update()









