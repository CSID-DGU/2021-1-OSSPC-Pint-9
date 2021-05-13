import pygame
import operator
import math
from random import *
from pygame.locals import *

from mino import *

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

STARTING_FRAMERATE_BY_DIFFCULTY = [50, 30, 20]
FRAMELATE_MULTIFLIER_BY_DIFFCULTY = [0.9, 0.8, 0.7]

# Define
block_size = 17 # Height, width of single block
width = 10 # Board width
height = 20 # Board height
framerate = 30 # Bigger -> Slower


pygame.init()

class ui_variables:
    # Fonts
    font_path = "./assets/fonts/OpenSans-Light.ttf"
    font_path_b = "./assets/fonts/OpenSans-Bold.ttf"
    font_path_i = "./assets/fonts/Inconsolata/Inconsolata.otf"

    h1 = pygame.font.Font(font_path, 50)
    h2 = pygame.font.Font(font_path, 30)
    h4 = pygame.font.Font(font_path, 20)
    h5 = pygame.font.Font(font_path, 13)
    h6 = pygame.font.Font(font_path, 10)

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 30)

    h2_i = pygame.font.Font(font_path_i, 30)
    h5_i = pygame.font.Font(font_path_i, 13)

    # Sounds
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav")
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
    single_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav")
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")

    #image
    levelup = pygame.image.load("assets/images/levelup.png")
    levelup = pygame.transform.smoothscale(levelup,(int(SCREEN_WIDTH * 0.25),int(SCREEN_HEIGHT*0.25)))
    #fever = pygame.image.load("assets/images/fever.png")
    #pygame.transform.smoothscale(fever, (200, 100))

    # Background colors
    black = (10, 10, 10) #rgb(10, 10, 10)
    white = (255, 255, 255) #rgb(255, 255, 255)
    grey_1 = (26, 26, 26) #rgb(26, 26, 26)
    grey_2 = (35, 35, 35) #rgb(35, 35, 35)
    grey_3 = (55, 55, 55) #rgb(55, 55, 55)
    grey_4 = (100,100,100)
    # Tetrimino colors
    cyan = (69, 206, 204) #rgb(69, 206, 204) # I
    blue = (64, 111, 249) #rgb(64, 111, 249) # J
    orange = (253, 189, 53) #rgb(253, 189, 53) # L
    yellow = (246, 227, 90) #rgb(246, 227, 90) # O
    green = (98, 190, 68) #rgb(98, 190, 68) # S
    pink = (242, 64, 235) #rgb(242, 64, 235) # T
    red = (225, 13, 27) #rgb(225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3,grey_4]


fever_image=pygame.image.load("assets/images/fever.png")
fever_image = pygame.transform.smoothscale(fever_image, (int(SCREEN_WIDTH*0.2), int(SCREEN_HEIGHT*0.2)))

def draw_image(window, img_path, x, y, width, height):
    x = x - (width / 2)
    y = y - (height / 2)
    image = pygame.image.load(img_path)
    image = pygame.transform.smoothscale(image, (width, height))
    window.blit(image, (x, y))
# Draw block
def draw_block(x, y, color):
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )

# Draw game screen
def draw_board(next, hold, score, level, goal):
    screen.fill(ui_variables.grey_1)
    sidebar_width = int(SCREEN_WIDTH * 0.5312)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(sidebar_width, 0, int(SCREEN_WIDTH * 0.2375), SCREEN_HEIGHT)
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4):
        for j in range(4):
            dx = int(SCREEN_WIDTH * 0.025) + sidebar_width + block_size * j
            dy = int(SCREEN_HEIGHT * 0.3743) + block_size * i
            if grid_n[i][j] != 0:
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size)
                )

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 220 + block_size * j
                dy = 50 + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size)
                    )

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)

    # Place texts
    screen.blit(text_hold, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_next, (int(SCREEN_WIDTH  * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.2780)))
    screen.blit(text_score, (int(SCREEN_WIDTH  * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.5187)))
    screen.blit(score_value, (int(SCREEN_WIDTH  * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.5614)))
    screen.blit(text_level, (int(SCREEN_WIDTH  * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.6791)))
    screen.blit(level_value, (int(SCREEN_WIDTH  * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.7219)))
    screen.blit(text_goal, (int(SCREEN_WIDTH  * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.8395)))
    screen.blit(goal_value, (int(SCREEN_WIDTH  * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(SCREEN_WIDTH * 0.25) + block_size * x
            dy = int(SCREEN_HEIGHT * 0.055) + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])

# Draw a tetrimino
def draw_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r):
        ty += 1

    # Draw ghost
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[tx + j][ty + i] = 8

    # Draw mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = grid[i][j]

