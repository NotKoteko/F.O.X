import random
import sys

import pygame

from engine.python.util.rect import Rect
from engine.python.util.video import load_image, scale_image
from engine.python.world.object import WorldObject
from engine.python.world.world import World
from python.objects import Fox, Tree, Bush, FireBall, MenuBackground, WallBush


class RandomGeneratedWorld(World):
    def __init__(self):
        super().__init__()
        self.load()
        self.background_color = (87, 153, 0)
        self.world_time = 0

        self.font = pygame.font.SysFont('calibri', 50, bold=True)

    def load(self, filename="map1.txt"):
        fox = Fox(self)
        fox.rect.set_pos(936, 516)
        with open(f"resources/{filename}") as file:
            for line in file.readlines():
                if line == "\n" or line == "" or line.startswith("#"):
                    continue
                info = line.rstrip("\n").split()

                obj_type = info[0].split("=")[-1]
                obj = Tree(self) if obj_type == "tree" else Bush(self) if obj_type == "bush" \
                    else FireBall(self) if obj_type == "fireball_enemy" else WallBush(self) if obj_type == "wall_bush" \
                    else WorldObject(self)
                obj.add_texture(obj_type, load_image(obj_type))
                obj.set_texture(obj_type)
                x, y, w, h = int(info[1].split("=")[-1]), int(info[2].split("=")[-1]), \
                             int(info[3].split("=")[-1]), int(info[4].split("=")[-1])
                if obj_type in ["fireball_enemy", "wall_bush"]:
                    x1, y1, x2, y2 = int(info[6].split("=")[-1]), int(info[7].split("=")[-1]),\
                                     int(info[8].split("=")[-1]), int(info[9].split("=")[-1])
                    obj.zone_rect = Rect(x1, y1, x2 - x1, y2 - y1)
                obj.rect = Rect(x, y, w, h)

    def update(self, time, events, pressed_keys):
        super().update(time, events, pressed_keys)
        self.world_time += time
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

    def draw(self, surface):
        super().draw(surface)
        hp = self.get_player().hp
        color = (0, 255, 0) if hp > 50 else (255, 255, 0) if hp > 25 else (255, 0, 0)
        surface.blit(self.font.render(f"{self.get_player().hp}", False, color), (10, 30))


class Menu(World):
    def __init__(self):
        super().__init__()
        self.name = "Menu"

        MenuBackground(self)

        button_play = WorldObject(self)
        button_play.add_texture("default", load_image("menu/buttons/play_1"))
        button_play.add_texture("focused", load_image("menu/buttons/play_2"))
        button_play.rect.set_pos(500, 800)
        button_play.rect.set_size(186, 42)

        button_quit = WorldObject(self)
        button_quit.add_texture("default", load_image("menu/buttons/quit_1"))
        button_quit.add_texture("focused", load_image("menu/buttons/quit_2"))
        button_quit.rect.set_pos(500, 860)
        button_quit.rect.set_size(186, 42)

    def update(self, time, events, pressed_keys, *args):
        self.objects()[0].update(self, time)
        self.world_time += time
        button_play = self.objects()[1]
        button_quit = self.objects()[2]
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.rect.collide_point(event.pos):
                    return RandomGeneratedWorld()
                elif button_quit.rect.collide_point(event.pos):
                    sys.exit(0)
            elif event.type == pygame.MOUSEMOTION:
                if button_play.rect.collide_point(event.pos):
                    button_play.set_texture("focused")
                else:
                    button_play.set_texture("default")

                if button_quit.rect.collide_point(event.pos):
                    button_quit.set_texture("focused")
                else:
                    button_quit.set_texture("default")
        return self

    def draw(self, surface):
        surface.fill(self.background_color)
        for obj in sorted([o for o in self], key=lambda _: _.rect.y):
            if obj != self.objects()[0]:
                if self.world_time < 67 * 20:
                    break
            rect = obj.get_texture_rect()
            image = scale_image(obj.get_texture(), rect.width, rect.height)
            self.obj_dict[obj] = surface.blit(image, (rect.x + self.cam_x, rect.y + self.cam_y))
