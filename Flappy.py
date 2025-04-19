import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Game Variables
bird_x, bird_y = 50, HEIGHT // 2
bird_width, bird_height = 40, 40
bird_velocity = 0
gravity = 0.5
jump_strength = -10
pipe_width = 60
pipe_gap = 150
pipe_velocity = 3
score = 0
game_over = False

# Create a font
font = pygame.font.SysFont("Arial", 32)

# Define Bird Class
class Bird:
    def __init__(self):
        self.x = bird_x
        self.y = bird_y
        self.velocity = bird_velocity
        self.width = bird_width
        self.height = bird_height

    def update(self):
        # Apply gravity
        self.velocity += gravity
        self.y += self.velocity
        # Prevent bird from going out of screen
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height

    def jump(self):
        self.velocity = jump_strength

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

# Define Pipe Class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, HEIGHT - pipe_gap - 100)
        self.width = pipe_width
        self.gap = pipe_gap

    def update(self):
        self.x -= pipe_velocity

    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.height))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.height + self.gap, self.width, HEIGHT))

    def collide(self, bird):
        if bird.x + bird.width > self.x and bird.x < self.x + self.width:
            if bird.y < self.height or bird.y + bird.height > self.height + self.gap:
                return True
        return False

# Main Game Loop
def game_loop():
    global bird, pipes, score, game_over

    bird = Bird()
    pipes = [Pipe()]

    clock = pygame.time.Clock()
    run_game = True

    while run_game:
        clock.tick(60)  # 60 FPS
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not game_over:
                    bird.jump()

        # Update bird
        bird.update()
        bird.draw(screen)

        # Update pipes
        for pipe in pipes[:]:
            pipe.update()
            pipe.draw(screen)

            # Check for collisions
            if pipe.collide(bird):
                game_over = True

            # Remove off-screen pipes
            if pipe.x + pipe.width < 0:
                pipes.remove(pipe)
                score += 1

        # Add new pipes
        if len(pipes) == 0 or pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

        # Draw the score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Game Over screen
        if game_over:
            game_over_text = font.render("Game Over!", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            restart_text = font.render("Press R to Restart", True, BLACK)
            screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 10))

            # Restart the game
            if pygame.key.get_pressed()[pygame.K_r]:
                game_over = False
                score = 0
                pipes = [Pipe()]

        pygame.display.update()

# Start the game
game_loop()

# Quit Pygame
pygame.quit()
