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

# set up direction variables
DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9
MOVESPEED = 5

# set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

centreX = WINDOWWIDTH / 2
centreY = WINDOWHEIGHT / 2

# set up the block data structure
# b1 = {'rect': pygame.Rect(300, 80, 50, 100), 'color': RED, 'dir': UPRIGHT}
ball: Dict[str, Union[RectType, Tuple[int, int, int], int]] = {'rect': pygame.Rect(centreX, centreY, 20, 20), 'color': GREEN, 'dir': UPRIGHT}
# b3 = {'rect': pygame.Rect(100, 150, 60, 60), 'color': BLUE, 'dir': DOWNLEFT}
# balls = [b2]

padddle1 = {'rect': pygame.Rect(50, 250, 20, 100), 'color': BLUE}
padddle2 = {'rect': pygame.Rect(900, 250, 20, 100), 'color': RED}

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("monospace", 96)

# render text

p1_score = 0
p2_score = 0

# run the game loop
while True:

    def new_ball(direction):
        return {'rect': pygame.Rect(centreX, centreY, 20, 20), 'color': GREEN, 'dir': direction}


    # check for the QUIT event
    for event in pygame.event.get():

        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()

    # draw the black background onto the surface
    windowSurface.fill(BLACK)

    # loop the block
    paddle1_rect = padddle1['rect']
    paddle2_rect = padddle2['rect']

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

    pygame.draw.rect(windowSurface, padddle1['color'], paddle1_rect)
    pygame.draw.rect(windowSurface, padddle2['color'], paddle2_rect)

    windowSurface.blit(myfont.render(str(p1_score), 1, BLUE), (0, 0))
    windowSurface.blit(myfont.render(str(p2_score), 1, RED), (940, 0))

    # draw the window onto the screen
    pygame.display.update()
    time.sleep(0.02)
