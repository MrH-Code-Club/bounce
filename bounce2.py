import pygame
import sys
import random 

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Bouncing Balls with Click to Randomise')

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0) 

# First ball settings
ball_pos = pygame.Vector2(width // 2 , height // 2)
ball_radius = 15
ball_vel = pygame.Vector2(5, -1)
ball_color = black 

# Second ball settings
ball2_pos = pygame.Vector2(width // 3, height // 3) 
ball2_radius = 20 
ball2_vel = pygame.Vector2(-2, 2) 
ball2_color = red 

# Frame rate
clock = pygame.time.Clock()

def move_ball(ball_pos, ball_vel, ball_radius):
    ball_pos += ball_vel
    # Check for collisions with walls
    if ball_pos.x <= ball_radius or ball_pos.x >= width - ball_radius:
        ball_vel.x = -ball_vel.x
    if ball_pos.y <= ball_radius or ball_pos.y >= height - ball_radius:
        ball_vel.y = -ball_vel.y

def draw_ball(ball_pos, ball_color, ball_radius):
    pygame.draw.circle(screen, ball_color, (int(ball_pos.x), int(ball_pos.y)), ball_radius)

def draw():
    screen.fill(white)
    draw_ball(ball_pos, ball_color, ball_radius)
    draw_ball(ball2_pos, ball2_color, ball2_radius)
    pygame.display.flip()

def randomise_velocity():
    return pygame.Vector2(random.randint(-6, 6), random.randint(-6, 6))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
                # Randomise velocity vectors for both balls
                ball_vel = randomise_velocity()
                ball2_vel = randomise_velocity()
                continue

    move_ball(ball_pos, ball_vel, ball_radius)
    move_ball(ball2_pos, ball2_vel, ball2_radius)
    draw()

    # Cap the frame rate at 60 frames per second
    clock.tick(60)

pygame.quit()
sys.exit()
