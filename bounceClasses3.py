import pygame
import sys
import random
from itertools import combinations

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 1800, 870
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

    def check_collision(self, other):
        # Check collision with another ball
        delta = self.position - other.position
        distance = delta.length()
        if distance < self.radius + other.radius:
            # Calculate new velocities after collision
            collision_normal = delta.normalize()
            relative_velocity = self.velocity - other.velocity
            speed = relative_velocity.dot(collision_normal)
            if speed < 0:
                impulse = 1.1 * speed * collision_normal
                # Apply dampening to reduce energy increase
                dampening = 0.9
                self.velocity -= impulse * dampening * (2*other.radius/90)
                other.velocity += impulse * dampening* (2*self.radius/90)
                # Clamp the velocities to prevent excessive speeds
                max_velocity = 7
                if self.velocity.length() > max_velocity:
                    self.velocity.scale_to_length(max_velocity)
                if other.velocity.length() > max_velocity:
                    other.velocity.scale_to_length(max_velocity)

def randomize_color():
    # Generate a random color
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def randomize_velocity():
    # Generate a random velocity vector
    return (random.randint(-6, 6), random.randint(-6, 6))

def randomize_position():
    # Generate a random position
    return (random.randint(200, width - 200), random.randint(200, height - 200))

def randomize_radius():
    # Generate a random radius
    return (random.randint(40, 120))

# Create a list of balls
balls = [Ball(randomize_position(), randomize_radius(), randomize_velocity(), randomize_color()) for _ in range(10)]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Randomize properties for all balls on mouse click
            for ball in balls:
                ball.color = randomize_color()
                ball.velocity = pygame.Vector2(randomize_velocity())
                ball.radius = random.randint(20, 100)
                ball.position = pygame.Vector2(randomize_position())

    # Check for collisions between balls
    for ball1, ball2 in combinations(balls, 2):
        ball1.check_collision(ball2)

    # Move and draw all balls
    screen.fill(black)
    for ball in balls:
        ball.move()
        ball.draw()
    pygame.display.flip()

    # Cap the frame rate in frames per second
    clock.tick(60)

pygame.quit()
sys.exit()