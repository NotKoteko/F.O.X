from typing import Iterable
import pygame

from engine.python.util.video import scale_image
from engine.python.world.object import WorldObject
from engine.python.world.player import Player


class World:
    def __init__(self):
        self.obj_dict = {}
        self.cam_x, self.cam_y = 0, 0
        self.name = None
        self.background_color = (0, 0, 0)
        self.world_time = 0

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
        self.world_time += time
        for obj in self:
            obj.update(self, time)

    def draw(self, surface):
        surface.fill(self.background_color)
        player = self.get_player()
        for obj in sorted([o for o in self], key=lambda _: _.rect.y):
            if not obj.is_visible:
                continue
            rect = obj.get_texture_rect()
            image = scale_image(obj.get_texture(), rect.width, rect.height)
            if player:
                if obj != player:
                    player_rect = player.get_texture_rect()
                    if rect.collide_rect(player_rect):
                        image.set_alpha(220)
            self.obj_dict[obj] = surface.blit(image, (rect.x + self.cam_x, rect.y + self.cam_y))
