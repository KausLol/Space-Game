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
    rows = 4
    cols = 8
    alien_cooldown = 500  # bullet cooldown in milliseconds
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

            self.mask = pygame.mask.from_surface(self.image)
            pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 10))
            if self.health_remaining > 0:
                pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10),
                                                 int(self.rect.width * (self.health_remaining / self.health_start)),
                                                 10))

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
            self.move_counter = 0
            self.move_direction = 1

        def update(self):
            self.rect.x += self.move_direction
            self.move_counter += 1
            if abs(self.move_counter) > 75:
                self.move_direction *= -1
                self.move_counter *= self.move_direction

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

    create_aliens(rows, cols, alien_group, Aliens)

    spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
    spaceship_group.add(spaceship)

    run = True
    game_over = False

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

            for bullet in bullet_group:
                hit_aliens = pygame.sprite.spritecollide(bullet, alien_group, True)
                if hit_aliens:
                    bullet.kill()

            hit_spaceship = pygame.sprite.spritecollide(spaceship, alien_bullet_group, True, pygame.sprite.collide_mask)

            if hit_spaceship:
                spaceship.health_remaining -= len(hit_spaceship)

            if not alien_group:
                game2(screen, screen_width, screen_height)

            if spaceship.health_remaining <= 0:
                game_over = True

        else:
            font = pygame.font.Font(None, 74)
            text_surface = font.render("Skill Issue...", True, white)
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text_surface, text_rect)

        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)

        pygame.display.update()

    pygame.quit()


def game_bg(screen, bg):
    screen.blit(bg, (0, 0))


def create_aliens(row, col, alien_group, aliens):
    for row in range(row):
        for col in range(col):
            alien = aliens(100 + col * 100, 200 + row * 70)
            alien_group.add(alien)


def game2(screen, screen_width, screen_height):
    font = pygame.font.Font(None, 74)

    text_surface = font.render("Welcome to Another Planet", True, (255, 255, 255))

    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))

    screen.fill((0, 0, 0))

    screen.blit(text_surface, text_rect)

    pygame.display.update()

    time.sleep(3)


if __name__ == "__main__":
    main()
