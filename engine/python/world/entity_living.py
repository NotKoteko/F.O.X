from engine.python.world.entity import Entity


class EntityLiving(Entity):
    def __init__(self, world):
        super().__init__(world)  # Инициализация как у Entity
        self.hp = 100            # Здоровье
        self.energy = 100        # Энергия
        self.direction = 3       # Направление взгляда

        self.is_shifting = False
        self.shifting_time_start = 0
        self.shifting_time_end = 0
        self.last_attack_time = 0

    # Устанавливает направление взгляда
    def set_direction(self, direction):
        self.direction = direction

    def attack(self, world, target, damage):
        target.get_damage(world, damage)
        self.last_attack_time = world.world_time

    def get_damage(self, world, damage):
        self.hp -= damage

    def update(self, world, time):
        super().update(world, time)
        if self.is_shifting:
            if self.exist_time - self.shifting_time_start > 150:
                self.stop_shifting(world)

    def start_shifting(self, world):
        self.speed[self.direction] = self.max_speed * 5
        self.is_shifting = True
        self.shifting_time_start = self.exist_time

    def stop_shifting(self, world):
        self.speed[self.direction] = self.max_speed
        self.is_shifting = False
        self.shifting_time_end = self.exist_time

    def update_speed(self, world, time):
        if not self.is_shifting:
            super().update_speed(world, time)
