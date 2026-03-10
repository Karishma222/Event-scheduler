from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Event(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)


class Resource(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(50))   # room / instructor / equipment


class Allocation(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    resource_id = db.Column(db.Integer, db.ForeignKey("resource.id"))

    event = db.relationship("Event")
    resource = db.relationship("Resource")

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(200))

    role = db.Column(db.String(50))   # Admin / Organizer / Viewer