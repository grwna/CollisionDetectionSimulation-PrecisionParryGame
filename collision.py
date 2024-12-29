import pygame
import numpy as np
import sys


# AABB Collision
def aabb_collision(box1, box2):
    # Get centers of bounding boxes
    center1 = np.array([box1.x + box1.width / 2, box1.y + box1.height / 2])
    center2 = np.array([box2.x + box2.width / 2, box2.y + box2.height / 2])

    # Calculate half-sizes
    half_size1 = np.array([box1.width / 2, box1.height / 2])
    half_size2 = np.array([box2.width / 2, box2.height / 2])

    # Distance between centers
    distance = np.abs(center1 - center2)

    # Sum of half-sizes along each axis
    total_half_size = half_size1 + half_size2

    # Check for collision (distance <= total_half_size)
    return distance, total_half_size


def move_box(box, keys, controls):
    if keys[controls['left']]:
        box.x -= 5
    if keys[controls['right']]:
        box.x += 5
    if keys[controls['up']]:
        box.y -= 5
    if keys[controls['down']]:
        box.y += 5


def chase_box(chaser, target, speed):
    # Calculate direction vector from chaser to target
    chaser_center = np.array([chaser.x + chaser.width / 2, chaser.y + chaser.height / 2])
    target_center = np.array([target.x + target.width / 2, target.y + target.height / 2])

    direction = target_center - chaser_center
    distance = np.linalg.norm(direction)

    if distance != 0:  # Avoid division by zero
        direction = direction / distance  # Normalize direction vector

    # Move the chaser towards the target
    chaser.x += int(direction[0] * speed)
    chaser.y += int(direction[1] * speed)


def draw_health_bar(screen, box=None, health=100, max_health=100, color=(0, 0, 255), bar_width=400, bar_height=20, is_boss=False):  # noqa
    health_ratio = health / max_health

    if is_boss:
        # Boss health bar
        bar_width = 400
        bar_height = 20
        bar_x = (screen.get_width() - bar_width) // 2
        bar_y = screen.get_height() - 50
    else:
        # Player health bar
        bar_width = 100
        bar_height = 10
        bar_x = box.x + (box.width - bar_width) // 2
        bar_y = box.y - 15

    pygame.draw.rect(screen, (50, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, color, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))


def combat(keys, box1, box2, health, can_parry, parry_timer, collision):
    distance, total_half_size = aabb_collision(box1, box2)

    if np.all(distance <= total_half_size + 50) and parry_timer == 0:
        can_parry = True
        parry_timer = 30  # Parry window duration in frames
    if collision:
        if keys[pygame.K_SPACE] and can_parry:
            # Parry successful
            health['box2'] = max(0, health['box2'] - 10)
            print("Parry successful!")
            can_parry = False
            parry_timer = 0

            # Knockback
            knockback_dir = np.array([box2.x - box1.x, box2.y - box1.y])
            knockback_dir = knockback_dir / np.linalg.norm(knockback_dir)
            knockback_strength = 70  # Adjust strength as needed
            box2.x += int(knockback_dir[0] * knockback_strength)
            box2.y += int(knockback_dir[1] * knockback_strength)
        else:
            # No parry: reduce red box health
            health['box1'] = max(0, health['box1'] - 5)
            print("Red box damaged!")

            # Knockback
            knockback_dir = np.array([box1.x - box2.x, box1.y - box2.y])
            knockback_dir = knockback_dir / np.linalg.norm(knockback_dir)
            knockback_strength = 90
            box1.x += int(knockback_dir[0] * knockback_strength)
            box1.y += int(knockback_dir[1] * knockback_strength)

    return health, can_parry, parry_timer


if __name__ == "__main__":
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Collision Detection")
    clock = pygame.time.Clock()

    box1 = pygame.Rect(300, 200, 50, 50)  # x, y, width, height
    box2 = pygame.Rect(500, 300, 75, 75)
    box1_health = 100
    box2_health = 100

    # Parry system state
    can_parry = False
    parry_timer = 0
    parry_cooldown = 60

    RED = (255, 0, 0)
    LIGHT_RED = (255, 102, 102)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (102, 102, 255)
    GREEN = (0, 255, 0)
    PURPLE = (255, 0, 255)
    BLACK = (0, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update the display
        keys = pygame.key.get_pressed()
        move_box(box1, keys, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN})
        move_box(box2, keys, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s})

        chase_box(box2, box1, speed=5)
        distance, total_half_size = aabb_collision(box1, box2)
        collision = np.all(distance <= total_half_size)

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the rectangles
        pygame.draw.rect(screen, LIGHT_RED if collision else RED, box1)  # Draw box1 in red
        pygame.draw.rect(screen, LIGHT_BLUE if collision else BLUE, box2)  # Draw box2 in blue
        draw_health_bar(screen, box=box1, health=box1_health, max_health=100, color=GREEN)
        draw_health_bar(screen, health=box2_health, max_health=100, color=RED, is_boss=True)

        health = {'box1': box1_health, 'box2': box2_health}
        health, can_parry, parry_timer = combat(keys, box1, box2, health, can_parry, parry_timer, collision)
        box1_health, box2_health = health['box1'], health['box2']

        pygame.display.flip()
        clock.tick(60)
