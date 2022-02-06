import random
import random
import sys
import time

import pygame
import pygame.locals
# set up pygame
import pygame.rect
from pygame._sdl2.controller import Controller
from pygame.constants import *

pygame.init()

# see debug information blitted in real time over the game
DEBUG_MODE = True

# set up the window
WINDOWWIDTH = 1000
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Animation')

pygame.joystick.init()
pygame._sdl2.controller.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)
joystick = joysticks[0]
# controller gives us a more 'natural' set of controls
controller = Controller.from_joystick(joystick)

print("Axes: " + str(joystick.get_numaxes()))
print("Hats: " + str(joystick.get_numhats()))
print("Balls: " + str(joystick.get_numballs()))
print("Buttons: " + str(joystick.get_numbuttons()))


def get_controller_left():
  return joystick.get_hat(0).index(0) == 1


def get_controller_right():
  return joystick.get_hat(0).index(0) == -1


def get_controller_up():
  return joystick.get_hat(0).index(1) == 1


def get_controller_down():
  return joystick.get_hat(0).index(1) == -1


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
BLUE = (0, 0, 255)
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
myfont = pygame.font.SysFont("Arial", 72)
myfont2 = pygame.font.SysFont("Courier", 30)

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

  if DEBUG_MODE:
    # print the state of all controller buttons in this loop
    for button in range(joystick.get_numbuttons()):
      windowSurface.blit(myfont2.render(f"B{button}", True, GREEN), (button * 60, 300))
      windowSurface.blit(myfont.render(str(joystick.get_button(button)), True, GREEN), (button * 60, 330))

    # now do the same for the axes!
    for axis in range(joystick.get_numaxes()):
      windowSurface.blit(myfont2.render(f"A{axis}", True, BLUE), (axis * 170, 400))
      windowSurface.blit(myfont.render(str(round(joystick.get_axis(axis), 1)), True, BLUE), (axis * 170, 430))

    # now do the same for the hats!
    for hat in range(joystick.get_numhats()):
      windowSurface.blit(myfont2.render(f"H{hat}", True, ORANGE), (hat * 170, 500))
      windowSurface.blit(myfont.render(str(joystick.get_hat(hat)), True, ORANGE), (hat * 170, 530))

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

  # check for keyboard controls
  keys_pressed = pygame.key.get_pressed()

  if keys_pressed[pygame.K_q] or controller.get_button(CONTROLLER_BUTTON_DPAD_UP):
    paddle1_rect.top -= SPEED
  if keys_pressed[pygame.K_a] or controller.get_button(CONTROLLER_BUTTON_DPAD_DOWN):
    paddle1_rect.top += SPEED

  if keys_pressed[pygame.K_p] or controller.get_button(CONTROLLER_BUTTON_Y):
    paddle2_rect.top -= SPEED
  if keys_pressed[pygame.K_l] or controller.get_button(CONTROLLER_BUTTON_A):
    paddle2_rect.top += SPEED

  windowSurface.blit(bone_left, (paddle1_rect.left, paddle1_rect.top))
  windowSurface.blit(bone_right, (paddle2_rect.left, paddle2_rect.top))

  windowSurface.blit(myfont.render(str(p1_score), True, PURPLE), (20, 0))
  windowSurface.blit(myfont.render(str(p2_score), True, RED), (940, 0))

  # draw the window onto the screen
  pygame.display.update()
  time.sleep(0.01)
