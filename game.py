import pygame
from pygame.locals import *
import time
import random


# noinspection PyTypeChecker
def main():
    # initialise pygame
    pygame.init()

    # define fps
    clock = pygame.time.Clock()
    fps = 60

    # define game variables
    rows = 5
    cols = 8

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
    # noinspection PyTypeChecker
    class Spaceship(pygame.sprite.Sprite):
        def __init__(self, x, y, health):

            # initialises spaceship as a sprite
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/spaceship.png")

            # convert sprite into a rectangle object
            self.rect = self.image.get_rect()

            # positions it in the center
            self.rect.center = [x, y]

            self.health_start = health
            self.health_remaining = health

            # notes when was last bullet created (to prevent bullet spam)
            self.last_shot = pygame.time.get_ticks()

        def update(self):
            # set movement speed
            speed = 8

            # cooldown variable in milliseconds
            cooldown = 450

            # get key press
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= speed
            if key[pygame.K_RIGHT] and self.rect.right < screen_width:
                self.rect.x += speed

            # record current time (to prevent bullet spam)
            time_now = pygame.time.get_ticks()

            # shooting functionality
            if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
                bullet = Bullets(self.rect.centerx, self.rect.top)
                bullet_group.add(bullet)

                # restarts cooldown timer
                self.last_shot = time_now

            # draw health bar
            pygame.draw.rect(
                screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 10)
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
                        10,
                    ),
                )

    # create bullets
    class Bullets(pygame.sprite.Sprite):
        def __init__(self, x, y):

            # initialises bullet as a sprite
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/bullet.png")

            # convert the sprite into a rectangle object
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):
            self.rect.y -= 5

            # deletes bullets from the group when they leave the screen
            if self.rect.bottom < 0:
                self.kill()

    # create asteroids
    class Aliens(pygame.sprite.Sprite):
        def __init__(self, x, y):

            # initialises aliens as a sprite
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/aliens/" + str(random.randint(0,4)) + ".png")

            # converts sprites into rectangle objects
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

            # movement of aliens
            self.move_counter = 0
            self.move_direction = 1

        def update(self):
            self.rect.x += self.move_direction
            self.move_counter += 1
            if abs(self.move_counter) > 75:
                self.move_direction *= -1
                self.move_counter *= self.move_direction

    # create a sprite group
    spaceship_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    alien_group = pygame.sprite.Group()

    create_aliens(rows, cols, Aliens, alien_group)

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
        bullet_group.update()
        alien_group.update()

        # draw sprite groups
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)

        # update the game
        pygame.display.update()
    pygame.quit()


# sets an image as game background
def game_bg(screen, bg):
    screen.blit(bg, (0, 0))


# to create aliens
def create_aliens(rows, cols, aliens, alien_group):
    for row in range(rows):
        for col in range(cols):
            alien = aliens(100 + col * 100, 100 + row * 70)
            alien_group.add(alien)


if __name__ == "__main__":
    main()
