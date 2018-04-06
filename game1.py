import pygame
import time
import random

pygame.init()

# Game Dimensions (800 x 600)

display_width = 800
display_height = 600

# initializing rgb colors

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# creating display

gameDisplay = pygame.display.set_mode((display_width, display_height))

# setting window title

pygame.display.set_caption("Smiley Face Dash")

# clock object for controlling time in the game

clock = pygame.time.Clock()

# loading smiley face image

smileyImg = pygame.image.load("smiley.png")
smileyImgWidth = 73
smileyImgHeight = 73

# This function displays the smiley face to the screen at coordinates x and y, two parameters that it is passed by
# whatever function calls it.


def smiley_face(x, y):
    gameDisplay.blit(smileyImg, (x, y))

# This function takes a parameter count, which is the number of blocks dodged by the smiley face, and then displays
# on the left side of the window the score of the player (i.e. the number of blocks dodged).


def blocks_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))

# This function takes five parameters: the block's starting x and y coordinates, its height and width, and its color.
# It then displays a rectangular block of that size and color and at that position onto the screen.


def blocks(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

# This function gets called when the smiley face crashes: smiley face hits the sides of the window or smiley face hits
# an incoming block. An game over message of "You Crashed" gets displayed on the screen for five seconds and then the
# game starts again.


def crash():
    text = "You Crashed"
    font = pygame.font.Font("freesansbold.ttf", 80)
    text_surf = font.render(text, True, black)
    text_rect = text_surf.get_rect()
    text_rect.center = ((display_width/2), (display_height/3))

    gameDisplay.blit(text_surf, text_rect)
    pygame.display.update()

    time.sleep(5)

    game_loop()

# This is the game loop. The idea behind this game is that there's a smiley face that the user controls in an attempt
# to dash incoming blocks of random sizes and positions. It will continue to run until the user exits the window,
# thereby indicating that he/she wants to quit playing.


def game_loop():

    # initial coordinates for the smiley face

    x = display_width * 0.45
    y = display_height * 0.7

    # initial width, height, position, and speed of blocks

    block_width = 100
    block_height = 100
    block_x = random.randrange(0, display_width - block_width)
    block_y = -600
    block_speed = 7
    block_color = (53, 115, 255)

    # list that will store the properties of multiple blocks
    # initially, it'll only contain the properties of a single block, but as the game goes on, other block properties
    # will be appended to it.
    # NOTE: this is a list of lists

    block_list = [[block_x, block_y, block_width, block_height]]

    random_num = random.randrange(1, len(block_list) + 1)

    # this will keep track of the score (i.e. number of blocks dodged)

    dodged = 0

    game_over = False

    # this loop will continue to run until the user decides to quit the game

    while not game_over:

        # listening for events, specifically key strokes

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                quit()

        # storing list of the keys that were pressed

        keys = pygame.key.get_pressed()

        # the smiley face object will move left and right when the left and right arrow keys are pressed respectively.
        # it moves by 20 units each press to allow the smiley face to move fast since 1 unit transitions per press
        # is too slow and will cause users to lose really fast.

        if keys[pygame.K_LEFT]:
            x -= 20

        if keys[pygame.K_RIGHT]:
            x += 20

        # checking if the smiley face crashed into the sides of the window

        if x > display_width - smileyImgWidth or x < 0:
            crash()
        else:

            # setting the game screen background to a basic white color

            gameDisplay.fill(white)

            # drawing the smiley face image at the coordinates (x,y)

            smiley_face(x, y)

            # displaying the number of blocks the user has dodged so far

            blocks_dodged(dodged)

            # looping through a random selection of block properties in the list of block properties

            for i in range(random_num):

                # giving block new random rgb color
                # going from 1 to 254 to eliminate the possibility of black/white colored blocks

                r = random.randrange(1, 254)
                g = random.randrange(1, 254)
                b = random.randrange(1, 254)

                block_color = (r, g, b)
                
                # drawing the block by passing its sublist existing in the list of block properties

                blocks(block_list[i][0], block_list[i][1], block_list[i][2], block_list[i][3], block_color)

                # incrementing a block's y coordinate by block_speed's value. this will essentially make it drop down
                # the screen by block_speed pixels from its current position

                block_list[i][1] += block_speed

                # checking if the block has crossed the end of the screen

                if block_list[i][1] > display_height:

                    # incrementing dodged by 1

                    dodged += 1

                    # adjusting the block's start y position to negative it's height
                    # that way it'll automatically display onto the screen the next loop
                    # the block is given a new random x position between 0 and the display width minus its width

                    block_list[i][1] = -block_height
                    block_list[i][0] = random.randrange(0, display_width - block_list[i][2])
                    block_list[i][2] = random.randrange(50, 100)

                    checker = True

                    while checker:
                        checker = False

                        # looping through the list of lists of block properties

                        for j in range(len(block_list)):

                            # checking that the block is not the same as the block we're comparing to

                            if j != i:

                                # checking that incoming blocks don't collide with each other

                                if (block_list[i][0] < block_list[j][0] + block_list[j][2] and
                                        block_list[i][0] + block_list[i][2] > block_list[j][0]):

                                    checker = True
                                    block_list[i][0] = random.randrange(0, display_width - block_list[i][2])

                    # if the user dodges a multiple of 3 blocks, then a new block gets added to the screen

                    if dodged % 3 == 0:

                        # generating random properties for the new block

                        thingw = random.randrange(50, 100)
                        thingx = random.randrange(0, display_width - thingw)
                        thingy = -block_height

                        # new block's list of properties

                        list_element = [thingx, thingy, thingw, block_height, block_color]

                        # checking that the list of lists of block properties is less than 5 so that there aren't too
                        # many blocks being displayed on the screen, which would inevitably make the game impossible
                        # if it is less than 5, the new block gets added. Otherwise, the speed of the blocks gets
                        # incremented by 1 unit.

                        if len(block_list) < 5:
                            block_list.append(list_element)
                        else:
                            block_speed += 1

                        # generating a new random number that will be used to display a random set of blocks from the
                        # list of lists of block properties

                        new_num = random.randrange(1, len(block_list) + 1)

                        while new_num < random_num:
                            new_num = random.randrange(1, len(block_list) + 1)

                        # adjusting the previous random value with a new one

                        random_num = new_num

                # checking if the smiley face and a block have crashed

                if y < block_list[i][1] + block_list[i][3] and y + smileyImgHeight > block_list[i][1]:
                    if x < block_list[i][0] + block_list[i][2] and x + smileyImgWidth > block_list[i][0]:
                        crash()

            # updating the game display on each run

            pygame.display.update()

            clock.tick(6000)


game_loop()
