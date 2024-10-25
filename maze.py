import pygame
import random
import os
import subprocess
import sys

# initialize Pygame
pygame.init()

# constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
CELL_SIZE = 30
MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
MAZE_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
BLACK = (0, 0, 0)

# initialise font globally
font = pygame.font.Font(None, 36)

# Load images
spaceship_img = pygame.image.load("assets/spaceship_small.png")
spaceship_img = pygame.transform.scale(spaceship_img, (CELL_SIZE, CELL_SIZE))
planet_img = pygame.image.load("assets/planet2_small(1).png")
planet_img = pygame.transform.scale(planet_img, (CELL_SIZE, CELL_SIZE))

# Load asteroid images
asteroid_images = [
    pygame.transform.scale(
        pygame.image.load(f"assets/asteroids_small/{i}.png"), (CELL_SIZE, CELL_SIZE)
    )
    for i in range(1, 6)
]


# Load individual frame images for gif
def load_gif(image_folder):
    images = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith((".gif", ".png", ".jpg")):
            img = pygame.image.load(os.path.join(image_folder, filename))
            images.append(img.convert_alpha())
            print(f"Loaded: {filename}")
    return images


# Fade effect
def fade_surface(surface, fade_in=True):
    fade_surface = surface.copy()
    for alpha in range(0, 255, 5) if fade_in else range(255, 0, -5):
        fade_surface.set_alpha(alpha)
        yield fade_surface
        pygame.time.delay(20)


# Function to display Screen 1
# noinspection PyUnusedLocal
def screen_1(screen, clock, font):
    font = pygame.font.Font(None, 36)
    text1 = (
        "Planet Solaris is a colossal crimson gas giant, whose turbulent storms paint spiral patterns across "
        "its massive surface, like brushstrokes of fire."
    )
    text2 = "The planet is abundant in Celestial element. You decide to take some home!"

    # Load GIF images
    planet_images = load_gif("assets/planet1_gif")
    planet_index = 0
    frame_delay = 100
    last_frame_update = pygame.time.get_ticks()

    # Initialize alpha value for fade effect
    alpha = 0
    fade_speed = 3

    # Create surfaces for text
    wrapped_text1 = wrap_text(text1, font, SCREEN_WIDTH - 40)
    wrapped_text2 = wrap_text(text2, font, SCREEN_WIDTH - 40)

    # Create surfaces for the text elements
    text1_surfaces = []
    text2_surfaces = []

    for line in wrapped_text1:
        text_surface = font.render(line, True, (255, 255, 255))
        text_surface = text_surface.convert_alpha()
        text1_surfaces.append(text_surface)

    for line in wrapped_text2:
        text_surface = font.render(line, True, (255, 255, 255))
        text_surface = text_surface.convert_alpha()
        text2_surfaces.append(text_surface)

    # Main animation loop
    animation_done = False
    fade_out = False
    while not animation_done:
        screen.fill(BLACK)
        current_time = pygame.time.get_ticks()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    fade_out = True

        # Update GIF frame
        if current_time - last_frame_update > frame_delay:
            last_frame_update = current_time
            planet_index = (planet_index + 1) % len(planet_images)

        # Fade in/out logic
        if not fade_out:
            alpha = min(255, alpha + fade_speed)
        else:
            alpha = max(0, alpha - fade_speed)
            if alpha == 0:
                animation_done = True

        # Draw text1 with current alpha
        for i, surface in enumerate(text1_surfaces):
            temp_surface = surface.copy()
            temp_surface.set_alpha(alpha)
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 40))
            screen.blit(temp_surface, text_rect)

        # Draw planet with current alpha
        planet_surface = planet_images[planet_index].copy()
        planet_surface.set_alpha(alpha)
        screen.blit(
            planet_surface,
            (
                SCREEN_WIDTH // 2 - planet_surface.get_width() // 2,
                SCREEN_HEIGHT // 2 - planet_surface.get_height() // 2 + 100,
            ),
        )

        # Draw text2 with current alpha
        space_between = 80
        for i, surface in enumerate(text2_surfaces):
            temp_surface = surface.copy()
            temp_surface.set_alpha(alpha)
            text_rect = surface.get_rect(
                center=(SCREEN_WIDTH // 2, 200 + i * 40 + space_between)
            )
            screen.blit(temp_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)


# Function to display Screen 2
def screen_2(screen, clock):
    font = pygame.font.Font(None, 36)
    text = (
        "You made it just in time! However, a malfunction at the refueling station has forced you to fill only "
        "25% of the fuel tank. Make your way towards the next planet in hopes of more fuel!"
    )

    # Initialize alpha value for fade effect
    alpha = 0
    fade_speed = 3

    # Create surfaces for the text elements
    wrapped_text = wrap_text(text, font, SCREEN_WIDTH - 40)
    text_surfaces = []

    for line in wrapped_text:
        text_surface = font.render(line, True, (255, 255, 255))
        text_surface = text_surface.convert_alpha()
        text_surfaces.append(text_surface)

    # Main animation loop
    animation_done = False
    fade_out = False
    while not animation_done:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    fade_out = True

        # Fade in/out logic
        if not fade_out:
            alpha = min(255, alpha + fade_speed)
        else:
            alpha = max(0, alpha - fade_speed)
            if alpha == 0:
                animation_done = True

        # Draw text with current alpha
        for i, surface in enumerate(text_surfaces):
            temp_surface = surface.copy()
            temp_surface.set_alpha(alpha)
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 40))
            screen.blit(temp_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)


