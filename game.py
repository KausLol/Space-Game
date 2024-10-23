import pygame
from pygame.locals import *
import time


def main():
    # initialise pygame
    pygame.init()

    # define fps
    clock = pygame.time.Clock()
    fps = 60

    # window dimensions
    screen_width = 900
    screen_height = 900

    screen = pygame.display.set_mode((screen_width, screen_height))

    # set game title
    pygame.display.set_caption("Space Game")

    # background image
    bg = pygame.image.load("assets/space.jpeg")

    # game status
    run = True
    while run:
        # set fps
        clock.tick(fps)

        # draw background
        game_bg(screen, bg)

        # event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # update the game
        pygame.display.update()
    pygame.quit()


# sets an image as game background
def game_bg(screen, bg):
    screen.blit(bg, (0, 0))


if __name__ == '__main__':
    main()
