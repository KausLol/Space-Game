import pygame
from pygame.locals import *
import time
import random
import subprocess
import sys


# noinspection PyTypeChecker
def main():
    # initialise pygame
    pygame.init()

    # define fps
    clock = pygame.time.Clock()
    fps = 60

    # define game variables
    rows = 4
    cols = 8
    alien_cooldown = 10000  # bullet cooldown in milliseconds
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

    # create a spaceship object
    # noinspection PyShadowingNames,PyTypeChecker,PyAttributeOutsideInit
    class Spaceship(pygame.sprite.Sprite):
        def __init__(self, x, y, health):

            # initialise spaceship as a sprite
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/spaceship.png")

            # convert sprite into a rectangle object
            self.rect = self.image.get_rect()

            # position it in center
            self.rect.center = [x, y]

            # spaceship health
            self.health_start = health
            self.health_remaining = health

            # notes when was last bullet created (to prevent bullet spam)
            self.last_shot = pygame.time.get_ticks()

        def update(self):
            # set movement speed
            speed = 8

            # set cooldown
            cooldown = 0

            # get keypress
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= speed
            if key[pygame.K_RIGHT] and self.rect.right < screen_width:
                self.rect.x += speed

            # record current time to prevent bullet spam
            time_now = pygame.time.get_ticks()

            # shooting functionality
            if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
                bullet = Bullets(self.rect.centerx, self.rect.top)
                bullet_group.add(bullet)

                # restarts cooldown timer
                self.last_shot = time_now

            # adjusts spaceship hit-box (update mask)
            self.mask = pygame.mask.from_surface(self.image)

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

    # create bullets as objects
    class Bullets(pygame.sprite.Sprite):
        def __init__(self, x, y):

            # initialise bullets as sprites
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/bullet.png")

            # convert bullet into a rectangle object
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):
            self.rect.y -= 5

            # deletes bullets from game if they leave the screen
            if self.rect.bottom < 0:
                self.kill()

    # create alien as an object
    class Aliens(pygame.sprite.Sprite):
        def __init__(self, x, y):

            # initialise alien as a sprite
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(
                "assets/aliens/" + str(random.randint(0, 4)) + ".png"
            )

            # set alien as a rectangle object
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

    # create aliens bullets as objects
    class Alien_Bullets(pygame.sprite.Sprite):
        def __init__(self, x, y):

            # initialise alien bullets as sprites
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/alien_bullet.png")

            # convert alien bullets into rectangle objects
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):
            self.rect.y += 2

            # deletes bullets when they leave the screen
            if self.rect.top > screen_height:
                self.kill()

    # create sprite groups
    spaceship_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    alien_group = pygame.sprite.Group()
    alien_bullet_group = pygame.sprite.Group()

    create_aliens(rows, cols, alien_group, Aliens)

    # create player with initial health as 3
    spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
    spaceship_group.add(spaceship)

    # Show welcome screen before starting the game
    show_welcome_screen(screen, screen_width, screen_height)

    # game status
    run = True
    game_over = False

    while run:

        # sets fps
        clock.tick(fps)

        # draws background
        game_bg(screen, bg)

        # create random alien bullets
        # records current time
        time_now = pygame.time.get_ticks()

        # shoot bullets
        if time_now - last_alien_shot > alien_cooldown:
            if len(alien_group) > 0:

                # pick a random alien
                attacking_alien = random.choice(alien_group.sprites())

                alien_bullet = Alien_Bullets(
                    attacking_alien.rect.centerx, attacking_alien.rect.bottom
                )
                alien_bullet_group.add(alien_bullet)

                # reset cooldown
                last_alien_shot = time_now

        # event handlers
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        # updates sprite groups
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

            # Check for collisions between alien bullets and the spaceship
            hit_spaceship = pygame.sprite.spritecollide(
                spaceship, alien_bullet_group, True, pygame.sprite.collide_mask
            )

            # reduce health based on hits
            if hit_spaceship:
                spaceship.health_remaining -= len(
                    hit_spaceship
                )

            # Check if all aliens are destroyed to advance levels
            if not alien_group:
                win_message_1(screen, screen_width, screen_height)

            # Check for game over condition
            if spaceship.health_remaining <= 0:
                game_over = True

        else:
            # Display a message when game is over
            font = pygame.font.Font(
                None, 74
            )

            # renders the text
            text_surface = font.render(
                "Skill Issue...", True, white
            )

            # Center the text on the screen.
            text_rect = text_surface.get_rect(
                center=(screen_width // 2, screen_height // 2)
            )

            # draw text on screen
            screen.blit(text_surface, text_rect)

        # draw sprite groups
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)

        # updates the game
        pygame.display.update()

    pygame.quit()


# sets image as a game background
def game_bg(screen, bg):
    screen.blit(bg, (0, 0))


