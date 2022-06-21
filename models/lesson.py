from datetime import timedelta
from enum import Enum
from models.event import Event
from models.place import Place


class Lesson(Event):

    def __init__(self, title, description, lesson_type, begin_date, classroom=None, lesson_id=None):
        super().__init__(title, description, begin_date, begin_date + timedelta(minutes=90), Place.CAMPUS, lesson_id)
        assert isinstance(lesson_type, LessonType), "Lesson type: LessonType class is required!"
        self.__lesson_type = lesson_type
        self.__classroom = classroom
        self.__id = lesson_id
        
    @property
    def lesson_type(self):
        return self.__lesson_type
    
    @property
    def classroom(self):
        return self.__classroom or "Не назначена"
        
    def __str__(self):
        return f"Занятие {self.__id if self.__id else '(без идентификатора)'}\n" \
                f"Дисциплина:\t{self.title}\n" \
                f"Содержание:\t{self.description}\n" \
                f"Вид занятия:\t{self.__lesson_type}\n" \
                f"Начало:\t\t{str(self.begin_date)}\n" \
                f"Окончание:\t{str(self.end_date)}\n" \
                f"Место:\t\t{self.place}\n" \
                f"Аудитория:\t{self.classroom}"

    def __iter__(self):
        for key in ["class", "id", "title", "description", "lesson_type_id", "begin_date", "end_date", "place_id", "classroom"]:
            if key in ["id", "begin_date", "end_date"]:
                yield key, str(getattr(self, key))
            elif key in ["place_id", "lesson_type_id"]:
                yield key, getattr(self, key[:-3]).value
            elif key == "class": 
                yield key, str(self.__class__.__name__)
            else:
                yield key, getattr(self, key)


class LessonType(Enum):

    LECTURE = 1
    PRACTICAL = 2
    SEMINAR = 3
    SELF_WORK = 4
    LABORATORY_WORK = 5

    def __str__(self) -> str:
        if self.value == 1:
            return "Лекция"
        elif self.value == 2:
            return "Практическое занятие"
        elif self.value == 3: 
            return "Семинар"
        elif self.value == 4:
            return "Самостоятельная работа"
        elif self.value == 5:
            return "Лабораторная работа"
