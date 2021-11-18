from engine.python.world.entity import Entity


class EntityLiving(Entity):
    def __init__(self, world):
        super().__init__(world)  # Инициализация как у Entity
        self.hp = 100            # Здоровье
        self.energy = 100        # Энергия
        self.direction = 3       # Направление взгляда

    # Устанавливает направление взгляда
    def set_direction(self, direction):
        self.direction = direction
