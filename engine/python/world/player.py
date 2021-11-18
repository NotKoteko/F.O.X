from engine.python.world.entity_living import EntityLiving


class Player(EntityLiving):

    def __init__(self, world):
        super().__init__(world)

    # Изменяет направление взгляда в зависимости от движения энтити
    def update_direction(self, is_moving_up, is_moving_left, is_moving_down, is_moving_right):
        if is_moving_up and not (is_moving_down or is_moving_left or is_moving_right):
            self.set_direction(0)
        elif is_moving_left and not is_moving_right:
            self.set_direction(1)
        elif is_moving_down and not (is_moving_up or is_moving_left or is_moving_right):
            self.set_direction(2)
        elif is_moving_right and not is_moving_left:
            self.set_direction(3)
