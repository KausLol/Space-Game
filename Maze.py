import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
CELL_SIZE = 30
MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
MAZE_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
BLACK = (0, 0, 0)

# Load images
spaceship_img = pygame.image.load('assets/spaceship_small.png')
spaceship_img = pygame.transform.scale(spaceship_img, (CELL_SIZE, CELL_SIZE))
planet_img = pygame.image.load('assets/planet2_small(1).png')
planet_img = pygame.transform.scale(planet_img, (CELL_SIZE, CELL_SIZE))

# Load asteroid images
asteroid_images = [pygame.transform.scale(pygame.image.load(f'assets/asteroids_small/{i}.png'), (CELL_SIZE, CELL_SIZE))
                   for i in range(1, 6)]  # Assuming 5 asteroid images named asteroid1.png, asteroid2.png, etc.


# Create Maze (Asteroid Belt)
def create_maze():
    maze = [[0] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
    asteroid_positions = {}  # Dictionary to store positions of asteroids and their corresponding images

    # Randomly add obstacles, but keep clear zones around player and destination
    for _ in range(300):  # Adjust the number of asteroids as needed
        x = random.randint(0, MAZE_WIDTH - 1)
        y = random.randint(0, MAZE_HEIGHT - 1)

        # Ensure the starting area (top-left) and the goal area (bottom-right) are clear
        if not ((0 <= x <= 5 and 0 <= y <= 5) or (x >= MAZE_WIDTH - 6 and y >= MAZE_HEIGHT - 6)):
            maze[y][x] = 1  # Place an asteroid
            asteroid_positions[(x, y)] = random.choice(asteroid_images)  # Assign a random image to this position

    # Set the planet (goal) in the bottom-right corner with buffer space
    planet_x, planet_y = MAZE_WIDTH - 1, MAZE_HEIGHT - 1
    maze[planet_y][planet_x] = 2  # Place the planet

    # Clear a larger buffer zone around the planet
    for dx in range(-2, 3):  # -2 to 2 for x-axis (5 cells wide)
        for dy in range(-2, 3):  # -2 to 2 for y-axis (5 cells high)
            if 0 <= planet_x + dx < MAZE_WIDTH and 0 <= planet_y + dy < MAZE_HEIGHT:
                if dx == 0 and dy == 0:  # Skip the planet's position
                    continue
                if maze[planet_y + dy][planet_x + dx] == 1:  # If there is an asteroid here, clear it
                    maze[planet_y + dy][planet_x + dx] = 0

    # Clear a buffer zone around the player's starting position
    player_x, player_y = 0, 0
    for dx in range(-2, 3):  # -2 to 2 for x-axis (5 cells wide)
        for dy in range(-2, 3):  # -2 to 2 for y-axis (5 cells high)
            if 0 <= player_x + dx < MAZE_WIDTH and 0 <= player_y + dy < MAZE_HEIGHT:
                if dx == 0 and dy == 0:  # Skip the player's position
                    continue
                if maze[player_y + dy][player_x + dx] == 1:  # If there is an asteroid here, clear it
                    maze[player_y + dy][player_x + dx] = 0

    return maze, asteroid_positions


# Draw Maze
def draw_maze(screen, maze, asteroid_positions):
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:
                screen.blit(asteroid_positions[(x, y)], (x * CELL_SIZE, y * CELL_SIZE))  # Draw assigned asteroid image
            elif maze[y][x] == 2:
                # Center the planet in the cell
                screen.blit(planet_img, (x * CELL_SIZE + (CELL_SIZE - 50) // 2, y * CELL_SIZE + (CELL_SIZE - 50) // 2))


# Player class
class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        screen.blit(spaceship_img, (self.x * CELL_SIZE, self.y * CELL_SIZE))


# Timer class
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
    pygame.display.set_caption("Asteroid Navigation Game")
    clock = pygame.time.Clock()

    maze, asteroid_positions = create_maze()  # Get both maze and asteroid positions with images

    player = Player()

    countdown_time = 20  # Countdown time set to 30 seconds
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
        draw_maze(screen, maze, asteroid_positions)  # Pass both maze and asteroid positions to draw function

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
        time_text = font.render('You Reached the Planet!', True, (255, 255, 255))
    else:
        time_text = font.render('Time is up!', True, (255, 255, 255))

    screen.blit(time_text,
                (SCREEN_WIDTH // 2 - time_text.get_width() // 2,
                 SCREEN_HEIGHT // 2 - time_text.get_height() // 2))

    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()


if __name__ == "__main__":
    main()
