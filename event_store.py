from models.event import Event
from models.lesson import Lesson, LessonType
from models.unit_event import UnitEvent, UnitEventType
from models.place import Place
from datetime import datetime
import sqlite3


class EventStore:

    def __init__(self):
        self.__connection = self.__init_database()

    def __init_database(self):
        connection_string = 'database.db'
        connection = sqlite3.connect(connection_string, check_same_thread=False)
        connection.execute("PRAGMA foreign_keys = ON")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        if not bool(cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='places';").fetchall()):
            cursor.execute("CREATE TABLE places (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)")
            data = {
                (1, "Казарма"),
                (2, "Спортгородок"),
                (3, "Учебный корпус")
            }
            statement = "INSERT INTO places (id, title) VALUES (?, ?)"
            cursor.executemany(statement, data)
            connection.commit()
        if not bool(cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='lesson_types';").fetchall()):
            cursor.execute("CREATE TABLE lesson_types (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)")
            data = {
                (1, "Лекция"),
                (2, "Практическое занятие"),
                (3, "Семинар"),
                (4, "Самостоятельная работа"),
                (5, "Лабораторная работа")
            }
            statement = "INSERT INTO lesson_types (id, title) VALUES (?, ?)"
            cursor.executemany(statement, data)
            connection.commit()
        if not bool(cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='unit_event_types';").fetchall()):
            cursor.execute("CREATE TABLE unit_event_types (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)")
            data = {
                (1, "Чистка оружия"),
                (2, "Спортивно-массовая работа"),
                (3, "Информирование"),
                (4, "Воспитательная работа")
            }
            statement = "INSERT INTO unit_event_types (id, title) VALUES (?, ?)"
            cursor.executemany(statement, data)
            connection.commit()
        if not bool(cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='events';").fetchall()):
            cursor.execute("CREATE TABLE events (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, "
                           "description TEXT, begin_date INTEGER NOT NULL, end_date INTEGER NOT NULL, "
                           "place_id INTEGER NOT NULL, FOREIGN KEY (place_id) REFERENCES places(id))")
        if not bool(cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='lessons';").fetchall()):
            cursor.execute("CREATE TABLE lessons (id INTEGER PRIMARY KEY AUTOINCREMENT, event_id INTEGER NOT NULL, "
                           "lesson_type_id INTEGER NOT NULL, classroom TEXT NOT NULL, "
                           "CONSTRAINT fk_events FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,"
                           "FOREIGN KEY (lesson_type_id) REFERENCES lesson_types(id))")
        if not bool(cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='unit_events';").fetchall()):
            cursor.execute("CREATE TABLE unit_events (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                           "event_id INTEGER NOT NULL, unit_event_type_id INTEGER NOT NULL,"
                           "CONSTRAINT fk_events FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,"
                           "FOREIGN KEY (unit_event_type_id) REFERENCES unit_event_types(id))")
        return connection

    def add_event(self, event: Event):
        assert isinstance(event, Event), "Event is required"
        cursor = self.__connection.cursor()
        cursor.execute("INSERT INTO events (title, description, begin_date, end_date, place_id) "
                       "VALUES (?, ?, ?, ?, ?)",
                       (event.title, event.description, int(event.begin_date.timestamp()),
                        int(event.end_date.timestamp()), event.place.value))
        self.__connection.commit()
        if type(event) == Lesson:
            cursor.execute("INSERT INTO lessons (event_id, lesson_type_id, classroom) VALUES (?, ?, ?)",
                           (cursor.lastrowid, event.lesson_type.value, event.classroom))
        elif type(event) == UnitEvent:
            cursor.execute("INSERT INTO unit_events (event_id, unit_event_type_id) VALUES (?, ?)",
                           (cursor.lastrowid, event.unit_event_type.value))
        self.__connection.commit()

    def remove_event(self, event_id: int):
        assert isinstance(event_id, int), "Event is required"
        cursor = self.__connection.cursor()
        cursor.execute("DELETE FROM events WHERE id=?", (event_id,))
        self.__connection.commit()

    def find_by_date(self, begin_date: datetime, end_date: datetime = None):
        assert type(begin_date) == datetime, "Begin date: datetime required!"
        cursor = self.__connection.cursor()
        if end_date:
            rows = cursor.execute("SELECT events.id, title, description, begin_date, end_date, place_id, "
                                  "lesson_type_id, classroom, unit_event_type_id from events "
                                  "LEFT JOIN lessons ON events.id = lessons.event_id "
                                  "LEFT JOIN unit_events ON events.id = unit_events.event_id "
                                  "WHERE begin_date>=? AND end_date <=?",
                                  (begin_date.timestamp(), end_date.timestamp()))
        else:
            rows = cursor.execute("SELECT events.id, title, description, begin_date, end_date, place_id, "
                                  "lesson_type_id, classroom, unit_event_type_id from events "
                                  "LEFT JOIN lessons ON events.id = lessons.event_id "
                                  "LEFT JOIN unit_events ON events.id = unit_events.event_id "
                                  "WHERE begin_date>=?", (begin_date.timestamp(),))
        return self.__convert_rows_to_objects(rows)

    def find_by_text(self, text: str):
        assert type(text) == str, "text: str required!"
        cursor = self.__connection.cursor()
        rows = cursor.execute("SELECT events.id, title, description, begin_date, end_date, place_id, "
                              "lesson_type_id, classroom, unit_event_type_id from events "
                              "LEFT JOIN lessons ON events.id = lessons.event_id "
                              "LEFT JOIN unit_events ON events.id = unit_events.event_id "
                              f"WHERE title LIKE '%{text}%'")
        return self.__convert_rows_to_objects(rows)


    def find_by_date_or_text(self, text: str = None, begin_date: datetime = None, end_date: datetime = None):
        pass


    def get_all(self):
        cursor = self.__connection.cursor()
        rows = cursor.execute("SELECT events.id, title, description, begin_date, end_date, place_id, "
                              "lesson_type_id, classroom, unit_event_type_id from events "
                              "LEFT JOIN lessons ON events.id = lessons.event_id "
                              "LEFT JOIN unit_events ON events.id = unit_events.event_id")
        return self.__convert_rows_to_objects(rows)

    def __convert_rows_to_objects(self, rows):
        for row in rows:
            if row["lesson_type_id"]:
                yield Lesson(lesson_id=row["id"], title=row["title"], description=row["description"],
                             lesson_type=LessonType(row["lesson_type_id"]),
                             classroom=row["classroom"],
                             begin_date=datetime.fromtimestamp(row["begin_date"]))
            elif row["unit_event_type_id"]:
                yield UnitEvent(unit_event_id=row["id"], title=row["title"], description=row["description"],
                                unit_event_type=UnitEventType(row["unit_event_type_id"]),
                                begin_date=datetime.fromtimestamp(row["begin_date"]),
                                end_date=datetime.fromtimestamp(row["end_date"]))
            else:
                yield Event(event_id=row["id"], title=row["title"], description=row["description"],
                            begin_date=datetime.fromtimestamp(row["begin_date"]),
                            end_date=datetime.fromtimestamp(row["end_date"]), place=Place(row["place_id"]))