# to create aliens
def create_aliens(rows, cols, alien_group, aliens):
    for row in range(rows):
        for col in range(cols):
            alien = aliens(100 + col * 100, 200 + row * 70)
            alien_group.add(alien)


# shows welcome screen
def show_welcome_screen(screen, screen_width, screen_height):
    font = pygame.font.Font(None, 50)

    # load the main alien image
    alien_image = pygame.image.load("assets/main_alien.png")

    # define padding between text and image
    padding = 50  # 50 pixels of space between the text and the image

    # define the upward shift
    upward_shift = 100

    # position the alien image below the text with padding and upward shift
    alien_image_rect = alien_image.get_rect(
        center=(screen_width // 2, (screen_height // 2) + 100 + padding - upward_shift)
    )

    # updated welcome message text
    text_surface = font.render("You have encountered Alien bandits. Defeat them!", True, (255, 255, 255))
    text_rect = text_surface.get_rect(
        center=(screen_width // 2, (screen_height // 2) - upward_shift)
    )

    # fade-in effect
    alpha_value = 0

    while alpha_value < 255:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN and event.key == K_RETURN:
                fade_out_text(screen, text_surface, alien_image, alien_image_rect)
                return

        screen.fill((0, 0, 0))

        text_surface.set_alpha(alpha_value)
        screen.blit(text_surface, text_rect)
        alien_image.set_alpha(alpha_value)  # fade-in the alien image as well
        screen.blit(alien_image, alien_image_rect)  # display the alien image with padding

        alpha_value += 5
        if alpha_value > 255:
            alpha_value = 255

        pygame.display.update()
        time.sleep(0.03)

    # wait for Enter key to start fading out
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN and event.key == K_RETURN:
                fade_out_text(screen, text_surface, alien_image, alien_image_rect)
                return

        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        screen.blit(alien_image, alien_image_rect)  # display the alien image with padding

        pygame.display.update()


# to fade out text
def fade_out_text(screen, text_surface, alien_image, alien_image_rect):
    # get the text's rectangle for proper positioning
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))

    # apply fade-out effect
    for alpha in range(255, -1, -5):
        text_surface.set_alpha(alpha)
        alien_image.set_alpha(alpha)  # set the same alpha to the alien image

        # fill the screen with black to reset the background
        screen.fill((0, 0, 0))

        # redraw the text and image at their respective positions
        screen.blit(text_surface, text_rect)
        screen.blit(alien_image, alien_image_rect)

        pygame.display.update()
        time.sleep(0.02)


# to proceed to the next level
def win_message_1(screen, screen_width, screen_height):
    # load GIF frames (assuming you have frames saved as individual images)
    gif_frames = [pygame.image.load(f"assets/planet1_gif/frame_{i}_delay-0.17s.png") for i in range(59)]
    gif_index = 0
    gif_timer = pygame.time.get_ticks()

    # load victory message text
    font = pygame.font.Font(None, 50)
    text_surface = font.render("Victory! You can proceed to Planet Solaris...", True, (255, 255, 255))

    # get the position for the text
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

    # set up the position for the GIF (below the text)
    gif_rect = gif_frames[0].get_rect(center=(screen_width // 2, screen_height // 2 + 50))

    # fade-in effect
    alpha_value = 0
    while alpha_value < 255:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        # fill the screen with black
        screen.fill((0, 0, 0))

        # set alpha for the text and gif
        text_surface.set_alpha(alpha_value)
        gif_frames[gif_index].set_alpha(alpha_value)

        # draw text and gif on the screen
        screen.blit(text_surface, text_rect)
        screen.blit(gif_frames[gif_index], gif_rect)

        # update alpha value
        alpha_value += 5
        pygame.display.update()
        time.sleep(0.03)

    # main display loop for the GIF and message
    display_duration = 2  # Display duration in seconds
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < display_duration * 1000:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        # fill the screen with black
        screen.fill((0, 0, 0))

        # draw the text and current frame of the GIF
        screen.blit(text_surface, text_rect)
        screen.blit(gif_frames[gif_index], gif_rect)

        # update GIF frame every 100 ms
        if pygame.time.get_ticks() - gif_timer > 100:
            gif_index = (gif_index + 1) % len(gif_frames)
            gif_timer = pygame.time.get_ticks()

        pygame.display.update()

    # fade-out effect
    for alpha in range(255, -1, -5):
        # set the fading alpha for both text and GIF
        text_surface.set_alpha(alpha)
        gif_frames[gif_index].set_alpha(alpha)

        # fill the screen with black
        screen.fill((0, 0, 0))

        # redraw the text and gif with decreasing alpha
        screen.blit(text_surface, text_rect)
        screen.blit(gif_frames[gif_index], gif_rect)

        pygame.display.update()
        time.sleep(0.01)

    # start maze after fading out
    subprocess.run(["python", "maze.py"])
    sys.exit()


if __name__ == "__main__":
    main()
