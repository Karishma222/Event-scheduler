from flask import Blueprint, request, render_template, redirect
from models import db, Event, Resource, Allocation, User
from datetime import datetime

routes = Blueprint("routes", __name__)


# LOGIN
@routes.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            return redirect("/")

        return "Invalid Login"

    return render_template("login.html")


# DASHBOARD
@routes.route("/")
def home():

    events = Event.query.all()
    resources = Resource.query.all()

    return render_template("dashboard.html", events=events, resources=resources)


# CREATE EVENT
@routes.route("/events", methods=["POST"])
def create_event():

    title = request.form["title"]
    description = request.form["description"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]

    event = Event(
        title=title,
        description=description,
        start_time=datetime.strptime(start_time, "%Y-%m-%dT%H:%M"),
        end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
    )

    db.session.add(event)
    db.session.commit()

    return redirect("/")


# DELETE EVENT
@routes.route("/delete/<int:id>")
def delete_event(id):

    event = Event.query.get(id)

    db.session.delete(event)
    db.session.commit()

    return redirect("/")


# RESOURCE PAGE
@routes.route("/resources", methods=["GET", "POST"])
def resources():

    if request.method == "POST":

        name = request.form["name"]
        type = request.form["type"]

        resource = Resource(name=name, type=type)

        db.session.add(resource)
        db.session.commit()

        return redirect("/resources")

    resources = Resource.query.all()

    return render_template("resources.html", resources=resources)


# ALLOCATE RESOURCE
@routes.route("/allocate", methods=["POST"])
def allocate():

    event_id = int(request.form["event_id"])
    resource_id = int(request.form["resource_id"])

    event = Event.query.get(event_id)
    resource = Resource.query.get(resource_id)

    if not event or not resource:
        return "Event or Resource not found"

    allocations = Allocation.query.filter_by(resource_id=resource_id).all()

    for a in allocations:

        e = a.event

        if event.start_time < e.end_time and event.end_time > e.start_time:
            return "Resource already booked for this time"

    allocation = Allocation(event_id=event_id, resource_id=resource_id)

    db.session.add(allocation)
    db.session.commit()

    return redirect("/")


# REPORT PAGE
@routes.route("/report")
def report():

    allocations = Allocation.query.all()

    data = []

    for a in allocations:

        data.append({
            "event": a.event.title,
            "resource": a.resource.name,
            "start": a.event.start_time,
            "end": a.event.end_time
        })

    return render_template("report.html", data=data)


# CALENDAR VIEW
@routes.route("/calendar")
def calendar():

    events = Event.query.all()

    return render_template("calendar.html", events=events)