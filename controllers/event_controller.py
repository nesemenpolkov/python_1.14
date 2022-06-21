from flask import Blueprint, request, render_template, url_for, redirect
from event_store import EventStore
from datetime import datetime
from models.lesson import Lesson, LessonType
from models.unit_event import UnitEvent, UnitEventType


events = Blueprint("events", __name__)
route = "/events"


store = EventStore()


@events.route(route, methods=["GET"])
def get_all_events():
    inform = request.args.get("event_added", False)
    if inform:
        return render_template("events.html", events=[event for event in store.get_all()], info="Событие добавлено!")
    return render_template("events.html", events=[event for event in store.get_all()])


@events.route(f"{route}/search", methods=["GET"])
def find_events():
    text = request.args.get("query", "")
    try:
        begin = datetime.fromisoformat(request.args.get("begin_date", None))
    except TypeError:
        begin = None
    except ValueError:
        begin = None
    try:
        end = datetime.fromisoformat(request.args.get("end_date", None))
    except TypeError:
        end = None
    except ValueError:
        end = None
    events = store.find_by_date_or_text(text=text, begin_date=begin, end_date=end)
    if events:
        return render_template("events.html", events=[event for event in events])
    else:
        return render_template("events.html", events=[])


@events.route(f"{route}/add", methods=["GET", "POST"])
def add_event():
    if request.method == "GET":
        return render_template("new_event.html")
    else:
        if "event_type" not in request.form:
            return render_template("new_event.html", error="Не указан тип мероприятия!")
        event_type = request.form["event_type"]
        lesType = {
            "lecture": 1,
            "practical": 2,
            "seminar": 3,
            "self_work": 4,
            "laboratory_work": 5
        }
        unitType = {
            "weapon": 1,
            "sport": 2,
            "info": 3,
            "upbring": 4
        }
        if event_type == "lesson":

            title = request.form["title"]
            if not title:
                return render_template("new_event.html", error="Нехватает имени!")
            description = request.form["description"]
            if not description:
                return render_template("new_event.html", error="Нехватает описания!")
            lesson_type = request.form["lesson_type"]
            if not lesson_type:
                return render_template("new_event.html", error="Нехватает типа урока!")
            try:
                begin_date = datetime.fromisoformat(request.form["begin_date"])
            except:
                return render_template("new_event.html", error="Нехватает даты!")
            classroom = request.form["classroom"]

            event = Lesson(title=title,
                           description=description,
                           lesson_type=LessonType(lesType[lesson_type]),
                           begin_date=begin_date,
                           classroom=classroom)
        elif event_type == "unit_event":
            print(request.form)
            title = request.form["title"]
            print(title)
            if not title:
                return render_template("new_event.html", error="Нехватает имени!")
            description = request.form["description"]
            print(description)
            if not description:
                return render_template("new_event.html", error="Нехватает описания!")
            unit_event_type = request.form["unit_type"]
            print(unit_event_type)
            if not unit_event_type:
                return render_template("new_event.html", error="Нехватает типа урока!")
            try:
                begin_date = datetime.fromisoformat(request.form["begin_date"])
                end_date = datetime.fromisoformat(request.form["end_date"])
            except Exception as e:
                print(str(e))
                return render_template("new_event.html", error="Нехватает даты!")
            event = UnitEvent(title=title,
                              description=description,
                              unit_event_type=UnitEventType(unitType[unit_event_type]),
                              begin_date=begin_date,
                              end_date=end_date)
        else:
            return render_template("new_event.html", error="Указан неверный тип мероприятия!")
        store.add_event(event)
        return redirect(url_for(".get_all_events", event_added=True))


@events.route(f"{route}/delete", methods=["POST"])
def delete_event():
    if "id" not in request.form:
        return render_template("events.html", error="Ай Ди не указан!")
    try:
        event_id = request.form["id"]
    except ValueError:
        return render_template("events.html", error="Не верный формат Id!")
    store.remove_event(int(event_id))
    return render_template("events.html", events=[event for event in store.get_all()], info="Событие удалено!")