# Function to display Screen 3
def screen_3(screen, clock):
    font = pygame.font.Font(None, 36)
    text = (
        "Oh no! You have encountered an unexpected asteroid belt. Navigate your way to the next planet! "
        "You have about 20 seconds before your fuel runs out!"
    )

    # Initialize alpha value for fade effect
    alpha = 0
    fade_speed = 3

    # Create surfaces for the text elements
    wrapped_text = wrap_text(text, font, SCREEN_WIDTH - 40)
    text_surfaces = []

    for line in wrapped_text:
        text_surface = font.render(line, True, (255, 255, 255))
        text_surface = text_surface.convert_alpha()
        text_surfaces.append(text_surface)

    # Main animation loop
    animation_done = False
    fade_out = False
    while not animation_done:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    fade_out = True

        # Fade in/out logic
        if not fade_out:
            alpha = min(255, alpha + fade_speed)
        else:
            alpha = max(0, alpha - fade_speed)
            if alpha == 0:
                animation_done = True

        # Draw text with current alpha
        for i, surface in enumerate(text_surfaces):
            temp_surface = surface.copy()
            temp_surface.set_alpha(alpha)
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 40))
            screen.blit(temp_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)


# Function to display Screen 3 with Victory text and GIF
def screen_4(screen, clock):
    font = pygame.font.Font(None, 36)
    text = (
        "Victory! You've successfully navigated through the asteroid belt! "
        "You can now proceed to the next planet, Rosaria!"
    )

    # Load GIF images
    gif_frames = load_gif("assets/planet2_gif")
    gif_index = 0

    # Time delay between frames in milliseconds
    frame_delay = 100
    last_frame_update = pygame.time.get_ticks()

    # Initialize alpha value for fade effect
    alpha = 0
    fade_speed = 3

    # Create surfaces for the text elements
    wrapped_text = wrap_text(text, font, SCREEN_WIDTH - 40)
    text_surfaces = []

    for line in wrapped_text:
        text_surface = font.render(line, True, (255, 255, 255))
        text_surface = text_surface.convert_alpha()
        text_surfaces.append(text_surface)

    # Main animation loop
    animation_done = False
    fade_out = False
    while not animation_done:
        screen.fill(BLACK)
        current_time = pygame.time.get_ticks()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    fade_out = True

        # Update GIF frame
        if current_time - last_frame_update > frame_delay:
            last_frame_update = current_time
            gif_index = (gif_index + 1) % len(gif_frames)

        # Fade in/out logic
        if not fade_out:
            alpha = min(255, alpha + fade_speed)
        else:
            alpha = max(0, alpha - fade_speed)
            if alpha == 0:
                animation_done = True

        # Draw text with current alpha
        for i, surface in enumerate(text_surfaces):
            temp_surface = surface.copy()
            temp_surface.set_alpha(alpha)
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 40))
            screen.blit(temp_surface, text_rect)

        # Draw GIF below the text with current alpha
        gif_surface = gif_frames[gif_index].copy()
        gif_surface.set_alpha(alpha)
        gif_rect = gif_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        )
        screen.blit(gif_surface, gif_rect)

        pygame.display.flip()
        clock.tick(60)


# Function to wrap text for display
def wrap_text(text, font, max_width):
    words = text.split(" ")
    wrapped_lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word

    wrapped_lines.append(current_line)
    return wrapped_lines


