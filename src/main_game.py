from src.aabb import *
from src.sat import *
from src.game_logic import *
import pygame


def chase_object(chaser, target, speed):
    rotation_speed = speed
    chaser_center = np.mean(chaser.vertices, axis=0)
    target_center = np.mean(target.vertices, axis=0)

    # Calculate direction vector and distance
    direction = target_center - chaser_center
    distance = np.linalg.norm(direction)

    if distance != 0:
        direction = direction / distance  # Normalize direction

    # Move and rotate towards target
    chaser.move(int(direction[0] * speed), int(direction[1] * speed))
    target_angle = np.degrees(np.arctan2(direction[1], direction[0])) + 90
    current_angle = chaser.rotation_angle
    angle_diff = (target_angle - current_angle + 180) % 360 - 180
    new_angle = current_angle + max(-rotation_speed, min(rotation_speed, angle_diff))

    # Update angle
    chaser.rotate(new_angle - current_angle)
    chaser.rotation_angle = new_angle


def draw_health_bar(screen, health, max_health, pentagon=None, is_boss=False):  # Reduced parameters
    health_ratio = (health - 20) / (max_health - 20)

    if is_boss:
        bar_width = 400
        bar_height = 20
        color = RED
        bar_x = (screen.get_width() - bar_width) // 2
        bar_y = screen.get_height() - 50
    else:
        # Player health bar
        bar_width = 100
        bar_height = 10
        color = GREEN
        bar_x = np.mean([v[0] for v in pentagon.vertices]) - bar_width // 2
        bar_y = np.min([v[1] for v in pentagon.vertices]) - bar_height - 5

    pygame.draw.rect(screen, (50, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Background bar
    pygame.draw.rect(screen, color, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))  # Health bar


def combat(keys, font, pentagon1, pentagon2, health, can_parry, parry_timer, collision_aabb, collision_sat):
    global parry_display_timer, hit_display_timer
    if collision_aabb:
        can_parry = True
        parry_timer = 200

    if collision_sat:
        if keys[pygame.K_SPACE] and can_parry:
            # Parry successful
            health['pentagon2'] = max(0, health['pentagon2'] - 10)
            can_parry = False
            parry_timer = 0
            if parry_display_timer == 0:
                parry_display_timer = 30
            knockback(pentagon2, pentagon1, 100)  # Knockback Boss
        else:
            # Hit
            health['pentagon1'] = max(0, health['pentagon1'] - 10)
            if hit_display_timer == 0:
                hit_display_timer = 30
            knockback(pentagon1, pentagon2, 150)  # Knockback player

    if parry_display_timer > 0 or hit_display_timer > 0:
        parry_display_timer, hit_display_timer = display_combat_text(font, parry_display_timer, hit_display_timer)
    return health, can_parry, parry_timer


def knockback(moving_pentagon, source_pentagon, strength):
    source_center = np.mean(source_pentagon.vertices, axis=0)
    moving_center = np.mean(moving_pentagon.vertices, axis=0)
    knockback_dir = moving_center - source_center
    knockback_dir = knockback_dir / np.linalg.norm(knockback_dir)
    moving_pentagon.move(int(knockback_dir[0] * strength), int(knockback_dir[1] * strength))


def display_combat_text(font, parry_display_timer, hit_display_timer):
    x, y = (350, 50)
    if parry_display_timer > 0:
        parry_surface = font.render("Parry!", True, WHITE)
        screen.blit(parry_surface, (x - 50, y))
        parry_display_timer -= 1

    if hit_display_timer > 0:
        hit_surface = font.render("Hit!", True, WHITE)
        screen.blit(hit_surface, (x + 50, y))
        hit_display_timer -= 1

    return parry_display_timer, hit_display_timer
