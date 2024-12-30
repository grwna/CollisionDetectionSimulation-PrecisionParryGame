import pygame
import numpy as np


class Pentagon:
    def __init__(self, vertices=None, bounding_box_offset=20, position="center"):
        if vertices is None:
            if position == "left":
                vertices = [(100, 200), (150, 250), (125, 300), (75, 300), (50, 250)]
            elif position == "right":
                vertices = [(500, 200), (550, 250), (525, 300), (475, 300), (450, 250)]
            else:  # Default "center"
                vertices = [(300, 200), (350, 250), (325, 300), (275, 300), (250, 250)]
        self.vertices = vertices
        self.create_bounding_box(bounding_box_offset)

    def create_bounding_box(self, bounding_box_offset=20):
        min_x = min(x for x, y in self.vertices) - bounding_box_offset
        max_x = max(x for x, y in self.vertices) + bounding_box_offset
        min_y = min(y for x, y in self.vertices) - bounding_box_offset
        max_y = max(y for x, y in self.vertices) + bounding_box_offset

        self.box = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def get_normals(self):
        normals = []
        vertices = self.vertices
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
            edge = (x2 - x1, y2 - y1)
            normal = (-edge[1], edge[0])
            length = (normal[0]**2 + normal[1]**2)**0.5
            normals.append((normal[0] / length, normal[1] / length))  # Normalize
        self.normals = normals

    def project_onto_axis(self, axis):
        projections = [np.dot(vertex, axis) for vertex in self.vertices]
        return min(projections), max(projections)

    def draw_normals(self):
        for i, (nx, ny) in enumerate(self.normals):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % len(self.vertices)] 
            edge_midpoint = ((x1 + x2) / 2, (y1 + y2) / 2)
            normal_endpoint = (edge_midpoint[0] + nx * 20, edge_midpoint[1] + ny * 20)
            pygame.draw.line(screen, (255, 255, 0), edge_midpoint, normal_endpoint, 2)

    def draw(self, pentagon_color, bounding_box_color):
        pygame.draw.polygon(screen, pentagon_color, self.vertices)
        surface = pygame.Surface((self.box.width, self.box.height), pygame.SRCALPHA)
        surface.fill((*bounding_box_color, 100))  # RGBA: Add alpha transparency
        screen.blit(surface, (self.box.x, self.box.y))

    def move(self, dx, dy):
        self.vertices = [(x + dx, y + dy) for x, y in self.vertices]
        self.box.x += dx
        self.box.y += dy

    def rotate(self, angle):
        center_x = sum(x for x, y in self.vertices) / len(self.vertices)
        center_y = sum(y for x, y in self.vertices) / len(self.vertices)
        angle_rad = np.radians(angle)

        cos_theta = np.cos(angle_rad)
        sin_theta = np.sin(angle_rad)

        self.vertices = [
            (
                cos_theta * (x - center_x) - sin_theta * (y - center_y) + center_x,
                sin_theta * (x - center_x) + cos_theta * (y - center_y) + center_y,
            )
            for x, y in self.vertices
        ]


class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = (200, 200, 200)
        self.is_pressed = False

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        label = font.render(self.text, True, (0, 0, 0))
        screen.blit(label, (self.rect.x + 10, self.rect.y + 10))

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True  # Button is pressed

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.action()
            self.is_pressed = False


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

state = {
    "show_bounding_box": True,
    "show_normal_lines": False,
}


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

red_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN, 'ccw': pygame.K_RCTRL, 'cw': pygame.K_RSHIFT}  # noqa
blue_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s, 'ccw': pygame.K_q, 'cw': pygame.K_e}  # noqa


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


def rotate_object(obj, keys, controls):
    if hasattr(obj, 'rotate'):
        if keys[controls['ccw']]:
            obj.rotate(-5)
        if keys[controls['cw']]:
            obj.rotate(5)


def toggle_bounding_box():
    state["show_bounding_box"] = not state["show_bounding_box"]


def toggle_normal_lines():
    state["show_normal_lines"] = not state["show_normal_lines"]
