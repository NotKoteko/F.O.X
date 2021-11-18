from engine.python.util.rect import Rect
from engine.python.util.video import scale_image, load_image, flip_image, add_color_filter
from engine.python.world.object import WorldObject
from engine.python.world.player import Player


# Класс лисы, наследуется от Entity (который наследуется от Object)
class Fox(Player):
    def __init__(self, world):
        super().__init__(world)     # Всё то же самое, что у LivingEntity

        self.set_size(1, 1, 48)
        self.max_speed = 300        # Устанавливаем максимальную скорость на 300 пикселей/секунда
        self.direction = 3          # Устанавливаем направление взгляда на "вправо"

        self.is_shifting = False
        self.shifting_time = 0

        # Грузит текстуры idle и walk от 1 до 8 (увеличить, если кадров больше)
        for i in range(8):          # Грузим текстуры idle и walk от 1 до 8
            self.add_texture(f"idle_0_{i}", scale_image(load_image(f"fox/idle/1_{i}"), 26, 66))
            self.add_texture(f"idle_1_{i}", scale_image(load_image(f"fox/idle/2_{i}"), 70, 48))
            self.add_texture(f"idle_2_{i}", scale_image(load_image(f"fox/idle/3_{i}"), 26, 66))
            self.add_texture(f"idle_3_{i}", flip_image(self.textures[f"idle_1_{i}"], True, False))

            self.add_texture(f"walk_0_{i}", scale_image(load_image(f"fox/walk/1_{i}"), 26, 66))
            self.add_texture(f"walk_1_{i}", scale_image(load_image(f"fox/walk/2_{i}"), 70, 48))
            self.add_texture(f"walk_2_{i}", scale_image(load_image(f"fox/walk/3_{i}"), 26, 66))
            self.add_texture(f"walk_3_{i}", flip_image(self.textures[f"walk_1_{i}"], True, False))
        self.add_texture("idle_1_blink", scale_image(load_image(f"fox/idle/2_blink"), 70, 48))
        self.add_texture("idle_2_blink", scale_image(load_image(f"fox/idle/3_blink"), 26, 66))
        self.add_texture("idle_3_blink", flip_image(self.textures["idle_1_blink"], True, False))

    def get_texture(self):
        texture_type = 'walk' if self.is_moving() else 'idle'
        texture_number = self.exist_time // 80 % 8                         # 80 - время между кадрами, 8 - кол-во
        texture_key = f"{texture_type}_{self.direction}_{texture_number}"  # Тип_Направление_номер (напр. walk_1_1)
        if self.exist_time // 80 % 80 == 0 and self.direction in (2, 4):
            texture_key = f"idle_{self.direction}_blink"
        texture = self.textures.get(texture_key, self.textures["default"])
        if self.is_shifting:
            return add_color_filter(texture, (255, 255, 255))
        return texture

    def get_texture_rect(self):
        if self.direction == 0:
            return Rect(self.rect.x + 11, self.rect.y, 26, 66)
        elif self.direction == 1:
            return Rect(self.rect.x, self.rect.y, 70, 48)
        elif self.direction == 2:
            return Rect(self.rect.x + 11, self.rect.y - (66 - self.rect.height), 26, 66)
        elif self.direction == 3:
            return Rect(self.rect.x - (70 - self.rect.width), self.rect.y, 70, 48)
        return self.rect

    def move(self, world, x, y):
        super().move(world, x, y)
        world.cam_x -= x
        world.cam_y -= y

    def update(self, world, time):
        super().update(world, time)
        if self.is_shifting:
            self.shifting_time += time
            if self.shifting_time > 200:
                self.stop_shifting(world)

    def start_shifting(self, world):
        self.speed[self.direction] = self.max_speed * 5
        self.is_shifting = True

    def stop_shifting(self, world):
        self.speed[self.direction] = self.max_speed
        self.is_shifting = False
        self.shifting_time = 0

    def update_speed(self, world, time):
        if not self.is_shifting:
            super().update_speed(world, time)


class Tree(WorldObject):
    def __init__(self, group):
        super().__init__(group)
        self.add_texture("tree", load_image("tree"))
        self.set_texture("tree")

    def get_texture_rect(self):
        size = 96, 144
        return Rect(self.rect.x - (size[0] - self.rect.width) // 2,
                    self.rect.y - (size[1] - self.rect.height), size[0], size[1])
