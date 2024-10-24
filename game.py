import pygame
from pygame.locals import *
import time
import random


def main():
    # Initialise pygame
    pygame.init()

    # Define fps
    clock = pygame.time.Clock()
    fps = 60

    # Define game variables
    rows = 4
    cols = 8
    alien_cooldown = 500  # bullet cooldown in milliseconds
    last_alien_shot = pygame.time.get_ticks()

    # Define colors
    red = (255, 0, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)

    # Window dimensions
    screen_width = 900
    screen_height = 900

    screen = pygame.display.set_mode((screen_width, screen_height))

    # Set game title
    pygame.display.set_caption("Space Game")

    # Background image
    bg = pygame.image.load("assets/space.jpeg")

    # Create a spaceship object
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

            # Draw health bar
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
                            self.rect.width * (self.health_remaining / self.health_start)
                        ),
                        10,
                    ),
                )

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
            self.image = pygame.image.load(
                "assets/aliens/" + str(random.randint(0, 4)) + ".png"
            )
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

    level_number = 1

    def create_aliens(row, col):
        for row in range(row):
            for col in range(col):
                alien = Aliens(100 + col * 100, 200 + row * 70)
                alien_group.add(alien)

    create_aliens(rows + level_number - 1, cols)

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
                alien_bullet = Alien_Bullets(
                    attacking_alien.rect.centerx, attacking_alien.rect.bottom
                )
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

            # Check for collisions between alien bullets and the spaceship
            hit_spaceship = pygame.sprite.spritecollide(
                spaceship, alien_bullet_group, True
            )
            if hit_spaceship:
                spaceship.health_remaining -= len(hit_spaceship)  # Reduce health based on hits

            # Check if all aliens are destroyed to advance levels
            if not alien_group:
                level_number += 1
                rows += level_number - 1  # Increase rows for next level
                create_aliens(rows + level_number - 1, cols)

            # Check for game over condition
            if spaceship.health_remaining <= 0:
                game_over = True

        else:
           end_screen(screen)

        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)

        pygame.display.update()

    pygame.quit()


def game_bg(screen, bg):
    screen.blit(bg, (0, 0))


def end_screen(screen):
   clock.tick(60)  
   
   # Load the spaceship image for the end screen animation.
   ship_image_path="assets/spaceship.png"
   ship_image=pygame.image.load(ship_image_path).convert_alpha()
   ship_rect=ship_image.get_rect(center=(screen.get_width()//2 ,screen.get_height()//2))
    
   font=pygame.font.Font(None ,74) 
   text_surface=font.render("byebye", True,(255 ,255 ,255)) 
   text_rect=text_surface.get_rect(center=(screen.get_width()//2 ,screen.get_height()//2 +100)) 

   ship_y_velocity=-5  
   while ship_rect.bottom > -50:  
       screen.fill((0 ,0 ,0)) 
       ship_rect.y+=ship_y_velocity 
       screen.blit(ship_image ,ship_rect) 
       screen.blit(text_surface ,text_rect) 
       pygame.display.flip() 
       clock.tick(60) 

   time.sleep(2)  
   exit()  

if __name__ == "__main__":
     main()