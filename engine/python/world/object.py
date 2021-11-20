from engine.python.util.rect import Rect
from engine.python.util.video import load_image


# Объект, размещаемый в мире
class WorldObject:
    def __init__(self, world=None):
        if world:
            world.add(self)
        self.obj_id = None
        self.name = None
        self.rect = Rect(0, 0, 1, 1)

        self.textures = {"default": load_image("default")}
        self.texture = self.textures.get("default")

        self.exist_time = 0
        self.has_collision = True
        self.is_visible = True

    # Передвинуть объект
    def move(self, world, x, y):
        self.rect = self.rect.move(x, y)

    # Проверить, может ли объект передвинуться в указанное место
    def can_move_to(self, world, x, y):
        if not self.has_collision:
            return True
        rect = Rect(x, y, self.rect.width, self.rect.height)
        collide_after = [other for other in world if other != self and other.has_collision
                         and rect.collide_rect(other.rect) and not self.rect.collide_rect(other.rect)]
        return collide_after == []

    # Добавить новую текстуру в список
    def add_texture(self, texture_name, texture):
        self.textures[texture_name] = texture

    # Установить текстуру
    def set_texture(self, texture_key):
        if texture_key in self.textures.keys():
            self.texture = self.textures[texture_key]
        else:
            self.texture = self.textures["default"]
            print(f'Не удалось найти текстуру "{texture_key}" для объекта {self}')

    # Возвращает отображаемую текстуру
    def get_texture(self):
        return self.texture

    # Возвращает прямоугольник, в котором рисуется текстура
    def get_texture_rect(self):
        return self.rect

    # Вызывается каждый кадр для обновления объекта
    def update(self, world, time):
        self.exist_time += time  # Увеличиваем время существования

    def kill(self, world):
        del world.obj_dict[self]

