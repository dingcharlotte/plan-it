from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# association tables
association_table = db.Table(
    "association",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("event_id", db.Integer, db.ForeignKey("events.id"))
)
# association_table = db.Table(
#     "association",
#     db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
#     db.Column("time_id", db.Integer, db.ForeignKey("times.id"))
# )

# model classes
class User(db.Model):
    """
    User Model. 
    Has a one-to-many relationship with the Time model. 
    Has a many-to-many relationship with the Event model. 
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    available_times = db.relationship("Time", cascade="delete")
    # available_times = db.relationship('Time', secondary='user_times', back_populates='users')
    joined_events = db.relationship("Event", secondary=association_table, back_populates='users')
    # joined_events = db.relationship("Event", secondary='user_events', back_populates='users')

    def __init__(self, **kwargs): 
        """
        Initialize User object. 
        """
        self.name = kwargs.get("name", "")
        self.username = kwargs.get("username", "")
    
    def serialize(self):
        """
        Serialize User object. 
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    weekday = db.Column(db.Integer, nullable=False)
    timeslot = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # users = db.relationship('User', secondary='user_times', back_populates='available_times')

    def __init__(self, **kwargs):
        """
        Initialize Time object. 
        """
        self.weekday = kwargs.get("weekday", 0) # default to Sunday
        self.timeslot = kwargs.get("timeslot", "")
        self.user_id = kwargs.get("user_id")
    
    def serialize(self):
        """
        Serialize Time object. 
        """
        return {
            "id": self.id,
            "weekday": self.weekday,
            "timeslot": self.timeslot, 
            "user_id": self.user_id
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    users = db.relationship('User', secondary=association_table, back_populates='joined_events')

    def __init__(self, **kwargs):
        """
        Initialize Event object. 
        """
        self.description = kwargs.get("description", "")
        
    def serialize(self):
        """
        Serialize Event object.
        """
        return {
            "id": self.id,
            "description": self.description
        }