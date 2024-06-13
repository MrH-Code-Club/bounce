import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 400, 300
screen = pygame.display.set_mode((width, height))

# Ball properties
ball_pos = [width // 2, height // 2]
ball_radius = 10
ball_speed = 2  # Let's give the ball an initial speed
ball_angle = 35  # Starting angle in degrees

# Convert speed and angle to x and y velocities
def calculate_velocity(speed, angle):
    rad_angle = math.radians(angle)
    return [
        speed * math.cos(rad_angle),
        speed * math.sin(rad_angle)  # No need to negate as we will adjust the bounce logic
    ]

# Ball bounce functions
def TBWallBounce():
    global ball_angle
    # Reflect the y-component of the angle
    ball_angle = (-ball_angle) % 360

def LRWallBounce():
    global ball_angle
    # Reflect the x-component of the angle
    ball_angle = (180 - ball_angle) % 360

# Clock to control the frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_speed = 0  # Stop the ball when space key is pressed

    # Update ball position
    velocity = calculate_velocity(ball_speed, ball_angle)
    ball_pos[0] += velocity[0]
    ball_pos[1] += velocity[1]

    # Collision detection with walls
    if ball_pos[0] <= ball_radius or ball_pos[0] >= width - ball_radius:
        LRWallBounce()
        ball_pos[0] = ball_radius if ball_pos[0] < ball_radius else width - ball_radius
    if ball_pos[1] <= ball_radius or ball_pos[1] >= height - ball_radius:
        TBWallBounce()
        ball_pos[1] = ball_radius if ball_pos[1] < ball_radius else height - ball_radius

    # Drawing
    screen.fill((255, 255, 255))  # Fill the screen with white
    pygame.draw.circle(screen, (0, 0, 0), (int(ball_pos[0]), int(ball_pos[1])), ball_radius)  # Draw the ball
    pygame.display.flip()  # Update the display

    # Cap the frame rate at 60fps
    clock.tick(60)

pygame.quit()
sys.exit()
