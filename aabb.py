import numpy as np
import sys
from game_logic import *


def aabb_proximity(box1, box2):
    center1 = np.array([box1.x + box1.width / 2, box1.y + box1.height / 2])
    center2 = np.array([box2.x + box2.width / 2, box2.y + box2.height / 2])
    half_size1 = np.array([box1.width / 2, box1.height / 2])
    half_size2 = np.array([box2.width / 2, box2.height / 2])

    distance = np.abs(center1 - center2)
    total_half_size = half_size1 + half_size2

    return distance, total_half_size


def aabb_collision(distance, total_half_size):
    return np.all(distance <= total_half_size)


if __name__ == "__main__":
    WIDTH, HEIGHT = 700, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AABB Simulation")
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        distance, total_half_size = aabb_proximity(pentagon1.box, pentagon2.box)
        collision = aabb_collision(distance, total_half_size)

        # Key inputs
        keys = pygame.key.get_pressed()
        move_object(pentagon1, keys, red_controls) # noqa
        move_object(pentagon2, keys, blue_controls)

        screen.fill(BLACK)
        pentagon1.draw(RED, LIGHT_RED if collision else RED)
        pentagon2.draw(BLUE, LIGHT_BLUE if collision else BLUE)

        # Display distance and half-sizes
        distance_text = f"Distance (x,y): {distance}"
        total_half_size_text = f"Total Half Size (x,y): {total_half_size}"
        distance_surface = font.render(distance_text, True, WHITE)
        total_half_size_surface = font.render(total_half_size_text, True, WHITE)
        screen.blit(distance_surface, (10, 10))
        screen.blit(total_half_size_surface, (10, 40))

        # Display "Collision!" when collision occurs
        if collision:
            collision_surface = font.render("Collision!", True, WHITE)
            screen.blit(collision_surface, (WIDTH - collision_surface.get_width() - 10, 10))

        pygame.display.flip()
        clock.tick(60)
