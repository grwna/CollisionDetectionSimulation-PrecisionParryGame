from main_game import *


if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Split Second Game")
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 26)
    finish_font = pygame.font.Font(None, 100)
    buttons = [
        Button(600, 50, 180, 40, "Toggle Box", toggle_bounding_box),
    ]
    pentagon1 = Pentagon(size="small", position="left")
    previous_show_bounding_box = state["show_bounding_box"]

    game_over = False
    game_over_text = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Game Over Logic
        if pentagon1_health <= 0 or pentagon2_health <= 0:
            game_over = True
            if pentagon1_health <= 0:
                game_over_text = "Game Over!"
            else:
                game_over_text = "You Win!"

        # Freeze Screen on Game Over
        if game_over:
            game_over_surface = finish_font.render(game_over_text, True, WHITE)
            text_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_surface, text_rect)
            pygame.display.flip()
            continue

        # Update the display
        keys = pygame.key.get_pressed()
        for button in buttons:
            button.check_click(event)

        move_object(pentagon1, keys, blue_controls)
        rotate_object(pentagon1, keys, blue_controls)
        pentagon1.get_normals()
        pentagon2.get_normals()

        chase_object(pentagon2, pentagon1, speed=5)
        collision_sat = sat_collsion(pentagon1, pentagon2)
        distance, total_half_size = aabb_proximity(pentagon1.box, pentagon2.box)
        collision_aabb = aabb_collision(distance, total_half_size)

        # Clear screen
        screen.fill(BLACK)

        if state["show_bounding_box"] != previous_show_bounding_box:
            if state["show_bounding_box"]:
                pentagon1.create_bounding_box()
                pentagon2.create_bounding_box()
            else:
                pentagon1.box.width = 0
                pentagon1.box.height = 0
                pentagon2.box.width = 0
                pentagon2.box.height = 0

            previous_show_bounding_box = state["show_bounding_box"]

        pentagon1.draw(LIGHT_RED if collision_sat else RED, LIGHT_RED if collision_aabb else RED)
        pentagon2.draw(LIGHT_BLUE if collision_sat else BLUE, LIGHT_BLUE if collision_aabb else BLUE)

        draw_health_bar(screen, pentagon=pentagon1, health=pentagon1_health, max_health=100)
        draw_health_bar(screen, health=pentagon2_health, max_health=100, is_boss=True)

        health = {'pentagon1': pentagon1_health, 'pentagon2': pentagon2_health}
        health, can_parry, parry_timer = combat(keys, font, pentagon1, pentagon2, health,
                                                can_parry, parry_timer, collision_aabb, collision_sat)
        pentagon1_health, pentagon2_health = health['pentagon1'], health['pentagon2']

        for button in buttons:
            button.draw(screen, button_font)

        pygame.display.flip()
        clock.tick(60)
