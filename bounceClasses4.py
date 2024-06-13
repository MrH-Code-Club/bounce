import pygame
import sys
import random
from itertools import combinations
import sounddevice as sd
import numpy as np
import threading
import time  # Import the time module for sleeping

# Initialize Pygame
pygame.init()

# Configuration parameters
width, height = 800, 600  # Screen dimensions
min_radius, max_radius = 20, 50  # Minimum and maximum ball radius
min_velocity, max_velocity = -5, 5  # Minimum and maximum initial ball velocity
max_ball_velocity = 8  # Maximum velocity for a ball after collision
frame_rate = 60  # Frame rate in frames per second
audio_duration = 0.1  # Duration of audio capture in seconds
sample_rate = 44100  # Sample rate in Hz
noise_scale_factor = 0.1  # Factor for smoothing the noise level
velocity_scale_min, velocity_scale_max = 1, 2  # Minimum and maximum velocity scaling factors
sensitivity = 0.1  # Sensitivity to noise, value between 0 and 1
compression_factor = 0.5  # Compression factor for the noise level

# Screen settings
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Bouncing Balls with Click to Randomize')

# Colors
white = (255, 255, 255)
grey = (100, 100, 100)
black = (0, 0, 0)

# Frame rate
clock = pygame.time.Clock()

# Global variable for noise level
noise_level = 0

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
            self.position.x = max(self.radius, min(self.position.x, width - self.radius))
        if self.position.y <= self.radius or self.position.y >= height - self.radius:
            self.velocity.y = -self.velocity.y
            self.position.y = max(self.radius, min(self.position.y, height - self.radius))

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
                self.velocity -= impulse * dampening
                other.velocity += impulse * dampening
                # Clamp the velocities to prevent excessive speeds
                if self.velocity.length() > max_ball_velocity:
                    self.velocity.scale_to_length(max_ball_velocity)
                if other.velocity.length() > max_ball_velocity:
                    other.velocity.scale_to_length(max_ball_velocity)

def randomize_color():
    # Generate a random color
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def randomize_velocity():
    # Generate a random velocity vector with higher speed
    return (random.randint(min_velocity, max_velocity), random.randint(min_velocity, max_velocity))

def randomize_position():
    # Generate a random position
    return (random.randint(100, width - 100), random.randint(100, height - 100))

def randomize_radius():
    # Generate a random radius
    return random.randint(min_radius, max_radius)

def sample_noise():
    global noise_level
    while True:
        recording = sd.rec(int(audio_duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
        sd.wait()
        volume_norm = np.linalg.norm(recording) * 10
        noise_level = volume_norm
        print(noise_level)
        time.sleep(3)  # Sleep for 3 seconds between samples

def compress_noise_level(noise_level, factor):
    """Apply compression to the noise level to reduce dynamic range."""
    return np.log1p(noise_level * factor) / np.log1p(factor)

# Create a list of balls
balls = [Ball(randomize_position(), randomize_radius(), randomize_velocity(), randomize_color()) for _ in range(5)]

# Start noise sampling thread
noise_thread = threading.Thread(target=sample_noise, daemon=True)
noise_thread.start()

# Main loop
running = True
smoothed_noise_level = 0
while running:
    smoothed_noise_level = smoothed_noise_level * (1 - noise_scale_factor) + noise_level * noise_scale_factor
    compressed_noise_level = compress_noise_level(smoothed_noise_level, compression_factor)
    adjusted_noise_level = compressed_noise_level * sensitivity  # Apply sensitivity factor
    velocity_scale = min(max(adjusted_noise_level / 5, velocity_scale_min), velocity_scale_max)  # Adjust the scale for more noticeable speed changes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Randomize properties for all balls on mouse click
            for ball in balls:
                ball.color = randomize_color()
                ball.velocity = pygame.Vector2(randomize_velocity())
                ball.radius = random.randint(min_radius, max_radius)
                ball.position = pygame.Vector2(randomize_position())

    # Adjust velocities based on noise level
    for ball in balls:
        ball.velocity *= velocity_scale

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
    clock.tick(frame_rate)

pygame.quit()
sys.exit()
