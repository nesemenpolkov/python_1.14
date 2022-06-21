from datetime import datetime
from models.place import Place


class Event:

    def __init__(self, title, description, begin_date, end_date, place, event_id=None):
        assert isinstance(begin_date, datetime), "Begin date: datetime class is required"
        assert isinstance(end_date, datetime), "End date: datetime class is required"
        assert isinstance(place, Place), "Place: Place class is required"
        self.__id = event_id
        self.__title = title
        self.__description = description
        self.__begin_date = begin_date
        self.__end_date = end_date
        self.__place = place

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def begin_date(self):
        return self.__begin_date

    @property
    def end_date(self):
        return self.__end_date

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        assert isinstance(value, Place), "Place: Place class is required"
        self.__place = value

    def __str__(self):
        return f"Событие {self.__id if self.__id else '(без идентификатора)'}\n" \
               f"Название:\t{self.title}\n" \
               f"Описание:\t{self.description}\n" \
               f"Начало:\t\t{str(self.begin_date)}\n" \
               f"Окончание:\t{str(self.end_date)}"

    def __eq__(self, event) -> bool:
        assert isinstance(event, Event), "Event is required"
        return type(self) == type(event) and self.id == event.id

    def __iter__(self):
        for key in ["class", "id", "title", "description", "begin_date", "end_date", "place_id"]:
            if key in ["id", "begin_date", "end_date"]:
                yield key, str(getattr(self, key))
            elif key == "place_id":
                yield key, self.__place.value
            elif key == "class":
                yield key, str(self.__class__.__name__)
            else:
                yield key, getattr(self, key)
