from typing import Iterable
import pygame

from engine.python.world.object import WorldObject
from engine.python.world.player import Player


class World:
    def __init__(self):
        self.obj_dict = {}
        self.cam_x, self.cam_y = 0, 0
        self.name = None
        self.background_color = (0, 0, 0)

    def save(self, filename=None):
        pass

    def load(self, filename=None):
        pass

    def add(self, obj: WorldObject):
        self.obj_dict[obj] = 0

    def get_player(self) -> Player:
        for obj in self:
            if isinstance(obj, Player):
                return obj

    def objects(self):
        return list(self.obj_dict)

    def __iter__(self) -> Iterable[WorldObject]:
        return iter(self.objects())

    def update(self, time, events, pressed_keys):
        player = self.get_player()
        if player:
            player.update_direction(pressed_keys[pygame.K_w], pressed_keys[pygame.K_a],
                                    pressed_keys[pygame.K_s], pressed_keys[pygame.K_d])
            player.speed[0] = player.max_speed if pressed_keys[pygame.K_w] else player.speed[0]
            player.speed[2] = player.max_speed if pressed_keys[pygame.K_s] else player.speed[2]
            player.speed[1] = player.max_speed if pressed_keys[pygame.K_a] else player.speed[1]
            player.speed[3] = player.max_speed if pressed_keys[pygame.K_d] else player.speed[3]

        for obj in self:
            obj.update(self, time)
