import pygame
import sys
import random
import time
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DOT_RADIUS = 5
TOTAL_DOTS = 100
FPS = 30
SPEED = 10
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
TIME_TO_TURN_RED = 300  # 5 minutes * 60 seconds/minute

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_COLOR = (150, 150, 150)
SLIDER_COLOR = (100, 100, 100)
SLIDER_KNOB_COLOR = (200, 200, 200)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("panic_buying")

# Create dots
dots = [{"color": BLUE,
         "radius": DOT_RADIUS,
         "pos": (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
         "velocity": (random.uniform(-SPEED, SPEED), random.uniform(-SPEED, SPEED)),
         "conformity": random.uniform(0, 1),
         "inventory_level": random.choice([0, 1]),
         "fear_of_shortage": random.uniform(0, 1),
         "anticipated_scarcity": random.uniform(0, 1),
         "media_coverage": random.uniform(0, 1),
         "herd_mentality": random.uniform(0, 1)} for _ in range(TOTAL_DOTS)]
dots[random.randint(0, TOTAL_DOTS - 1)]["color"] = RED  # Make one dot red initially

# Sliders initial positions and sizes
slider_positions = {
    "conformity": (10, 50, 200, 20),
    "inventory_level": (10, 100, 200, 20),
    "fear_of_shortage": (10, 150, 200, 20),
    "anticipated_scarcity": (10, 200, 200, 20),
    "media_coverage": (10, 250, 200, 20),
    "herd_mentality": (10, 300, 200, 20)
}

slider_values = {
    "conformity": 0.5,
    "inventory_level": 0.5,
    "fear_of_shortage": 0.5,
    "anticipated_scarcity": 0.5,
    "media_coverage": 0.5,
    "herd_mentality": 0.5
}

# Function to check collisions
def check_collisions():
    for i in range(TOTAL_DOTS):
        for j in range(i + 1, TOTAL_DOTS):
            dx = dots[i]["pos"][0] - dots[j]["pos"][0]
            dy = dots[i]["pos"][1] - dots[j]["pos"][1]
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance < (dots[i]["radius"] + dots[j]["radius"]):
                if dots[i]["color"] == BLUE and dots[j]["color"] == BLUE:
                    # Check additional logic for turning blue dot into red dot
                    if dots[i]["inventory_level"] == 1 and dots[j]["inventory_level"] == 1:
                        continue  # Do not change to red dot if inventory level is 1 for both dots
                    if dots[i]["fear_of_shortage"] == 0 and dots[j]["fear_of_shortage"] == 0:
                        continue  # Do not change to red dot if fear of shortage is 0 for both dots
                    if dots[i]["anticipated_scarcity"] == 1 or dots[j]["anticipated_scarcity"] == 1:
                        continue  # Do not change to red dot if anticipated scarcity is 1 for either dot
                    if dots[i]["media_coverage"] == 0 and dots[j]["media_coverage"] == 0:
                        continue  # Do not change to red dot if media coverage is 0 for both dots
                    if dots[i]["herd_mentality"] == 0 and dots[j]["herd_mentality"] == 0:
                        continue  # Do not change to red dot if herd mentality is 0 for both dots

                    # Change blue dots to red
                    dots[i]["color"] = RED
                    dots[j]["color"] = RED

# Function to draw buttons
def draw_buttons():
    start_button_rect = pygame.Rect(10, SCREEN_HEIGHT - 60, BUTTON_WIDTH, BUTTON_HEIGHT)
    stop_button_rect = pygame.Rect(120, SCREEN_HEIGHT - 60, BUTTON_WIDTH, BUTTON_HEIGHT)
    step_button_rect = pygame.Rect(230, SCREEN_HEIGHT - 60, BUTTON_WIDTH, BUTTON_HEIGHT)

    pygame.draw.rect(screen, BUTTON_COLOR, start_button_rect)
    pygame.draw.rect(screen, BUTTON_COLOR, stop_button_rect)
    pygame.draw.rect(screen, BUTTON_COLOR, step_button_rect)

    font = pygame.font.Font(None, 36)
    start_text = font.render("Start", True, BLACK)
    stop_text = font.render("Stop", True, BLACK)
    step_text = font.render("Step", True, BLACK)

    screen.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 10))
    screen.blit(stop_text, (stop_button_rect.x + 25, stop_button_rect.y + 10))
    screen.blit(step_text, (step_button_rect.x + 25, step_button_rect.y + 10))

    return start_button_rect, stop_button_rect, step_button_rect

