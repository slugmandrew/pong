import random

import pygame
import pygame.locals
# set up pygame
import pygame.rect
import sys
import time

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
bone_left = pygame.transform.rotozoom(bone_left, 0, 0.4)
bone_right = pygame.transform.rotozoom(bone_right, 0, 0.4)

# set up direction/speed variables
STATIONARY = "stationary"
DOWN_LEFT = "down-left"
DOWN_RIGHT = "down-right"
UP_LEFT = "up-left"
UP_RIGHT = "up-right"
SPEED = 5

# set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (155, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

centreX = WINDOWWIDTH / 2
centreY = WINDOWHEIGHT / 2

# function that chooses a random
def random_direction():
  options = [DOWN_LEFT, DOWN_RIGHT, UP_LEFT, UP_RIGHT]
  return random.choice(options)

# function that creates a new ball
def new_ball(direction):
  return {'rect': pygame.Rect(centreX, centreY, 20, 20), 'color': ORANGE, 'dir': direction}

# set up the ball
ball = new_ball(random_direction())

# set up the paddles
paddle1 = {'rect': pygame.Rect(50, 250, 20, 100), 'color': PURPLE}
paddle2 = {'rect': pygame.Rect(900, 250, 20, 100), 'color': RED}

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("Chiller", 96)

# render text

p1_score = 0
p2_score = 0

# run the game loop
while True:

  # check for the QUIT event
  for event in pygame.event.get():

    if event.type == pygame.locals.QUIT:
      pygame.quit()
      sys.exit()

  # draw the black background onto the surface
  windowSurface.fill(BLACK)
  background.set_alpha(75)
  windowSurface.blit(background, (0, 0))

  # move the block data structure
  if ball['dir'] == DOWN_LEFT:
    ball['rect'].left -= SPEED
    ball['rect'].top += SPEED

  if ball['dir'] == DOWN_RIGHT:
    ball['rect'].left += SPEED
    ball['rect'].top += SPEED

  if ball['dir'] == UP_LEFT:
    ball['rect'].left -= SPEED
    ball['rect'].top -= SPEED

  if ball['dir'] == UP_RIGHT:
    ball['rect'].left += SPEED
    ball['rect'].top -= SPEED

  # check if the block has moved out of the window
  if ball['rect'].top < 0:

    # block has moved past the top
    if ball['dir'] == UP_LEFT:
      ball['dir'] = DOWN_LEFT
    if ball['dir'] == UP_RIGHT:
      ball['dir'] = DOWN_RIGHT

  if ball['rect'].bottom > WINDOWHEIGHT:

    # block has moved past the bottom
    if ball['dir'] == DOWN_LEFT:
      ball['dir'] = UP_LEFT
    if ball['dir'] == DOWN_RIGHT:
      ball['dir'] = UP_RIGHT

  if ball['rect'].left < 0:
    # block has moved past the left side

    # increment score by 1
    p2_score += 1

    # wait for space bar to start

    ball = new_ball(UP_RIGHT)

  if ball['rect'].right > WINDOWWIDTH:
    # block has moved past the right side

    # increment score by 1
    p1_score += 1

    ball = new_ball(UP_LEFT)

    # if ball['dir'] == DOWNRIGHT:
    #     ball['dir'] = DOWNLEFT
    # if ball['dir'] == UPRIGHT:
    #     ball['dir'] = UPLEFT

  # grab the rectangles
  paddle1_rect = paddle1['rect']
  paddle2_rect = paddle2['rect']

  # left paddle
  if paddle1_rect.left >= ball['rect'].left:
    if ball['rect'].top > paddle1_rect.top and ball['rect'].bottom < paddle1_rect.bottom:
      # block has moved past the left side
      if ball['dir'] == DOWN_LEFT:
        ball['dir'] = DOWN_RIGHT
      if ball['dir'] == UP_LEFT:
        ball['dir'] = UP_RIGHT

  # right paddle
  if paddle2_rect.right <= ball['rect'].right:
    if ball['rect'].bottom > paddle2_rect.top and ball['rect'].top < paddle2_rect.bottom:
      # block has moved past the left side
      if ball['dir'] == DOWN_RIGHT:
        ball['dir'] = DOWN_LEFT
      if ball['dir'] == UP_RIGHT:
        ball['dir'] = UP_LEFT

  # draw the block onto the surface

  pygame.draw.circle(windowSurface, ball['color'], ball['rect'].center, 10.0)

  # paddle1

  keys_pressed = pygame.key.get_pressed()

  if keys_pressed[pygame.K_q]:
    paddle1_rect.top -= SPEED
  if keys_pressed[pygame.K_a]:
    paddle1_rect.top += SPEED

  if keys_pressed[pygame.K_p]:
    paddle2_rect.top -= SPEED
  if keys_pressed[pygame.K_l]:
    paddle2_rect.top += SPEED

  windowSurface.blit(bone_left, (paddle1_rect.left, paddle1_rect.top))
  windowSurface.blit(bone_right, (paddle2_rect.left, paddle2_rect.top))

  windowSurface.blit(myfont.render(str(p1_score), True, PURPLE), (20, 0))
  windowSurface.blit(myfont.render(str(p2_score), True, RED), (940, 0))

  # draw the window onto the screen
  pygame.display.update()
  time.sleep(0.01)
