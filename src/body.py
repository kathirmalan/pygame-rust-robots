import pdb
import random


class Body(object):

    def __init__(self):
        self.health_point = 0  # Health-Point remains with the body, when enabled it will be used

        self.movement_point = 0  # Added to movement-count of the robot
        self.weapon_slots = 0  # Added to weapons-slots of the robot

    def name(self):
        return self.__class__.__name__

    def use_health_point(self, point):
        assert point <= self.health_point, f"[{self.name}] number of health-point(HP) is less than point " \
                                           f"({self.health_point} < {point})."
        self.health_point -= point


class BattleBody(Body):

    def __init__(self):
        super().__init__()
        self.health_point = 5
        self.movement_point = 1
        self.weapon_slots = 1

    def name(self):
        return self.__class__.__name__


class HardBody(Body):

    def __init__(self):
        super().__init__()
        self.health_point = 5
        self.movement_point = 0
        self.weapon_slots = 0

    def name(self):
        return self.__class__.__name__


class LightBody(Body):

    def __init__(self):
        super().__init__()
        self.health_point = 5
        self.movement_point = 1
        self.weapon_slots = 1

    def name(self):
        return self.__class__.__name__


class SimpleBody(Body):

    def __init__(self):
        super().__init__()
        self.health_point = 2
        self.movement_point = 0
        self.weapon_slots = 0

    def name(self):
        return self.__class__.__name__


def choose_body() -> Body:
    bodies = [SimpleBody(),
              HardBody(),
              LightBody(),
              BattleBody()]

    return random.choice(bodies)
