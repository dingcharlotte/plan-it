import json
from db import db, User, Time, Event
from flask import Flask, request

db_filename = "plan-it.db"
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

# routes
@app.route("/")

@app.route("/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a new user. 
    """
    body = json.loads(request.data)
    new_user = User(
        name = body.get("name"), 
        username = body.get("username"))
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by id. 
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())

@app.route("/users/<int:user_id>/times/", methods=["POST"])
def create_time(user_id):
    """
    Endpoint for creating a new (available) timeslot for a user by id. 
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    body = json.loads(request.data)
    new_time = Time(
        weekday = body.get("weekday"),
        timeslot = body.get("timeslot"),
        user_id = user_id)
    db.session.add(new_time)
    db.session.commit()
    return success_response(new_time.serialize(), 201)

@app.route("/users/<int:user_id>/times/<int:time_id>/", methods=["DELETE"])
def delete_time(user_id, time_id): 
    """
    Endpoint for deleting a user's (available) timeslot by id. 
    """
    time = Time.query.filter_by(user_id=user_id, id=time_id).first()
    if time is None:
        return failure_response("Timeslot not found")
    db.session.delete(time)
    db.session.commit()
    return success_response(time.serialize())

@app.route("/events/<int:user_id>/", methods=["POST"])
def create_event(user_id): 
    """
    Endpoint for creating a new event. 
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    body = json.loads(request.data)
    description = body.get("description")
    users = body.get("users")
    event = Event.query.filter_by(description=description).first()
    if event is None: 
        event = Event(
            description = description)
    user.joined_events.append(event)
    for uid in users:
        u = User.query.filter_by(id=uid).first()
        u.joined_events.append(event)
    db.session.commit()
    return success_response(event.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)