from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# association tables
association_table = db.Table(
    "association",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("time_id", db.Integer, db.ForeignKey("times.id"))
)

association_table = db.Table(
    "association",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("event_id", db.Integer, db.ForeignKey("events.id"))
)

# model classes
class User(db.Model):
    """
    User Model. 
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    available_times = db.relationship('Time', secondary='user_times', back_populates='users')
    joined_events = db.relationship('Event', secondary='user_events', back_populates='users')

    def serialize(self):
        """
        Serializes a User object. 
        """
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "available_times": [time.serialize() for time in self.available_times],
            "events_joined": [event.serialize() for event in self.joined_events]
        } # last two might need to be simple serialized in the future
    
class Time(db.Model):
    """
    Time Model. 
    """
    __tablename__ = 'times'
    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.String)
    timeslot = db.Column(db.String(10))
    users = db.relationship('User', secondary='user_times', back_populates='available_times')

    def serialize(self):
        """
        Serializes a Time object. 
        """
        return {
            "id": self.id,
            "weekday": self.weekday,
            "timeslot": self.timeslot
        }
    
    # def simple_serialize(self):
    #     """
    #     Serializes a Time object without users. 
    #     """
    #     return {
    #         "id": self.id,
    #         "weekday": self.weekday,
    #         "timeslot": self.timeslot 
    #     }

class Event(db.Model):
    """
    Event Model. 
    """
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    users = db.relationship('User', secondary='user_events', back_populates='joined_events')

    def serialize(self):
        """
        Serializes an Event object.
        """
        return {
            "id": self.id,
            "description": self.description
        }