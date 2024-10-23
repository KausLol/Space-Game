import pygame
from pygame.locals import *
import time


def main():
    # initialise pygame
    pygame.init()

    # define fps
    clock = pygame.time.Clock()
    fps = 60

    # define colors
    red = (255, 0, 0)
    green = (0, 255, 0)

    # window dimensions
    screen_width = 900
    screen_height = 900

    screen = pygame.display.set_mode((screen_width, screen_height))

    # set game title
    pygame.display.set_caption("Space Game")

    # background image
    bg = pygame.image.load("assets/space.jpeg")

    # creating a spaceship
    class Spaceship(pygame.sprite.Sprite):
        def __init__(self, x, y, health):

            # initialises spaceship as a sprite
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/spaceship.png")

            # convert image into a rectangle object
            self.rect = self.image.get_rect()

            # positions it in the center
            self.rect.center = [x, y]

            self.health_start = health
            self.health_remaining = health

        def update(self):
            # set movement speed
            speed = 8

            # get key press
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= speed
            if key[pygame.K_RIGHT] and self.rect.right < screen_width:
                self.rect.x += speed

            # draw health bar
            pygame.draw.rect(
                screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15)
            )
            if self.health_remaining > 0:
                pygame.draw.rect(
                    screen,
                    green,
                    (
                        self.rect.x,
                        (self.rect.bottom + 10),
                        int(
                            self.rect.width
                            * (self.health_remaining / self.health_start)
                        ),
                        15,
                    ),
                )

    # create a sprite group
    spaceship_group = pygame.sprite.Group()

    # create player with initial health as 3
    spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)

    spaceship_group.add(spaceship)

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

        # update spaceship
        spaceship.update()

        # update sprite groups
        spaceship_group.draw(screen)

        # update the game
        pygame.display.update()
    pygame.quit()


# sets an image as game background
def game_bg(screen, bg):
    screen.blit(bg, (0, 0))


if __name__ == "__main__":
    main()
