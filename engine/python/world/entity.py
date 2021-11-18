from engine.python.util.physics import *
from engine.python.world.object import WorldObject


class Entity(WorldObject):
    def __init__(self, world):
        super().__init__(world)
        self.speed = [0, 0, 0, 0]   # Скорость по направлениям
        self.max_speed = 0          # Максимальная скорость

    # Получить скорость по направлению
    def get_speed(self, direction) -> float:
        return self.speed[direction]

    # Получить суммарную скорость по горизонтали (0) или вертикали (1), или обе (None)
    def get_axis_speed(self, vector=None):
        if vector is None:
            return self.get_speed(3) - self.get_speed(1), self.get_speed(2) - self.get_speed(0)
        return self.get_axis_speed()[vector]

    # Двигаться по инерции, аргументы: мир, время
    def move_inertia(self, world, time):
        vx, vy = self.get_axis_speed()
        if vx == 0 and vy == 0:
            return
        move_x, move_y = get_distance(vx, time), get_distance(vy, time)

        if self.can_move_to(world, self.rect.x + move_x, self.rect.y):
            self.move(world, move_x, 0)
        else:
            self.speed[1], self.speed[3] = 0, 0

        if self.can_move_to(world, self.rect.x, self.rect.y + move_y):
            self.move(world, 0, move_y)
        else:
            self.speed[0], self.speed[2] = 0, 0

    # Проверить, движется ли объект вообще (None) или в указанном направлении
    def is_moving(self, direction=None) -> bool:
        if direction is None:
            return self.get_axis_speed(0) != 0 or self.get_axis_speed(1) != 0
        else:
            return self.get_speed(direction) > 0

    # Вызывается каждый кадр для обновления объекта
    def update(self, world, time):
        super().update(world, time)
        self.move_inertia(world, time)  # Движение по инерции
        self.update_speed(time)

    def update_speed(self, time):
        for i in range(len(self.speed)):
            self.speed[i] = int(self.speed[i] - (self.max_speed / 100 * 1000) * (time / 1000))
            if self.speed[i] < 1:
                self.speed[i] = 0


# Направления:
# 0 - вверх
# 1 - влево
# 2 - вниз
# 3 - вправо
