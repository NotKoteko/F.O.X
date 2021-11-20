import random
import pygame

from engine.python.util.video import load_image, get_screen_size, get_centered_pos
from engine.python.world.object import WorldObject
from engine.python.world.world import World
from python.objects import Fox, Tree, Bush


class RandomGeneratedWorld(World):
    def __init__(self):
        super().__init__()
        self.load()
        self.background_color = (0, 170, 0)

    def load(self, filename=None):
        screen_size = get_screen_size()

        fox = Fox(self)
        fox_pos = get_centered_pos(screen_size, fox.rect.get_size())
        fox.rect.set_pos(fox_pos[0], fox_pos[1])

        cell_size = 48
        cells_x, cells_y = screen_size[0] // cell_size - 1, screen_size[1] // cell_size
        for y in range(cells_y):
            for x in range(cells_x):
                if (x % 2 == 0 and (y == 0 or y == cells_y - 2)) or (y % 2 == 0 and (x == 0 or x == cells_x - 1)):
                    obj = Bush(self)
                    obj.add_texture("bush", load_image("bush"))
                    obj.set_texture("bush")
                    obj.rect.set_pos(x, y, 48)
                    obj.rect.set_size(2, 2, 48)
                    obj.has_collision = True
                elif random.randint(1, 100) <= 20 and x % 2 == 0 and y % 2 == 0 and 2 < x < cells_x and 2 < y < cells_y:
                    objects = ["stump" for i in range(30)] + ["tree" for i in range(20)] + ["bush" for i in range(20)]
                    obj_type = random.choice(objects)
                    obj = WorldObject(self) if obj_type == "stump" else Tree(self) if obj_type == "tree" else Bush(self)
                    obj.rect.set_pos(x, y, 48)
                    obj.rect.set_size(1, 1, 48)
                    obj.add_texture(obj_type, load_image(obj_type))
                    obj.set_texture(obj_type)

                    if obj.rect.collide_rect(fox.rect):
                        obj.kill(self)

    def update(self, time, events, pressed_keys):
        super().update(time, events, pressed_keys)
        player = self.get_player()
        if player and isinstance(player, Fox):
            player.update_direction(pressed_keys[pygame.K_w], pressed_keys[pygame.K_a],
                                    pressed_keys[pygame.K_s], pressed_keys[pygame.K_d])
            player.speed[0] = player.max_speed if pressed_keys[pygame.K_w] and not player.is_shifting \
                else player.speed[0]
            player.speed[2] = player.max_speed if pressed_keys[pygame.K_s] and not player.is_shifting \
                else player.speed[2]
            player.speed[1] = player.max_speed if pressed_keys[pygame.K_a] and not player.is_shifting \
                else player.speed[1]
            player.speed[3] = player.max_speed if pressed_keys[pygame.K_d] and not player.is_shifting \
                else player.speed[3]
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        if player.exist_time - player.shifting_time_end > 1500:
                            player.start_shifting(self)


class Menu(World):
    def __init__(self):
        super().__init__()
        self.name = "Menu"
        button = WorldObject()
        button.add_texture("default", load_image("button_start"))
        button.add_texture("focused", load_image("button_start_focused"))
        button.set_texture("default")
        button.rect.set_size(200, 70)
        pos = get_centered_pos(get_screen_size(), button.rect.get_size())
        button.rect.set_pos(pos[0], pos[1] - 100)
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
