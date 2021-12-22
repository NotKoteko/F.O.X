from engine.python.util.rect import Rect
from engine.python.util.video import scale_image, load_image, flip_image, add_color_filter
from engine.python.world.entity_living import EntityLiving
from engine.python.world.object import WorldObject
from engine.python.world.player import Player


# Класс лисы, наследуется от Entity (который наследуется от Object)
class Fox(Player):
    def __init__(self, world):
        super().__init__(world)     # Всё то же самое, что у LivingEntity

        self.rect.set_size(1, 1, 48)
        self.max_speed = 300        # Устанавливаем максимальную скорость на 300 пикселей/секунда
        self.direction = 3          # Устанавливаем направление взгляда на "вправо"

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


class Tree(WorldObject):
    def __init__(self, world):
        super().__init__(world)
        self.rect.set_size(48, 24)

    def get_texture_rect(self):
        size = 96, 144
        return Rect(self.rect.x - (size[0] - self.rect.width) // 2,
                    self.rect.y - (size[1] - self.rect.height - 16), size[0], size[1])


class Bush(WorldObject):
    def __init__(self, world):
        super().__init__(world)
        self.rect.set_size(24, 24)
        self.has_collision = True

    def get_texture_rect(self):
        size = 96, 96
        return Rect(self.rect.x - (size[0] - self.rect.width) // 2,
                    self.rect.y - (size[1] - self.rect.height + -16), size[0], size[1])


class MenuBackground(WorldObject):
    def __init__(self, world):
        super().__init__(world)
        for i in range(1, 68):
            self.add_texture(f"mm_{i}", load_image(f"menu/mm_{i}"))
            self.rect.set_pos(0, 0)
            self.rect.set_size(1920, 1080)

    def get_texture(self):
        if self.exist_time < 67 * 20:
            texture_number = self.exist_time // 20 % 67
        else:
            texture_number = 66 if self.exist_time // 500 % 2 == 0 else 67
        texture = self.textures.get(f"mm_{texture_number}", self.textures["default"])
        return texture

    def get_texture_rect(self):
        return Rect(0, 0, 1920, 1080)


class FireBall(EntityLiving):
    def __init__(self, world):
        super().__init__(world)
        self.max_speed = 100
        self.direction = 1
        self.has_collision = False
        self.add_texture("fireball", load_image("fireball_enemy"))
        self.set_texture("fireball")
        self.zone_rect = Rect(0, 0, 1920, 1080)

    def update(self, world, time):
        super().update(world, time)
        player = world.get_player()
        if player.rect.collide_rect(self.zone_rect):
            dist_x = int(self.rect.x - player.rect.x)
            dist_y = int(self.rect.y - player.rect.y)
            if self.rect.collide_rect(player.rect) and self.exist_time % 100 == 0:
                self.attack(world, player, 1)
            elif dist_x == 0 and abs(dist_y) < 300:
                self.direction = 0 if dist_y > 0 else 2
                self.start_shifting(world)
            elif dist_y == 0 and abs(dist_x) < 300:
                self.direction = 1 if dist_x > 0 else 3
                self.start_shifting(world)
            else:
                self.speed[0] = self.max_speed if dist_y > 1 else 0
                self.speed[1] = self.max_speed if dist_x > 1 else 0
                self.speed[2] = self.max_speed if dist_y < -1 else 0
                self.speed[3] = self.max_speed if dist_x < -1 else 0


class WallBush(Bush):
    def __init__(self, world):
        super().__init__(world)
        self.zone_rect = Rect(0, 0, 1920, 1080)

    def update(self, world, time):
        super().update(world, time)
        player = world.get_player()
        if player.rect.collide_rect(self.zone_rect):
            for obj in world:
                if isinstance(obj, FireBall):
                    if obj.rect.collide_rect(self.zone_rect):
                        self.has_collision = True
                        return
        self.has_collision = False
