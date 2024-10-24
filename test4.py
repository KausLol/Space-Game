# healthbar at top

import pygame
from pygame.locals import *
import time
import random


def main():
    # initialise pygame
    pygame.init()

    # define fps
    clock = pygame.time.Clock()
    fps = 60

    # define game variables
    rows = 5
    cols = 8
    alien_cooldown = 750  # bullet cooldown in milliseconds
    last_alien_shot = pygame.time.get_ticks()

    # define colors
    red = (255, 0, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)

    # window dimensions
    screen_width = 900
    screen_height = 900

    screen = pygame.display.set_mode((screen_width, screen_height))

    # set game title
    pygame.display.set_caption("Space Game")

    # background image
    bg = pygame.image.load("assets/space.jpeg")

    class Spaceship(pygame.sprite.Sprite):
        def __init__(self, x, y, health):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/spaceship.png")
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.health_start = health
            self.health_remaining = health
            self.last_shot = pygame.time.get_ticks()

        def update(self):
            speed = 8
            cooldown = 450
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= speed
            if key[pygame.K_RIGHT] and self.rect.right < screen_width:
                self.rect.x += speed

            time_now = pygame.time.get_ticks()
            if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
                bullet = Bullets(self.rect.centerx, self.rect.top)
                bullet_group.add(bullet)
                self.last_shot = time_now

            # Draw pixelated health bar at the top of the screen
            pixel_size = 10  # Size of each pixel in the health bar
            for i in range(self.health_start):
                if i < self.health_remaining:
                    pygame.draw.rect(screen, green, (i * pixel_size + 10, 10, pixel_size - 2, pixel_size - 2))
                else:
                    pygame.draw.rect(screen, red, (i * pixel_size + 10, 10, pixel_size - 2, pixel_size - 2))

    class Bullets(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/bullet.png")
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):
            self.rect.y -= 5
            if self.rect.bottom < 0:
                self.kill()

    class Aliens(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/aliens/" + str(random.randint(0, 4)) + ".png")
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):
            pass  # No movement logic for aliens

    class Alien_Bullets(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/alien_bullet.png")
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):
            self.rect.y += 2
            if self.rect.top > screen_height:
                self.kill()

    spaceship_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    alien_group = pygame.sprite.Group()
    alien_bullet_group = pygame.sprite.Group()

    level_number = 1

    def create_aliens(rows, cols):
        for row in range(rows):
            for col in range(cols):
                alien = Aliens(100 + col * 100, 100 + row * 70)
                alien_group.add(alien)

    create_aliens(rows + level_number - 1, cols)

    spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
    spaceship_group.add(spaceship)

    run = True
    game_over = False
    victory_message_displayed = False

    while run:
        clock.tick(fps)
        game_bg(screen, bg)

        time_now = pygame.time.get_ticks()

        if time_now - last_alien_shot > alien_cooldown:
            if len(alien_group) > 0:
                attacking_alien = random.choice(alien_group.sprites())
                alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
                alien_bullet_group.add(alien_bullet)
                last_alien_shot = time_now

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        if not game_over:
            spaceship.update()
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()

            # Check for collisions between bullets and aliens
            for bullet in bullet_group:
                hit_aliens = pygame.sprite.spritecollide(bullet, alien_group, True)
                if hit_aliens:
                    bullet.kill()  # Remove bullet on hit

                    # Check for victory condition after hitting aliens
                    if not alien_group:
                        victory_message_displayed = True

            # Check for collisions between alien bullets and the spaceship
            hit_spaceship = pygame.sprite.spritecollide(spaceship, alien_bullet_group, True)

            if hit_spaceship:
                spaceship.health_remaining -= len(hit_spaceship)  # Reduce health based on hits

                # Check for game over condition after taking damage
                if spaceship.health_remaining <= 0:
                    game_over = True

        else:
            # Display "You Lost" message when game is over
            font_loss = pygame.font.Font(None, 74)  # Create a font object with a size of your choice.
            text_surface_loss = font_loss.render('You Lost', True, white)  # Render the text.
            text_rect_loss = text_surface_loss.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text_surface_loss, text_rect_loss)  # Draw the text on the screen.

            # Pause before quitting to let players see the message.
            time.sleep(2)
            run = False

        if victory_message_displayed:
            # Display "You Won" message when all aliens are destroyed.
            font_win = pygame.font.Font(None, 74)  # Create a font object with a size of your choice.
            text_surface_win = font_win.render('You Won!', True, white)  # Render the text.
            text_rect_win = text_surface_win.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text_surface_win, text_rect_win)  # Draw the text on the screen.

            # Pause before quitting to let players see the message.
            time.sleep(2)
            run = False

        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)

        pygame.display.update()

        if game_over or victory_message_displayed:
            time.sleep(2)  # Pause before quitting to let players see the message.

    pygame.quit()


def game_bg(screen, bg):
    screen.blit(bg, (0, 0))


if __name__ == "__main__":
    main()