# Erase a tetrimino
def erase_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(height+1):
        for i in range(width):
            if matrix[i][j] == 8:
                matrix[i][j] = 0

    # Erase mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = 0

# Returns true if mino is at bottom
def is_bottom(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (y + i + 1) > height:
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
                    return True

    return False

# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j - 1) < 0:
                    return True
                elif matrix[x + j - 1][y + i] != 0:
                    return True

    return False

# Returns true if mino is at the right edge
def is_rightedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j + 1) > width-1:
                    return True
                elif matrix[x + j + 1][y + i] != 0:
                    return True

    return False

# Returns true if turning right is possible
def is_turnable_r(x, y, mino, r):
    if r != 3:
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > width-1 or (y + i) < 0 or (y + i) > height:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True

# Returns true if turning left is possible
def is_turnable_l(x, y, mino, r):
    if r != 0:
        grid = tetrimino.mino_map[mino - 1][r - 1]
    else:
        grid = tetrimino.mino_map[mino - 1][3]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > width-1 or (y + i) < 0 or (y + i) > height:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True

# Returns true if new block is drawable
def is_stackable(mino):
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            #print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False

    return True

# Start game
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
pygame.display.set_caption("PINTRIS™")

# pages
blink = False
start = False
pause = False
done = False
game_over = False

# Initial values
score = 0
level = 1
difficulty = 0
goal = level * 2
bottom_count = 0
hard_drop = False
fever_score = 500
fever_count = 0
current_time=pygame.time.get_ticks()

dx, dy = 3, 0 # Minos location status
rotation = 0 # Minos rotation status

mino = randint(1, 7) # Current mino
next_mino = randint(1, 7) # Next mino

hold = False # Hold status
hold_mino = -1 # Holded mino

name_location = 0
name = [65, 65, 65]

with open('leaderboard.txt') as f:
    lines = f.readlines()
lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
for i in lines:
    leaders[i.split(' ')[0]] = int(i.split(' ')[1])
leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

matrix = [[0 for y in range(height + 1)] for x in range(width)] # Board matrix

###########################################################
# Loop Start
###########################################################

