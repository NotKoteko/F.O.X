import pygame


class Rect:
    def __init__(self, *args):
        if len(args) == 2:
            self.x, self.y = args[0]
            self.width, self.height = args[1]
        elif len(args) == 4:
            self.x = args[0]
            self.y = args[1]
            self.width = args[2]
            self.height = args[3]

    def get_pos(self):
        return self.x, self.y

    def get_size(self):
        return self.width, self.height

    def set_pos(self, x, y, multiplier=1):
        self.x = x * multiplier
        self.y = y * multiplier

    def set_size(self, width, height, multiplier=1):
        self.width = width * multiplier
        self.height = height * multiplier

    def collide_rect(self, other) -> bool:
        if int(self.x) >= int(other.x + other.width):
            return False
        if int(self.x + self.width) <= int(other.x):
            return False
        if int(self.y) >= int(other.y + other.height):
            return False
        if int(self.y + self.height) <= int(other.y):
            return False
        return True

    def collide_point(self, point) -> bool:
        return self.x < point[0] < self.x + self.width and self.y < point[1] < self.y + self.height

    def collide_any(self, world):
        return [obj for obj in world if self.collide_rect(obj.rect) and obj != self]

    def move(self, x, y):
        return Rect(self.x + x, self.y + y, self.width, self.height)

    def to_pygame_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))
