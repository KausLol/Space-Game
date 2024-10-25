import pygame
import random

# Initialize Pygame
pygame.init()

# Constants for higher resolution
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
FPS = 60
GRAVITY = 0.2
FLAP_STRENGTH = -5
ALIEN_WIDTH = 70
ALIEN_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Load images
UFO_IMAGE = pygame.image.load("assets/spaceship2.png")  # spaceship image
SPACE_BACKGROUND = pygame.image.load("assets/space.jpeg")  # Background image
ASTEROID_IMAGE = pygame.image.load("assets/asteroids/5.png")  # Asteroid image

# Resize images if necessary
UFO_IMAGE = pygame.transform.scale(UFO_IMAGE, (50, 30))
ASTEROID_IMAGE = pygame.transform.scale(ASTEROID_IMAGE, (50, 50))


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
            return True

        return False


class Alien:
    def __init__(self, x):
        self.image = ASTEROID_IMAGE
        self.rect = self.image.get_rect(
            topleft=(x, random.randint(50, SCREEN_HEIGHT - ALIEN_HEIGHT - 50))
        )

    def update(self):
        pass


def fade(screen, fade_in=True):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)

    for alpha in range(
        0 if fade_in else 255, 256 if fade_in else -1, 1 if fade_in else -1
    ):
        fade_surface.set_alpha(alpha)
        screen.fill(BLACK)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)


def show_welcome_screen(screen):
    font = pygame.font.Font(None, 30)
    title_text = font.render(
        "You refuelled your tank to full, and are on your way to home!", True, WHITE
    )
    instruction_text = font.render(
        "However, there's a malfunction in your ship! "
        "Hit enter, and space to control!",
        True,
        WHITE,
    )

    screen.fill(BLACK)
    screen.blit(
        title_text,
        (
            SCREEN_WIDTH // 2 - title_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - title_text.get_height(),
        ),
    )
    screen.blit(
        instruction_text,
        (
            SCREEN_WIDTH // 2 - instruction_text.get_width() // 2,
            SCREEN_HEIGHT // 2 + title_text.get_height(),
        ),
    )

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False


def show_game_over_screen(screen, score):
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    instruction_text = font.render("Skill issue", True, WHITE)

    screen.fill(BLACK)
    screen.blit(
        game_over_text,
        (
            SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - game_over_text.get_height(),
        ),
    )
    screen.blit(
        score_text,
        (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2),
    )
    screen.blit(
        instruction_text,
        (
            SCREEN_WIDTH // 2 - instruction_text.get_width() // 2,
            SCREEN_HEIGHT // 2 + game_over_text.get_height(),
        ),
    )

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  # Quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False


def show_victory_screen(screen, clock):
    # Initialize font and colors
    font = pygame.font.Font(None, 48)
    text_color = WHITE

    # Create text with word wrapping
    victory_text = "Victory! You reached your home planet, Maya! Congratulations!"
    words = victory_text.split()
    lines = []
    current_line = []

    # Word wrap logic
    for word in words:
        test_line = " ".join(current_line + [word])
        test_surface = font.render(test_line, True, text_color)
        if test_surface.get_width() <= SCREEN_WIDTH - 40:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    lines.append(" ".join(current_line))

    # Create text surfaces
    text_surfaces = [font.render(line, True, text_color) for line in lines]

    # Load gif frames
    gif_frames = []
    gif_frame_count = 8
    for i in range(gif_frame_count):
        frame = pygame.image.load(f"assets/planet3_gif/frame_{i}_delay-0.17s.gif ")
        frame = pygame.transform.scale(frame, (200, 200))
        gif_frames.append(frame)

    # Animation variables
    current_frame = 0
    frame_delay = 100  # Milliseconds between frames
    last_frame_time = pygame.time.get_ticks()

    # Fade in
    fade(screen, fade_in=True)

    waiting = True
    while waiting:
        current_time = pygame.time.get_ticks()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Fade out before exiting
                    fade(screen, fade_in=False)
                    waiting = False

        # Clear screen
        screen.fill(BLACK)

        # Draw text lines
        total_text_height = sum(surface.get_height() for surface in text_surfaces)
        current_y = SCREEN_HEIGHT // 3

        for surface in text_surfaces:
            x = SCREEN_WIDTH // 2 - surface.get_width() // 2
            screen.blit(surface, (x, current_y))
            current_y += surface.get_height() + 10

        # Update and draw gif animation
        if current_time - last_frame_time >= frame_delay:
            current_frame = (current_frame + 1) % gif_frame_count
            last_frame_time = current_time

        # Draw current gif frame centered below text
        gif_x = SCREEN_WIDTH // 2 - gif_frames[current_frame].get_width() // 2
        gif_y = current_y + 30
        screen.blit(gif_frames[current_frame], (gif_x, gif_y))

        pygame.display.flip()
        clock.tick(60)


def main():
    # Set the display mode with a title bar and no special fullscreen flags
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Stellar Siege")

    clock = pygame.time.Clock()

    # Show welcome screen without fade effects before starting the game
    show_welcome_screen(screen)

    running = True

    while running:
        ufo = UFO()
        aliens = []
        score = 0

        # Increase the number of aliens from three to ten.
        for i in range(10):
            aliens.append(Alien(SCREEN_WIDTH + i * (SCREEN_WIDTH // 10)))

        while running:
            seconds_passed = (pygame.time.get_ticks()) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        ufo.flap()

            out_of_bounds = ufo.update()

            for alien in aliens:
                alien.update()

            for alien in aliens:
                alien.rect.x -= 2

                if ufo.rect.colliderect(alien.rect):
                    show_game_over_screen(screen, score)
                    running = False
                    break

                if alien.rect.x < -ALIEN_WIDTH:
                    aliens.remove(alien)
                    score += 1

                    # Check for victory condition after reaching a score of 15.
                    if score >= 12:
                        show_victory_screen(screen, clock)
                        running = False
                        break

                    aliens.append(Alien(SCREEN_WIDTH))

            if out_of_bounds:
                show_game_over_screen(screen, score)
                running = False
                break

            screen.blit(SPACE_BACKGROUND, (0, 0))
            screen.blit(ufo.image, ufo.rect)

            for alien in aliens:
                screen.blit(alien.image, alien.rect)

            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, GREEN)
            timer_text = font.render(f"Time: {int(seconds_passed)}", True, WHITE)

            screen.blit(score_text, (10, 10))
            screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 10, 10))

            # Check for victory condition after one minute (60 seconds).
            if seconds_passed >= 60:
                show_victory_screen(screen)
                running = False

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
