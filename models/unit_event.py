from enum import Enum
from models.event import Event
from models.place import Place


class UnitEvent(Event):
    
    def __init__(self, title, description, unit_event_type, begin_date, end_date, unit_event_id=None):
        assert isinstance(unit_event_type, UnitEventType), "Unit event type: UnitEventType class is required!"
        if unit_event_type == UnitEventType.SPORTS:
            place = Place.SPORTS_GROUND
        else:
            place = Place.BARRACKS
        super().__init__(title, description, begin_date, end_date, place, unit_event_id)
        self.__unit_event_type = unit_event_type
        self.__id = unit_event_id

    @property
    def unit_event_type(self):
        return self.__unit_event_type

    def __str__(self):
        return f"Мероприятие {self.__id if self.__id else '(без идентификатора)'}\n" \
                f"Наименование:\t{self.title}\n" \
                f"Содержание:\t{self.description}\n" \
                f"Вид:\t\t{self.__unit_event_type}\n" \
                f"Начало:\t\t{str(self.begin_date)}\n" \
                f"Окончание:\t{str(self.end_date)}\n" \
                f"Место:\t\t{self.place}"

    def __iter__(self):
        for key in ["class", "id", "title", "description", "unit_event_type_id", "begin_date", "end_date", "place_id"]:
            if key in ["id", "begin_date", "end_date"]:
                yield key, str(getattr(self, key))
            elif key in ["place_id", "unit_event_type_id"]:
                yield key, getattr(self, key[:-3]).value
            elif key == "class": 
                yield key, str(self.__class__.__name__)
            else:
                yield key, getattr(self, key)


class UnitEventType(Enum):

    WEAPON_CLEANING = 1
    SPORTS = 2
    INFORMING = 3
    UPBRINGING = 4

    def __str__(self) -> str:
        if self.value == 1:
            return "Чистка оружия"
        elif self.value == 2:
            return "Спортивно-массовая работа"
        elif self.value == 3: 
            return "Информирование"
        elif self.value == 4:
            return "Воспитательная работа"
