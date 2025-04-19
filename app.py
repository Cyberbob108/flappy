import pygame
import random
import time
import streamlit as st
from pygame.locals import *
import numpy as np

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 400
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Game parameters
bird_width = 40
bird_height = 40
bird_x = 50
bird_y = HEIGHT // 2
gravity = 0.5
bird_velocity = 0
jump_strength = -10
pipe_width = 60
pipe_gap = 150
pipe_velocity = 3
score = 0

# Font for displaying text
font = pygame.font.SysFont("Arial", 30)

# Create Bird Class
class Bird:
    def __init__(self):
        self.x = bird_x
        self.y = bird_y
        self.velocity = bird_velocity
        self.width = bird_width
        self.height = bird_height

    def update(self):
        self.velocity += gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = jump_strength

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))  # Bird as a rectangle

# Create Pipe Class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, HEIGHT - pipe_gap - 100)
        self.width = pipe_width
        self.gap = pipe_gap

    def update(self):
        self.x -= pipe_velocity

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.height))  # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.height + self.gap, self.width, HEIGHT))  # Bottom pipe

    def collide(self, bird):
        if bird.x + bird.width > self.x and bird.x < self.x + self.width:
            if bird.y < self.height or bird.y + bird.height > self.height + self.gap:
                return True
        return False

# Game Loop
def game_loop():
    global score
    bird = Bird()
    pipes = [Pipe()]
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_SPACE:
                bird.jump()

        bird.update()
        bird.draw(screen)

        # Generate new pipes
        if pipes[-1].x < WIDTH - 300:
            pipes.append(Pipe())

        for pipe in pipes[:]:
            pipe.update()
            pipe.draw(screen)

            # Remove pipes that have gone off-screen
            if pipe.x < -pipe.width:
                pipes.remove(pipe)

            # Check for collision
            if pipe.collide(bird):
                running = False

            # Check for scoring
            if pipe.x + pipe.width < bird.x and not hasattr(pipe, 'scored'):
                score += 1
                pipe.scored = True

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)

    # Game over screen
    game_over_text = font.render("Game Over", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.fill(WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    time.sleep(3)

# Streamlit Interface
def streamlit_interface():
    st.title("Flappy Bird Game")
    st.write("Use the spacebar to make the bird jump and avoid the pipes!")

    if st.button("Start Game"):
        # Run the game in a new pygame window
        game_loop()
        st.write("Game Over! Press 'Start Game' to play again.")

if __name__ == "__main__":
    # Run Streamlit app and game interface
    streamlit_interface()