while not done:
    # Pause screen
    if pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                draw_board(next_mino, hold_mino, score, level, goal)

                pause_text = ui_variables.h2_b.render("PAUSED", 1, ui_variables.white)
                pause_start = ui_variables.h5.render("Press esc to continue", 1, ui_variables.white)

                screen.blit(pause_text, (43, 100))
                if blink:
                    screen.blit(pause_start, (40, 160))
                    blink = False
                else:
                    blink = True
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)

    # Game screen
    elif start:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 10)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation)
                draw_board(next_mino, hold_mino, score, level, goal)
                pygame.display.update()

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:

                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        #fever +=10 * level
                        draw_mino(dx, dy, mino, rotation)
                        draw_board(next_mino, hold_mino, score, level, goal)
                        if is_stackable(next_mino):
                            mino = next_mino
                            next_mino = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            start = False
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                # Erase line
                erase_count = 0
                for j in range(height+1):
                    is_full = True
                    for i in range(width):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        k = j
                        while k > 0:
                            for i in range(width):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1
                if erase_count == 1:
                    ui_variables.single_sound.play()
                    score += 50 * level
                elif erase_count == 2:
                    ui_variables.double_sound.play()
                    score += 100 * level
                elif erase_count == 3:
                    ui_variables.triple_sound.play()
                    score += 200 * level
                elif erase_count == 4:
                    ui_variables.tetris_sound.play()
                    score += 500 * level

                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    goal += level * 2
                    framerate = math.ceil(framerate * FRAMELATE_MULTIFLIER_BY_DIFFCULTY[difficulty])
                    screen.blit(ui_variables.levelup, (SCREEN_WIDTH*0.3, SCREEN_HEIGHT*0.2))
                    pygame.display.update()
                    pygame.time.delay(300)
                    for j in range(height):
                        for i in range(width):
                            matrix[i][j] = matrix[i][j + 1]       #기존있던블럭들 한칸증가


                    for i in range(width):
                        matrix[i][20] = 9                            #방해블록이 맨밑줄을 채움
                    k = randint(1, 9)
                    matrix[k][20] = 0                                #한군데가 구멍나있게 증가

                #점수 구간에 따른 피버타임
                for i in range(1,100,3):
                    if score >i*fever_score and score < (i+1)*fever_score: #500~1000,2000~2500.3500~4000
                        mino=randint(1,1)
                        next_mino=randint(1,1)

                        if blink:
                            screen.blit(fever_image,
                                        (SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.1))  # fever time시 이미지 깜빡거리게 #위치
                            blink = False
                        else:
                            blink = True

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino
                            next_mino = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                # Turn right
                elif event.key == K_UP or event.key == K_x:
                    if is_turnable_r(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
            elif event.type == VIDEORESIZE:
                SCREEN_WIDTH = event.w
                SCREEN_HEIGHT = event.h
                block_size = int(SCREEN_HEIGHT * 0.045)

        pygame.display.update()

    # Game over screen
    elif game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                over_text_1 = ui_variables.h2_b.render("GAME", 1, ui_variables.white)
                over_text_2 = ui_variables.h2_b.render("OVER", 1, ui_variables.white)
                over_start = ui_variables.h5.render("Press return to continue", 1, ui_variables.white)

                draw_board(next_mino, hold_mino, score, level, goal)
                screen.blit(over_text_1, (SCREEN_WIDTH*0.0775, SCREEN_HEIGHT*0.167))
                screen.blit(over_text_2, (SCREEN_WIDTH*0.0775, SCREEN_HEIGHT*0.233))

                name_1 = ui_variables.h2_i.render(chr(name[0]), 1, ui_variables.white)
                name_2 = ui_variables.h2_i.render(chr(name[1]), 1, ui_variables.white)
                name_3 = ui_variables.h2_i.render(chr(name[2]), 1, ui_variables.white)

                underbar_1 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_2 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_3 = ui_variables.h2.render("_", 1, ui_variables.white)

                screen.blit(name_1, (SCREEN_WIDTH*0.08125, SCREEN_HEIGHT*0.326))
                screen.blit(name_2, (SCREEN_WIDTH*0.11875, SCREEN_HEIGHT*0.326))
                screen.blit(name_3, (SCREEN_WIDTH*0.15625, SCREEN_HEIGHT*0.326))

                if blink:
                    screen.blit(over_start, (SCREEN_WIDTH*0.05, SCREEN_HEIGHT*0.4333))
                    blink = False
                else:
                    if name_location == 0:
                        screen.blit(underbar_1, (SCREEN_WIDTH*0.08125-2, SCREEN_HEIGHT*0.326-2))
                    elif name_location == 1:
                        screen.blit(underbar_2, (SCREEN_WIDTH*0.11875-2, SCREEN_HEIGHT*0.326-2))
                    elif name_location == 2:
                        screen.blit(underbar_3, (SCREEN_WIDTH*0.15625, SCREEN_HEIGHT*0.326-2))
                    blink = True
                pygame.display.update()
            # 마우스로 창크기조절
            elif event.type == VIDEORESIZE:
                SCREEN_WIDTH = event.w
                SCREEN_HEIGHT = event.h
                block_size = int(SCREEN_HEIGHT * 0.045)

                pygame.display.update()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()

                    outfile = open('leaderboard.txt','a')
                    outfile.write(chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                    outfile.close()

                    game_over = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    fever_score = 500
                    score = 0
                    fever=0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    with open('leaderboard.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_RIGHT:
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_LEFT:
                    if name_location != 0:
                        name_location -= 1
                    else:
                        name_location = 2
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_UP:
                    ui_variables.click_sound.play()
                    if name[name_location] != 90:
                        name[name_location] += 1
                    else:
                        name[name_location] = 65
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_DOWN:
                    ui_variables.click_sound.play()
                    if name[name_location] != 65:
                        name[name_location] -= 1
                    else:
                        name[name_location] = 90
                    pygame.time.set_timer(pygame.USEREVENT, 1)

    # Start screen
    else:
        # 복잡성을 줄이기 위해 start screen 내부에 page를 나누는 방식으로 구현했습니다.
        # Start page <-> Menu Page <-> Diffculty Page -> Start
        #                          <-> HelpPage
        #                          <-> SettingPage
        #
        # page는 지금 있는 page의 고유 넘버를 나타내고, 아래와 같이 상수를 사용해 가독성을 높였습니다.
        # selected는 선택지가 있는 페이지에서 몇번째 보기를 선택하고 있는지 나타내는 변수입니다.
        # 편의상 0부터 시작합니다.

        START_PAGE, MENU_PAGE, HELP_PAGE, SETTING_PAGE, DIFFICULTY_PAGE = 0, 10, 11, 12, 20
        page, selected = START_PAGE, 0

        while not done and not start:
            # Start Page
            if page == START_PAGE:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            # goto menu page
                            ui_variables.click_sound.play()
                            page, selected = MENU_PAGE, 0
                    elif event.type == VIDEORESIZE:
                        SCREEN_WIDTH = event.w
                        SCREEN_HEIGHT = event.h

                        block_size = int(SCREEN_HEIGHT * 0.045)
                        screen.fill(ui_variables.white)
                        pygame.draw.rect(
                            screen,
                            ui_variables.grey_1,
                            Rect(0, 0, int(SCREEN_WIDTH),
                            int(SCREEN_HEIGHT * 0.24))
                                )

                        title = ui_variables.h1.render("PINTRIS™", 1, ui_variables.white)
                        title_menu = ui_variables.h5.render("Press space to MENU", 1, ui_variables.grey_1)
                        title_info = ui_variables.h6.render("Copyright (c) 2021 PINT Rights Reserved.", 1, ui_variables.grey_1)

                        leader_1 = ui_variables.h5_i.render('1st ' + leaders[0][0] + ' ' + str(leaders[0][1]), 1, ui_variables.white)
                        leader_2 = ui_variables.h5_i.render('2nd ' + leaders[1][0] + ' ' + str(leaders[1][1]), 1, ui_variables.white)
                        leader_3 = ui_variables.h5_i.render('3rd ' + leaders[2][0] + ' ' + str(leaders[2][1]), 1, ui_variables.white)

                        if blink:
                            screen.blit(title_menu, title.get_rect(center=(SCREEN_WIDTH/2+40, SCREEN_HEIGHT *0.44)))

                        blink = not blink

                        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT *0.1)))
                        screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT *0.77)))

                        screen.blit(leader_1, (int(SCREEN_WIDTH * 0.033), int(SCREEN_HEIGHT *0.0347)))
                        screen.blit(leader_1, (int(SCREEN_WIDTH * 0.033), int(SCREEN_HEIGHT *0.0614)))
                        screen.blit(leader_1, (int(SCREEN_WIDTH * 0.033), int(SCREEN_HEIGHT *0.096)))
                block_size = int(SCREEN_HEIGHT * 0.045)
                screen.fill(ui_variables.white)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    Rect(0, 0, int(SCREEN_WIDTH),
                         int(SCREEN_HEIGHT * 0.24))
                )

                title = ui_variables.h1.render("PINTRIS™", 1, ui_variables.white)
                title_menu = ui_variables.h5.render("Press space to MENU", 1, ui_variables.grey_1)
                title_info = ui_variables.h6.render("Copyright (c) 2021 PINT Rights Reserved.", 1, ui_variables.grey_1)

                leader_1 = ui_variables.h5_i.render('1st ' + leaders[0][0] + ' ' + str(leaders[0][1]), 1,
                                                    ui_variables.white)
                leader_2 = ui_variables.h5_i.render('2nd ' + leaders[1][0] + ' ' + str(leaders[1][1]), 1,
                                                    ui_variables.white)
                leader_3 = ui_variables.h5_i.render('3rd ' + leaders[2][0] + ' ' + str(leaders[2][1]), 1,
                                                    ui_variables.white)

                if blink:
                    screen.blit(title_menu, title.get_rect(center=(SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT * 0.44)))

                blink = not blink

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.77)))

                screen.blit(leader_1, (int(SCREEN_WIDTH * 0.033), int(SCREEN_HEIGHT * 0.0347)))
                screen.blit(leader_1, (int(SCREEN_WIDTH * 0.033), int(SCREEN_HEIGHT * 0.0614)))
                screen.blit(leader_1, (int(SCREEN_WIDTH * 0.033), int(SCREEN_HEIGHT * 0.096)))
            # MENU PAGE
            elif page == MENU_PAGE:
                current_selected = selected
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            # back to start page
                            ui_variables.click_sound.play()
                            page, selected = START_PAGE, 0
                        elif event.key == K_DOWN:
                            if selected == 0 or selected == 1:
                                # next menu select
                                ui_variables.click_sound.play()
                                selected = selected + 1
                        elif event.key == K_UP:
                            if selected == 1 or selected == 2:
                                # previous menu select
                                ui_variables.click_sound.play()
                                selected = selected - 1
                        elif event.key == K_SPACE:
                            if selected == 0:
                                # select start menu, goto difficulty select page
                                ui_variables.click_sound.play()
                                page, selected = DIFFICULTY_PAGE, 0
                            elif selected == 1:
                                # select help menu, goto help page
                                ui_variables.click_sound.play()
                                page = HELP_PAGE
                            elif selected == 2:
                                # select settings menu, goto settings menu
                                ui_variables.click_sound.play()
                                page = SETTING_PAGE
                    #마우스로 창크기조절
                    elif event.type == VIDEORESIZE:
                        SCREEN_WIDTH = event.w
                        SCREEN_HEIGHT = event.h
                        block_size = int(SCREEN_HEIGHT * 0.045)
                        screen.fill(ui_variables.white)
                        pygame.draw.rect(
                            screen,
                            ui_variables.grey_1,
                            Rect(0, 0, int(SCREEN_WIDTH),
                                 int(SCREEN_HEIGHT * 0.24))
                        )

                        title = ui_variables.h1.render("PINTRIS™", 1, ui_variables.white)
                        title_info = ui_variables.h6.render("Press up and down to change, space to select", 1,
                                                            ui_variables.grey_1)

                        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                        screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.77)))

                        title_start = ui_variables.h5.render("Game start", 1, ui_variables.grey_1)
                        title_help = ui_variables.h5.render("Help", 1, ui_variables.grey_1)
                        title_setting = ui_variables.h5.render("Settings", 1, ui_variables.grey_1)

                        pos_start = title_start.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))
                        pos_help = title_help.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
                        pos_setting = title_setting.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))

                        # blink current selected option
                        if blink:
                            if current_selected == 0:
                                screen.blit(title_help, pos_help)
                                screen.blit(title_setting, pos_setting)
                            elif current_selected == 1:
                                screen.blit(title_start, pos_start)
                                screen.blit(title_setting, pos_setting)
                            else:
                                screen.blit(title_start, pos_start)
                                screen.blit(title_help, pos_help)
                        else:
                            screen.blit(title_start, pos_start)
                            screen.blit(title_help, pos_help)
                            screen.blit(title_setting, pos_setting)

                        blink = not blink


                block_size = int(SCREEN_HEIGHT * 0.045)
                screen.fill(ui_variables.white)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    Rect(0, 0, int(SCREEN_WIDTH),
                         int(SCREEN_HEIGHT * 0.24))
                )

                title = ui_variables.h1.render("PINTRIS™", 1, ui_variables.white)
                title_info = ui_variables.h6.render("Press up and down to change, space to select", 1,
                                                    ui_variables.grey_1)

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.77)))

                title_start = ui_variables.h5.render("Game start", 1, ui_variables.grey_1)
                title_help = ui_variables.h5.render("Help", 1, ui_variables.grey_1)
                title_setting = ui_variables.h5.render("Settings", 1, ui_variables.grey_1)

                pos_start = title_start.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))
                pos_help = title_help.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
                pos_setting = title_setting.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))

                # blink current selected option
                if blink:
                    if current_selected == 0:
                        screen.blit(title_help, pos_help)
                        screen.blit(title_setting, pos_setting)
                    elif current_selected == 1:
                        screen.blit(title_start, pos_start)
                        screen.blit(title_setting, pos_setting)
                    else:
                        screen.blit(title_start, pos_start)
                        screen.blit(title_help, pos_help)
                else:
                    screen.blit(title_start, pos_start)
                    screen.blit(title_help, pos_help)
                    screen.blit(title_setting, pos_setting)

                blink = not blink

            # HELP PAGE
            elif page == HELP_PAGE:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        # back to menu page
                        if event.key == K_ESCAPE:
                            ui_variables.click_sound.play()
                            page, selected = MENU_PAGE, 0
                    # 마우스로 창크기조절
                    elif event.type == VIDEORESIZE:
                        SCREEN_WIDTH = event.w
                        SCREEN_HEIGHT = event.h
                        block_size = int(SCREEN_HEIGHT * 0.045)
                        screen.fill(ui_variables.white)
                        pygame.draw.rect(
                            screen,
                            ui_variables.grey_1,
                            pygame.draw.rect(
                                screen,
                                ui_variables.grey_1,
                                Rect(0, 0, int(SCREEN_WIDTH),
                                     int(SCREEN_HEIGHT * 0.24))
                            )
                        )

                        title = ui_variables.h1.render("HELP", 1, ui_variables.white)
                        title_explain = ui_variables.h5.render("Help page", 1, ui_variables.grey_1)
                        title_info = ui_variables.h6.render("Press esc to return menu", 1, ui_variables.grey_1)

                        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                        screen.blit(title_explain, title_explain.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
                        screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.77)))

                block_size = int(SCREEN_HEIGHT * 0.045)
                screen.fill(ui_variables.white)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    pygame.draw.rect(
                        screen,
                        ui_variables.grey_1,
                        Rect(0, 0, int(SCREEN_WIDTH),
                             int(SCREEN_HEIGHT * 0.24))
                    )
                )

                title = ui_variables.h1.render("HELP", 1, ui_variables.white)
                title_explain = ui_variables.h5.render("Help page", 1, ui_variables.grey_1)
                title_info = ui_variables.h6.render("Press esc to return menu", 1, ui_variables.grey_1)

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.1)))
                screen.blit(title_explain, title_explain.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))
                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.77)))

            # Setting Page
            elif page == SETTING_PAGE:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            # back to menu page
                            ui_variables.click_sound.play()
                            page, selected = MENU_PAGE, 0
                    # 마우스로 창크기조절
                    elif event.type == VIDEORESIZE:
                        SCREEN_WIDTH = event.w
                        SCREEN_HEIGHT = event.h
                        block_size = int(SCREEN_HEIGHT * 0.045)
                        screen.fill(ui_variables.white)
                        pygame.draw.rect(
                            screen,
                            ui_variables.grey_1,
                            pygame.draw.rect(
                                screen,
                                ui_variables.grey_1,
                                Rect(0, 0, int(SCREEN_WIDTH),
                                     int(SCREEN_HEIGHT * 0.24))
                            )
                        )

                        title = ui_variables.h1.render("SETTINGS", 1, ui_variables.white)
                        title_explain = ui_variables.h5.render("Setting page", 1, ui_variables.grey_1)
                        title_info = ui_variables.h6.render("Press esc to return menu", 1, ui_variables.grey_1)

                        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                        screen.blit(title_explain, title_explain.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
                        screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.77)))

                block_size = int(SCREEN_HEIGHT * 0.045)
                screen.fill(ui_variables.white)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    pygame.draw.rect(
                        screen,
                        ui_variables.grey_1,
                        Rect(0, 0, int(SCREEN_WIDTH),
                             int(SCREEN_HEIGHT * 0.24))
                    )
                )

                title = ui_variables.h1.render("SETTINGS", 1, ui_variables.white)
                title_explain = ui_variables.h5.render("Setting page", 1, ui_variables.grey_1)
                title_info = ui_variables.h6.render("Press esc to return menu", 1, ui_variables.grey_1)

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.1)))
                screen.blit(title_explain, title_explain.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))
                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.77)))

            # difficulty page
            elif page == DIFFICULTY_PAGE:
                current_selected = selected
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            # back to menu page
                            ui_variables.click_sound.play()
                            page, selected = MENU_PAGE, 0
                        elif event.key == K_RIGHT:
                            if selected == 0 or selected == 1:
                                # next difficulty select
                                ui_variables.click_sound.play()
                                selected = selected + 1
                        elif event.key == K_LEFT:
                            if selected == 1 or selected == 2:
                                # previous difficulty select
                                ui_variables.click_sound.play()
                                selected = selected - 1
                        if event.key == K_SPACE:
                            # start game with selected difficulty
                            ui_variables.click_sound.play()
                            start = True
                            difficulty = selected
                            framerate = STARTING_FRAMERATE_BY_DIFFCULTY[selected]
                    # 마우스로 창크기조절
                    elif event.type == VIDEORESIZE:
                        SCREEN_WIDTH = event.w
                        SCREEN_HEIGHT = event.h
                        block_size = int(SCREEN_HEIGHT * 0.045)
                        screen.fill(ui_variables.white)
                        pygame.draw.rect(
                            screen,
                            ui_variables.grey_1,
                            pygame.draw.rect(
                                screen,
                                ui_variables.grey_1,
                                Rect(0, 0, int(SCREEN_WIDTH),
                                     int(SCREEN_HEIGHT * 0.24))
                            )
                        )

                        difficulty_name = ["EASY", "NORMAL", "HARD"][current_selected]
                        difficulty_explain = [
                            "Easy mode",
                            "Normal mode",
                            "Hard mode",
                        ][current_selected]

                        title = ui_variables.h1.render(difficulty_name, 1, ui_variables.white)
                        title_explain = ui_variables.h5.render(difficulty_explain, 1, ui_variables.grey_1)
                        title_info = ui_variables.h6.render("Press left and right to change, space to start", 1,
                                                            ui_variables.grey_1)

                        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                        screen.blit(title_explain, title_explain.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
                        screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.77)))


                block_size = int(SCREEN_HEIGHT * 0.045)
                screen.fill(ui_variables.white)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    pygame.draw.rect(
                        screen,
                        ui_variables.grey_1,
                        Rect(0, 0, int(SCREEN_WIDTH),
                             int(SCREEN_HEIGHT * 0.24))
                    )
                )

                difficulty_name = ["EASY", "NORMAL", "HARD"][current_selected]
                difficulty_explain = [
                    "Easy mode",
                    "Normal mode",
                    "Hard mode",
                ][current_selected]

                title = ui_variables.h1.render(difficulty_name, 1, ui_variables.white)
                title_explain = ui_variables.h5.render(difficulty_explain, 1, ui_variables.grey_1)
                title_info = ui_variables.h6.render("Press left and right to change, space to start", 1, ui_variables.grey_1)

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.1)))
                screen.blit(title_explain, title_explain.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))
                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.77)))

                # draw left, right sign (triangle)
                if current_selected > 0:
                    pos = [[10, SCREEN_HEIGHT / 2], [15, SCREEN_HEIGHT / 2 - 5], [15, SCREEN_HEIGHT / 2 + 5]]
                    pygame.draw.polygon(screen, ui_variables.grey_1, pos, 1)

                if current_selected < 2:
                    pos = [[SCREEN_WIDTH - 10, SCREEN_HEIGHT/2], [SCREEN_WIDTH - 15, SCREEN_HEIGHT / 2 - 5],
                           [SCREEN_WIDTH - 15, SCREEN_HEIGHT / 2 + 5]]
                    pygame.draw.polygon(screen, ui_variables.grey_1, pos, 1)

            if not start:
                pygame.display.update()
                clock.tick(3)

pygame.quit()