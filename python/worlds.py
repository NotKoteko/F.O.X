import random
import pygame

from engine.python.util.rect import Rect
from engine.python.util.video import load_image, get_screen_size, get_centered_pos
from engine.python.world.object import WorldObject
from engine.python.world.world import World
from python.objects import Fox, Tree, Bush


class RandomGeneratedWorld(World):
    def __init__(self):
        super().__init__()
        self.load()
        self.background_color = (0, 170, 0)

    # Генерируем мир
    def load(self, filename=None):
        # Получаем размер экрана
        screen_size = get_screen_size()

        # Создаём лису по центру экрана
        fox = Fox(self)
        fox_pos = get_centered_pos(screen_size, fox.rect.get_size())
        fox.rect.set_pos(fox_pos[0], fox_pos[1])

        # Задаём размеры клетки, отталкиваясь от них считаем размеры мира (так, чтобы влезли на экран)
        cell_size = 48
        cells_x, cells_y = screen_size[0] // cell_size - 1, screen_size[1] // cell_size - 1

        # Генерируем заборы по краям экрана (проходимся двумя циклами по всем клеткам)
        for y in range(0, cells_y, 2):
            for x in range(0, cells_x, 2):
                # Ставим заборы слева (x == 0), справа (x == макс.x), сверху (y == 0) снизу (y == макс.y)
                if x == 0 or x == cells_x - 1 or y == 0 or y == cells_y - 1:
                    # Создаём объект, добавляем ему нужные текстуры и устанавливаем позицию.
                    obj = Bush(self)
                    obj.add_texture("bush", load_image("bush"))
                    obj.set_texture("bush")
                    obj.rect.set_pos(x, y, cell_size)
                    obj.rect.set_size(2, 2, cell_size)
                    obj.has_collision = True  # Включаем коллизию

        # Список всех возможных объектов для генерации
        objects = ["stump" for i in range(30)] + ["tree" for i in range(20)] + ["bush" for i in range(20)]
        # Создаём 15 рандомных объектов
        for i in range(15):
            # Выбираем тип объекта из списка, добавляем текстуры
            obj_type = random.choice(objects)
            obj = WorldObject(self) if obj_type == "stump" else Tree(self) if obj_type == "tree" else Bush(self)
            obj.add_texture(obj_type, load_image(obj_type))
            obj.set_texture(obj_type)

            # Выбираем рандомные x и y, пока не выберем их так, чтобы объект не касался других объектов
            x, y = 1, 1
            rect = Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            while x % 2 != 0 or y % 2 != 0 or rect.collide_any(self):
                x, y = random.randint(3, cells_x - 2), random.randint(3, cells_y - 2)
                rect.set_pos(x * cell_size, y * cell_size)
            obj.rect = rect

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
