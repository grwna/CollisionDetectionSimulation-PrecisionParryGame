from main_game import *

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Split Second Game")
clock = pygame.time.Clock()

if __name__ == "__main__":
    pygame.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update the display
        keys = pygame.key.get_pressed()
        move_object(box1, keys, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}) # noqa

        chase_box(boss, box1, speed=5)
        collision = aabb_collision(*aabb_proximity(box1, box2))

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the rectangles
        pygame.draw.rect(screen, LIGHT_RED if collision else RED, box1)
        pygame.draw.rect(screen, LIGHT_BLUE if collision else BLUE, boss)
        draw_health_bar(screen, box=box1, health=box1_health, max_health=100, color=GREEN)
        draw_health_bar(screen, health=boss_health, max_health=100, color=RED, is_boss=True)

        health = {'box1': box1_health, 'boss': boss_health}
        health, can_parry, parry_timer = combat(keys, box1, boss, health, can_parry, parry_timer, collision)
        box1_health, boss_health = health['box1'], health['boss']

        pygame.display.flip()
        clock.tick(60)
