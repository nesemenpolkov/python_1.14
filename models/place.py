from enum import Enum


class Place(Enum):

    BARRACKS = 1
    SPORTS_GROUND = 2
    CAMPUS = 3

    def __str__(self) -> str:
        if self.value == 1:
            return "Казарма"
        elif self.value == 2:
            return "Спортгородок"
        elif self.value == 3:
            return "Учебный корпус"
