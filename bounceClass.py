import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 1200, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Bouncing Balls with Click to Randomize')

# Colors
white = (255, 255, 255)
grey = (100, 100, 100)
black = (0, 0, 0)

# Frame rate
clock = pygame.time.Clock()

class Ball:
    def __init__(self, position, radius, velocity, color):
        self.position = pygame.Vector2(position)
        self.radius = radius
        self.velocity = pygame.Vector2(velocity)
        self.color = color

    def move(self):
        # Move the ball and check for collisions with walls
        self.position += self.velocity
        if self.position.x <= self.radius or self.position.x >= width - self.radius:
            self.velocity.x = -self.velocity.x
        if self.position.y <= self.radius or self.position.y >= height - self.radius:
            self.velocity.y = -self.velocity.y

    def draw(self):
        # Draw the ball
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

def random_color():
    # Generate a random color
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def randomize_velocity():
    # Generate a random velocity vector
    return (random.randint(-6, 6), random.randint(-6, 6))

# Create a list of balls
balls = [Ball((random.randint(100, width - 100), random.randint(100, height - 100)), random.randint(20, 70), randomize_velocity(), random_color()) for _ in range(10)]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Randomize velocity vectors for all balls on mouse click
            for ball in balls:
                ball.color = random_color()
                ball.velocity = pygame.Vector2(randomize_velocity())
                ball.radius = random.randint(30,150)

    # Move and draw all balls
    screen.fill(black)
    for ball in balls:
        ball.move()
        ball.draw()
    pygame.display.flip()

    # Cap the frame rate at 60 frames per second
    clock.tick(60)

pygame.quit()
sys.exit()
