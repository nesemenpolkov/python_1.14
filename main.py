from datetime import datetime
from models.lesson import Lesson, LessonType
from models.unit_event import UnitEvent, UnitEventType
from event_store import EventStore


def find_events(store: EventStore):
    print("Поиск событий")
    print("1. По дате")
    print("2. По содержимому")
    print("3. Назад")
    cmd = input()
    if cmd == "1":
        try:
            begin_date = datetime.strptime(input("Начальная дата и время (гггг-мм-дд чч:мм:сс): "), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Неверный формат даты!\n")
            find_events(store)
            return
        try:
            end_date = datetime.strptime(input("Конечная дата и время (гггг-мм-дд чч:мм:сс): "), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            end_date = None
        for event in store.find_by_date(begin_date, end_date):
            print(f"\n{event}\n")
    elif cmd == "2":
        for event in store.find_by_text(input("Введите запрос: ")):
            print(f"\n{event}\n")
    elif cmd == "3":
        return
    else:
        print("Неверная команда!\n")
        find_events(store)
        return


def show_all_events(store: EventStore):
    print("Вывод событий")
    for event in store.get_all():
        print(f"\n{event}\n")


def delete_event(store: EventStore):
    print("Удаление мероприятия")
    for event in store.get_all():
        print(f"\n{event}\n")
    while True:
        try:
            event_id = int(input("Введите ID мероприятия: "))
        except ValueError:
            print("Некорректный ID")
            continue
        store.remove_event(event_id)
        print("Удалено")
        break


def add_event(store: EventStore):
    print("Добавление события")
    print("1. Учебное занятие")
    print("2. Мероприятие подразделения")
    print("3. Назад")
    cmd = input()
    if cmd == "1":
        title = input("Дисциплина: ")
        while not title:
            print("Название дисциплины не может быть пустым")
            title = input("Дисциплина: ")
        description = input("Содержание: ")
        while not description:
            print("Содержание дисциплины не может быть пустым")
            description = input("Содержание: ")
        print("Вид занятия: ")
        lesson_type = None
        while not lesson_type:
            for (i, _lesson_type) in enumerate(LessonType):
                print(f"{i + 1}. {_lesson_type}")
            try:
                lesson_type = LessonType(int(input()))
            except ValueError:
                print("Введите номер пункта меню!")
                continue
        begin_date = None
        while not begin_date:
            try:
                begin_date = datetime.strptime(input("Дата и время проведения занятия (гггг-мм-дд чч:мм:сс): "),
                                               "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("Неверный формат даты!\n")
                continue
        classroom = input("Аудитория: ")
        event = Lesson(title=title,
                       description=description,
                       lesson_type=lesson_type,
                       begin_date=begin_date,
                       classroom=classroom)
    elif cmd == "2":
        title = input("Наименование: ")
        while not title:
            print("Наименование мероприятия не может быть пустым")
            title = input("Наименование: ")
        description = input("Содержание: ")
        while not description:
            print("Содержание мероприятия не может быть пустым")
            description = input("Содержание: ")
        print("Вид мероприятия: ")
        unit_event_type = None
        while not unit_event_type:
            for (i, _unit_event_type) in enumerate(UnitEventType):
                print(f"{i + 1}. {_unit_event_type}")
            try:
                unit_event_type = UnitEventType(int(input()))
            except ValueError:
                print("Введите номер пункта меню!")
                continue
        begin_date = None
        while not begin_date:
            try:
                begin_date = datetime.strptime(input("Дата и время начала мероприятия (гггг-мм-дд чч:мм:сс): "),
                                               "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("Неверный формат даты!\n")
                continue
        end_date = None
        while not end_date:
            try:
                end_date = datetime.strptime(input("Дата и время окончания мероприятия (гггг-мм-дд чч:мм:сс): "),
                                             "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("Неверный формат даты!\n")
                continue
        event = UnitEvent(title=title,
                          description=description,
                          unit_event_type=unit_event_type,
                          begin_date=begin_date,
                          end_date=end_date)
    elif cmd == "3":
        return
    else:
        print("Неверная команда!\n")
        add_event(store)
        return
    print(f"\n{event}\n")
    print("Сохранить изменения?")
    print("1. Да")
    print("2. Нет")
    while True:
        cmd = input()
        if cmd == "1":
            store.add_event(event)
            print("Изменения сохранены!\n")
            break
        elif cmd == "2":
            print("Изменения отменены!\n")
            break
        else:
            print("Неверная команда!\n")


def main():
    store = EventStore()
    while True:
        print("1. Показать все события")
        print("2. Добавить событие")
        print("3. Поиск")
        print("4. Удалить мероприятие")
        print("5. Выход")
        cmd = input()
        if cmd == "1":
            show_all_events(store)
        elif cmd == "2":
            add_event(store)
        elif cmd == "3":
            find_events(store)
        elif cmd == "4":
            delete_event(store)
        elif cmd == "5":
            break
        else:
            print("Неверная команда!\n")


if __name__ == "__main__":
    main()
