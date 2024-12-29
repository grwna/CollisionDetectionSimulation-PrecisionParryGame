import pygame


class Pentagon:
    def __init__(self, vertices=None, bounding_box_offset=10, position="center"):
        if vertices is None:
            if position == "left":
                vertices = [(100, 200), (150, 250), (125, 300), (75, 300), (50, 250)]
            elif position == "right":
                vertices = [(500, 200), (550, 250), (525, 300), (475, 300), (450, 250)]
            else:  # Default "center"
                vertices = [(300, 200), (350, 250), (325, 300), (275, 300), (250, 250)]
        self.vertices = vertices
        self.box = self.create_bounding_box(bounding_box_offset)

    def create_bounding_box(self, bounding_box_offset):
        min_x = min(x for x, y in self.vertices) - bounding_box_offset
        max_x = max(x for x, y in self.vertices) + bounding_box_offset
        min_y = min(y for x, y in self.vertices) - bounding_box_offset
        max_y = max(y for x, y in self.vertices) + bounding_box_offset

        return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def draw(self, pentagon_color, bounding_box_color):
        pygame.draw.polygon(screen, pentagon_color, self.vertices)
        surface = pygame.Surface((self.box.width, self.box.height), pygame.SRCALPHA)
        surface.fill((*bounding_box_color, 100))  # RGBA: Add alpha transparency
        screen.blit(surface, (self.box.x, self.box.y))

    def move(self, dx, dy):
        self.vertices = [(x + dx, y + dy) for x, y in self.vertices]
        self.box.x += dx
        self.box.y += dy


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Split Second Game")
clock = pygame.time.Clock()

box1 = pygame.Rect(300, 200, 50, 50)
box2 = pygame.Rect(300, 200, 75, 75)
boss = pygame.Rect(500, 300, 90, 90)
pentagon1 = Pentagon(position="left")
pentagon2 = Pentagon(position="right")
box1_health = 100
box2_health = 100
boss_health = 100

# Parry system state
can_parry = False
parry_timer = 0
parry_cooldown = 60

RED = (255, 0, 0)
LIGHT_RED = (255, 155, 155)
BLUE = (0, 0, 255)
LIGHT_BLUE = (155, 155, 255)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def move_object(obj, keys, controls):
    dx = 0
    dy = 0
    if keys[controls['left']]:
        dx -= 5
    if keys[controls['right']]:
        dx += 5
    if keys[controls['up']]:
        dy -= 5
    if keys[controls['down']]:
        dy += 5

    if isinstance(obj, pygame.Rect):  # For default objects
        obj.x += dx
        obj.y += dy
    elif hasattr(obj, 'move'):  # For custom objects
        obj.move(dx, dy)
