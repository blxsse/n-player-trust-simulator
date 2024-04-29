import random
from enum import Enum, auto

class Role(Enum):
    GOOD_GOVERNOR = auto()
    BAD_GOVERNOR = auto()
    CITIZEN = auto()

class Player:
    def __init__(self, role: Role) -> None:
        self.role = role
        self.fitness = 0

    def play(self, x1, x2, x3, tv, R1, R2) -> None:
        self.fitness = tv * (R1 * (x2 / (x2 + x3)) - 1) if self.role == Role.CITIZEN else tv * R1 * (x1 / (x2 + x3)) if self.role == Role.GOOD_GOVERNOR else tv * R2 * (x1 / (x2 + x3))

    def reproduce(self, choice: bool) -> 'Player':
        if choice:
            return Player(self.role)
        else:
            choices = [role for role in Role]
            choices.remove(self.role)
            return Player(random.choices(choices))