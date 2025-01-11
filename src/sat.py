import sys
from src.game_logic import *


def sat_collsion(obj1, obj2):
    for normal in obj1.normals + obj2.normals:
        o1_min, o1_max = obj1.project_onto_axis(normal)
        o2_min, o2_max = obj2.project_onto_axis(normal)
        if o1_max < o2_min or o2_max < o1_min:
            return False 
    return True


if __name__ == "__main__":
    WIDTH, HEIGHT = 800, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SAT Simulation")
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.Font(None, 26)

    buttons = [
        Button(10, 400, 200, 40, "Toggle Box", toggle_bounding_box),
        Button(10, 450, 200, 40, "Toggle Normal lines", toggle_normal_lines),
    ]

    previous_show_bounding_box = state["show_bounding_box"]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Inputs
        keys = pygame.key.get_pressed()
        for button in buttons:
            button.check_click(event)

        move_object(pentagon1, keys, red_controls)
        move_object(pentagon2, keys, blue_controls)
        rotate_object(pentagon1, keys, red_controls)
        rotate_object(pentagon2, keys, blue_controls)
        pentagon1.get_normals()
        pentagon2.get_normals()

        collision = sat_collsion(pentagon1, pentagon2)

        screen.fill(BLACK)
        # Buttons Handling
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

        pentagon1.draw(LIGHT_RED if collision else RED, RED)
        pentagon2.draw(LIGHT_BLUE if collision else BLUE, BLUE)

        if (state["show_normal_lines"]):
            pentagon1.draw_normals()
            pentagon2.draw_normals()

        normals1 = [(float(round(nx, 2)), float(round(ny, 2))) for nx, ny in pentagon1.normals]
        normals2 = [(float(round(nx, 2)), float(round(ny, 2))) for nx, ny in pentagon2.normals]
        norm1_text = f"Normals 1 (x,y): {normals1}"
        norm2_text = f"Normals 2 (x,y): {normals2}"
        norm1_surface = font.render(norm1_text, True, WHITE)
        norm2_surface = font.render(norm2_text, True, WHITE)
        screen.blit(norm1_surface, (10, 10))
        screen.blit(norm2_surface, (10, 30))

        if collision:
            collision_surface = font.render("Collision!", True, WHITE)
            screen.blit(collision_surface, (WIDTH - collision_surface.get_width() - 150, 100))

        for button in buttons:
            button.draw(screen, font)

        pygame.display.flip()
        clock.tick(60)
