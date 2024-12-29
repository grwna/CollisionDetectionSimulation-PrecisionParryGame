from aabb import *
from game_logic import *
import pygame


def chase_box(chaser, target, speed):
    # Calculate direction vector from chaser to target
    chaser_center = np.array([chaser.x + chaser.width / 2, chaser.y + chaser.height / 2])
    target_center = np.array([target.x + target.width / 2, target.y + target.height / 2])

    direction = target_center - chaser_center
    distance = np.linalg.norm(direction)

    if distance != 0:  # Avoid zero division
        direction = direction / distance  # Normalize diretion

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


def combat(keys, box1, boss, health, can_parry, parry_timer, collision):
    distance, total_half_size = aabb_proximity(box1, boss)

    if np.all(distance <= total_half_size + 50) and parry_timer == 0:
        can_parry = True
        parry_timer = 30  # Parry window duration in frames
    if collision:
        if keys[pygame.K_SPACE] and can_parry:
            # Parry successful
            health['boss'] = max(0, health['boss'] - 10)
            print("Parry successful!")
            can_parry = False
            parry_timer = 0

            # Knockback
            knockback_dir = np.array([boss.x - box1.x, boss.y - box1.y])
            knockback_dir = knockback_dir / np.linalg.norm(knockback_dir)
            knockback_strength = 70  # Adjust strength as needed
            boss.x += int(knockback_dir[0] * knockback_strength)
            boss.y += int(knockback_dir[1] * knockback_strength)
        else:
            # No parry: reduce red box health
            health['box1'] = max(0, health['box1'] - 5)
            print("Red box damaged!")

            # Knockback
            knockback_dir = np.array([box1.x - boss.x, box1.y - boss.y])
            knockback_dir = knockback_dir / np.linalg.norm(knockback_dir)
            knockback_strength = 90
            box1.x += int(knockback_dir[0] * knockback_strength)
            box1.y += int(knockback_dir[1] * knockback_strength)

    return health, can_parry, parry_timer
