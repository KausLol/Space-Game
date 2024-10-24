import pygame
import random

# Initialize Pygame
pygame.init()

# Constants for higher resolution
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.2
FLAP_STRENGTH = -8  # Increased flap strength for more levitation
ALIEN_WIDTH = 70
ALIEN_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Load images
UFO_IMAGE = pygame.image.load('assets/spaceship.png')  # UFO image
SPACE_BACKGROUND = pygame.image.load('assets/space.jpeg')  # Background image
ASTEROID_IMAGE = pygame.image.load('assets/asteroids/5.png')  # Asteroid image

# Resize images if necessary
UFO_IMAGE = pygame.transform.scale(UFO_IMAGE, (50, 30))  # Adjust size as needed
ASTEROID_IMAGE = pygame.transform.scale(ASTEROID_IMAGE, (50, 50))  # Adjust size as needed


class UFO:
    def __init__(self):
        self.image = UFO_IMAGE
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.velocity_y = 0

    def flap(self):
        self.velocity_y += FLAP_STRENGTH

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Check if the UFO goes off-screen and trigger game over if it does
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            return True  # Indicate that the UFO is out of bounds

        return False  # Indicate that the UFO is within bounds


class Alien:
    def __init__(self, x):
        self.image = ASTEROID_IMAGE
        self.rect = self.image.get_rect(topleft=(x, random.randint(50, SCREEN_HEIGHT - ALIEN_HEIGHT - 50)))

    def update(self):
        pass


def fade(screen, fade_in=True):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)

    for alpha in range(0 if fade_in else 255, 256 if fade_in else -1, 1 if fade_in else -1):
        fade_surface.set_alpha(alpha)
        screen.fill(BLACK)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)


def show_welcome_screen(screen):
    font = pygame.font.Font(None, 48)
    title_text = font.render("You are stranded", True, WHITE)
    instruction_text = font.render("and there's only one way out...", True, WHITE)

    screen.fill(BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2,
                             SCREEN_HEIGHT // 2 - title_text.get_height()))
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2,
                                   SCREEN_HEIGHT // 2 + title_text.get_height()))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  # Quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False  # Exit the welcome screen when space is pressed


def show_game_over_screen(screen, score):
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    instruction_text = font.render("Skill issue", True, WHITE)

    screen.fill(BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                 SCREEN_HEIGHT // 2 - game_over_text.get_height()))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                             SCREEN_HEIGHT // 2))
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2,
                                   SCREEN_HEIGHT // 2 + game_over_text.get_height()))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  # Quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


def show_victory_screen(screen):
    font = pygame.font.Font(None, 48)
    victory_text = font.render("You Survived!", True, GREEN)

    screen.fill(BLACK)
    screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2,
                               SCREEN_HEIGHT // 2 - victory_text.get_height()))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  # Quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


def main():
    # Set the display mode with a title bar and no special fullscreen flags
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("UFO Game")  # Set a title for the window

    clock = pygame.time.Clock()

    # Show welcome screen without fade effects before starting the game
    show_welcome_screen(screen)

    running = True
    start_ticks = pygame.time.get_ticks()  # Get the starting ticks for timer

    while running:
        ufo = UFO()
        aliens = []
        score = 0

        for i in range(3):
            aliens.append(Alien(SCREEN_WIDTH + i * (SCREEN_WIDTH // 2)))

        while running:
            seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000  # Calculate elapsed seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        ufo.flap()

            out_of_bounds = ufo.update()  # Check for out-of-bounds

            for alien in aliens:
                alien.update()

            for alien in aliens:
                alien.rect.x -= 2

                if ufo.rect.colliderect(alien.rect):
                    show_game_over_screen(screen, score)
                    break

                if alien.rect.x < -ALIEN_WIDTH:
                    aliens.remove(alien)
                    score += 1
                    aliens.append(Alien(SCREEN_WIDTH))

            # If the UFO is out of bounds trigger game over screen
            if out_of_bounds:
                show_game_over_screen(screen, score)
                break

            # Draw background first
            screen.blit(SPACE_BACKGROUND, (0, 0))

            # Draw UFO and asteroids
            screen.blit(ufo.image, ufo.rect)

            for alien in aliens:
                screen.blit(alien.image, alien.rect)

            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {score}', True, GREEN)
            timer_text = font.render(f'Time: {int(seconds_passed)}', True, WHITE)  # Display timer

            screen.blit(score_text, (10, 10))
            screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 10, 10))  # Position timer

            # Check for victory condition after one minute (60 seconds)
            if seconds_passed >= 60:
                show_victory_screen(screen)
                running = False

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