# Create Maze (Asteroid Belt)
def create_maze():
    maze = [[0] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]

    # Dictionary to store positions of asteroids and their corresponding images
    asteroid_positions = {}

    # Randomly adds obstacles, but keeps clear zones around player and destination
    # adjust number of asteroids here
    for _ in range(300):
        x = random.randint(0, MAZE_WIDTH - 1)
        y = random.randint(0, MAZE_HEIGHT - 1)

        # Ensure the starting area and the goal area are clear
        if not (
            (0 <= x <= 5 and 0 <= y <= 5)
            or (x >= MAZE_WIDTH - 6 and y >= MAZE_HEIGHT - 6)
        ):
            maze[y][x] = 1
            asteroid_positions[(x, y)] = random.choice(asteroid_images)

    # Set the planet in the bottom-right corner with buffer space
    planet_x, planet_y = MAZE_WIDTH - 1, MAZE_HEIGHT - 1
    maze[planet_y][planet_x] = 2  # Place the planet

    # Clear a larger buffer zone around the planet
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            if 0 <= planet_x + dx < MAZE_WIDTH and 0 <= planet_y + dy < MAZE_HEIGHT:
                if dx == 0 and dy == 0:
                    continue
                if maze[planet_y + dy][planet_x + dx] == 1:
                    maze[planet_y + dy][planet_x + dx] = 0

    # Clear a buffer zone around the player's starting position
    player_x, player_y = 0, 0
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            if 0 <= player_x + dx < MAZE_WIDTH and 0 <= player_y + dy < MAZE_HEIGHT:
                if dx == 0 and dy == 0:
                    continue
                if maze[player_y + dy][player_x + dx] == 1:
                    maze[player_y + dy][player_x + dx] = 0

    return maze, asteroid_positions


# Draw Maze
def draw_maze(screen, maze, asteroid_positions):
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:
                screen.blit(asteroid_positions[(x, y)], (x * CELL_SIZE, y * CELL_SIZE))
            elif maze[y][x] == 2:

                # Center the planet in the cell
                screen.blit(
                    planet_img,
                    (
                        x * CELL_SIZE + (CELL_SIZE - 50) // 2,
                        y * CELL_SIZE + (CELL_SIZE - 50) // 2,
                    ),
                )


# Player object
class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        if (
            0 <= new_x < MAZE_WIDTH
            and 0 <= new_y < MAZE_HEIGHT
            and maze[new_y][new_x] != 1
        ):
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        screen.blit(spaceship_img, (self.x * CELL_SIZE, self.y * CELL_SIZE))


# Timer object
class Timer:
    def __init__(self, countdown_time):
        self.font = pygame.font.SysFont(None, 36)
        self.start_time = pygame.time.get_ticks()
        self.countdown_time = countdown_time  # Time in seconds

    def get_time(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        remaining_time = self.countdown_time - elapsed_time // 1000
        if remaining_time < 0:
            remaining_time = 0
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        return f"Fuel runs out in: {minutes:01}:{seconds:02}"

    def draw(self, screen):
        time_text = self.font.render(self.get_time(), True, (255, 255, 255))
        screen.blit(time_text, (10, SCREEN_HEIGHT - 40))

    def is_time_up(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        remaining_time = self.countdown_time - elapsed_time // 1000
        return remaining_time <= 0


# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 36)
    pygame.display.set_caption("Stellar Siege")
    clock = pygame.time.Clock()

    # Call Screen 1
    screen_1(screen, clock, font)

    # Call Screen 2 after pressing Enter on Screen 1
    screen_2(screen, clock)

    # Call Screen 3 after pressing Enter on Screen 2
    screen_3(screen, clock)

    # After Screen 3, starts the maze game
    maze, asteroid_positions = create_maze()
    player = Player()
    countdown_time = 20
    timer = Timer(countdown_time)

    running = True
    won = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, -1, maze)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1, maze)
                elif event.key == pygame.K_LEFT:
                    player.move(-1, 0, maze)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0, maze)

        screen.fill(BLACK)
        draw_maze(screen, maze, asteroid_positions)
        player.draw(screen)
        timer.draw(screen)

        if maze[player.y][player.x] == 2:
            won = True
            running = False

        if timer.is_time_up():
            running = False

        pygame.display.flip()
        clock.tick(20)

    screen.fill(BLACK)
    if won:
        screen_4(screen, clock)

        # starts flappy ship
        subprocess.run(["python", "flappy_ship.py"])
        sys.exit()

    else:
        time_text = font.render("Skill Issue!", True, (255, 255, 255))


if __name__ == "__main__":
    main()
