import random
import pygame

from engine.python.util.video import load_image
from engine.python.world.object import WorldObject
from engine.python.world.world import World
from python.objects import Fox, Tree


class RandomGeneratedWorld(World):
    def __init__(self):
        super().__init__()
        self.load()
        self.background_color = (0, 200, 0)

    def load(self, filename=None):
        Fox(self).rect.set_pos(8, 5, 48)
        for i in range(40):
            for j in range(23):
                if random.randint(1, 100) < 5 or j == 0 or j == 22 or i == 0 or i == 40:
                    if random.choice(["stump", "tree"]) == "tree":
                        obj = Tree(self)
                    else:
                        obj = WorldObject(self)
                        obj.add_texture("stump", load_image(f"stump"))
                        obj.set_texture("stump")
                    obj.rect.set_pos(i, j, 48)
                    obj.rect.set_size(1, 1, 48)

    def update(self, time, events, pressed_keys):
        super().update(time, events, pressed_keys)
        player = self.get_player()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    player.shift(self)


class Menu(World):
    def __init__(self):
        super().__init__()
        self.name = "Menu"
        button = WorldObject()
        button.add_texture("default", load_image("button_start"))
        button.add_texture("focused", load_image("button_start_focused"))
        button.set_texture("default")
        button.rect.set_pos(300, 200)
        button.rect.set_size(195, 65)
        self.add(button)

    def update(self, time, events, pressed_keys, *args):
        button = self.objects()[0]
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.rect.collide_point(event.pos):
                    return RandomGeneratedWorld()
            elif event.type == pygame.MOUSEMOTION:
                if button.rect.collide_point(event.pos):
                    button.set_texture("focused")
                else:
                    button.set_texture("default")
        return self