# Function to draw sliders
def draw_sliders():
    for factor, pos in slider_positions.items():
        pygame.draw.rect(screen, SLIDER_COLOR, pos)
        knob_pos = (int(pos[0] + pos[2] * slider_values[factor]), pos[1])
        pygame.draw.rect(screen, SLIDER_KNOB_COLOR, (knob_pos[0] - 5, knob_pos[1], 10, pos[3]))

        font = pygame.font.Font(None, 24)
        text = font.render(factor.capitalize(), True, BLACK)
        screen.blit(text, (pos[0] + pos[2] + 10, pos[1]))

# Function to update slider values
def update_sliders(mouse_pos):
    for factor, pos in slider_positions.items():
        if pos[0] <= mouse_pos[0] <= pos[0] + pos[2] and pos[1] <= mouse_pos[1] <= pos[1] + pos[3]:
            # Calculate the relative position of the mouse within the slider
            relative_pos = (mouse_pos[0] - pos[0]) / pos[2]
            # Ensure the value is between 0 and 1
            slider_values[factor] = max(0, min(1, relative_pos))

# Main game loop
clock = pygame.time.Clock()
running = False
paused = False
start_time = time.time()  # Record the start time

# Initialize Matplotlib interactive mode
plt.ion()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            plt.ioff()  # Turn off interactive mode before exiting
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not paused:
                    running = not running
                paused = not paused
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                start_button_rect, stop_button_rect, step_button_rect = draw_buttons()
                if start_button_rect.collidepoint(mouse_pos):
                    running = True
                    paused = False
                elif stop_button_rect.collidepoint(mouse_pos):
                    running = False
                elif step_button_rect.collidepoint(mouse_pos):
                    if not paused:
                        running = False
                        paused = True
                        check_collisions()
                else:
                    update_sliders(mouse_pos)

    if running and not paused:
        elapsed_time = time.time() - start_time

        for dot in dots:
            # Update velocity to be a random value for both x and y directions
            dot["velocity"] = (random.uniform(-SPEED, SPEED), random.uniform(-SPEED, SPEED))

            dot["pos"] = (dot["pos"][0] + dot["velocity"][0], dot["pos"][1] + dot["velocity"][1])

            # Bounce off the walls
            if dot["pos"][0] < 0 or dot["pos"][0] > SCREEN_WIDTH:
                dot["velocity"] = (-dot["velocity"][0], dot["velocity"][1])
            if dot["pos"][1] < 0 or dot["pos"][1] > SCREEN_HEIGHT:
                dot["velocity"] = (dot["velocity"][0], -dot["velocity"][1])

            # Add logic to turn blue dots into red after 5 minutes with velocity 0.2
            if dot["color"] == BLUE and dot["velocity"] == (0.2, 0.2) and elapsed_time >= TIME_TO_TURN_RED:
                dot["color"] = RED

        check_collisions()

    screen.fill((255, 255, 255))

    for dot in dots:
        pygame.draw.circle(screen, dot["color"], (int(dot["pos"][0]), int(dot["pos"][1])), dot["radius"])

    # Draw buttons and get button rectangles
    start_button_rect, stop_button_rect, step_button_rect = draw_buttons()
    
    # Draw sliders
    draw_sliders()

    pygame.display.flip()
    clock.tick(FPS)
