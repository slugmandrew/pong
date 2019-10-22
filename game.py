from typing import Dict, Union, Tuple

import pygame, sys, time
from pygame.locals import *

# set up pygame
from pygame.rect import RectType

pygame.init()

# set up the window
WINDOWWIDTH = 1000
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Animation')

# load images
background = pygame.image.load("skull_background.jpg").convert()
background = pygame.transform.rotozoom(background, 0, 1.2)
skull = pygame.image.load("skull.png").convert_alpha()
skull = pygame.transform.rotozoom(skull, 0, 0.5)
bone_left = pygame.image.load("bone_left.png").convert_alpha()
bone_right = pygame.image.load("bone_right.png").convert_alpha()
bone_left = pygame.transform.rotozoom(bone_left, 0, 0.45)
bone_right = pygame.transform.rotozoom(bone_right, 0, 0.45)


# set up direction/speed variables
STATIONARY = 0
DOWNLEFT = 1
DOWNRIGHT = 2
UPLEFT = 3
UPRIGHT = 4
MOVESPEED = 5

# set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (155, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

centreX = WINDOWWIDTH / 2
centreY = WINDOWHEIGHT / 2

# set up the ball

ball = {'rect': pygame.Rect(centreX, centreY, 20, 20), 'color': ORANGE, 'dir': UPRIGHT}
paddle1 = {'rect': pygame.Rect(50, 250, 20, 100), 'color': PURPLE}
paddle2 = {'rect': pygame.Rect(900, 250, 20, 100), 'color': RED}

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("Chiller", 96)

# render text

p1_score = 0
p2_score = 0

# run the game loop
while True:

    def new_ball(direction):
        return {'rect': pygame.Rect(centreX, centreY, 20, 20), 'color': ORANGE, 'dir': direction}


    # check for the QUIT event
    for event in pygame.event.get():

        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()

    # draw the black background onto the surface
    windowSurface.fill(BLACK)
    windowSurface.blit(background, (0, 0))


    # loop the block
    paddle1_rect = paddle1['rect']
    paddle2_rect = paddle2['rect']

    # move the block data structure
    if ball['dir'] == DOWNLEFT:
        ball['rect'].left -= MOVESPEED
        ball['rect'].top += MOVESPEED

    if ball['dir'] == DOWNRIGHT:
        ball['rect'].left += MOVESPEED
        ball['rect'].top += MOVESPEED

    if ball['dir'] == UPLEFT:
        ball['rect'].left -= MOVESPEED
        ball['rect'].top -= MOVESPEED

    if ball['dir'] == UPRIGHT:
        ball['rect'].left += MOVESPEED
        ball['rect'].top -= MOVESPEED

    # check if the block has moved out of the window
    if ball['rect'].top < 0:

        # block has moved past the top
        if ball['dir'] == UPLEFT:
            ball['dir'] = DOWNLEFT
        if ball['dir'] == UPRIGHT:
            ball['dir'] = DOWNRIGHT

    if ball['rect'].bottom > WINDOWHEIGHT:

        # block has moved past the bottom
        if ball['dir'] == DOWNLEFT:
            ball['dir'] = UPLEFT
        if ball['dir'] == DOWNRIGHT:
            ball['dir'] = UPRIGHT

    if ball['rect'].left < 0:
        # block has moved past the left side

        # increment score by 1
        p2_score += 1

        # wait for space bar to start

        ball = new_ball(UPRIGHT)

    if ball['rect'].right > WINDOWWIDTH:
        # block has moved past the right side

        # increment score by 1
        p1_score += 1

        ball = new_ball(UPLEFT)

        # if ball['dir'] == DOWNRIGHT:
        #     ball['dir'] = DOWNLEFT
        # if ball['dir'] == UPRIGHT:
        #     ball['dir'] = UPLEFT

    # left paddle
    if paddle1_rect.left >= ball['rect'].left:
        if ball['rect'].top > paddle1_rect.top and ball['rect'].bottom < paddle1_rect.bottom:
            # block has moved past the left side
            if ball['dir'] == DOWNLEFT:
                ball['dir'] = DOWNRIGHT
            if ball['dir'] == UPLEFT:
                ball['dir'] = UPRIGHT

    # right paddle
    if paddle2_rect.right <= ball['rect'].right:
        if ball['rect'].bottom > paddle2_rect.top and ball['rect'].top < paddle2_rect.bottom:
            # block has moved past the left side
            if ball['dir'] == DOWNRIGHT:
                ball['dir'] = DOWNLEFT
            if ball['dir'] == UPRIGHT:
                ball['dir'] = UPLEFT

    # draw the block onto the surface

    pygame.draw.rect(windowSurface, ball['color'], ball['rect'])

    # paddle1

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_q]:
        paddle1_rect.top -= MOVESPEED
    if keys_pressed[pygame.K_a]:
        paddle1_rect.top += MOVESPEED

    if keys_pressed[pygame.K_p]:
        paddle2_rect.top -= MOVESPEED
    if keys_pressed[pygame.K_l]:
        paddle2_rect.top += MOVESPEED

    windowSurface.blit(bone_left, (paddle1_rect.left, paddle1_rect.top))
    windowSurface.blit(bone_right, (paddle2_rect.left, paddle2_rect.top))

    windowSurface.blit(myfont.render(str(p1_score), 1, PURPLE), (20, 0))
    windowSurface.blit(myfont.render(str(p2_score), 1, RED), (940, 0))

    # draw the window onto the screen
    pygame.display.update()
    time.sleep(0.02)
