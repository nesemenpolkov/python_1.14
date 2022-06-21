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
    return render_template("events.html", events=[event for event in store.get_all()])


@events.route(f"{route}/search", methods=["GET"])
def find_events():
    pass


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
            title = request.form["title"]
            description = request.form["description"]
            unit_event_type = request.form["unit_event_type"]
            begin_date = datetime.strptime(request.form["begin_date"], "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d %H:%M:%S")
            classroom = request.form["classroom"]
            event = UnitEvent(title=title,
                              description=description,
                              unit_event_type=unit_event_type,
                              begin_date=begin_date,
                              end_date=end_date)
        else:
            return render_template("new_event.html", error="Указан неверный тип мероприятия!")
        store.add_event(event)
        return redirect(url_for(".get_all_events", event_added=True))


@events.route(f"{route}/delete", methods=["POST"])
def delete_event():
    pass


