from flask import Flask, request, jsonify, render_template, redirect
import os
import json
import pusher
from datetime import datetime

from database import db_session
from models import Flight


app = Flask(__name__)

pusher_client = pusher.Pusher(
    app_id=os.getenv('PUSHER_APP_ID'),
    key=os.getenv('PUSHER_KEY'),
    secret=os.getenv('PUSHER_SECRET'),
    cluster=os.getenv('PUSHER_CLUSTER'),
    ssl=True
)


@app.route('/')
def index():
    flights = Flight.query.all()
    return render_template('index.html', flights=flights)


@app.route('/create', methods=["POST", "GET"])
def create():
    if request.method == "POST":
        flight = request.form["flight"]
        destination = request.form["destination"]
        check_in = datetime.strptime(
            request.form["check_in"], '%d-%m-%Y %H:%M %p')
        depature = datetime.strptime(
            request.form["depature"], '%d-%m-%Y %H:%M %p')
        status = request.form["status"]
        new_flight = Flight(flight, destination, check_in, depature, status)
        db_session.add(new_flight)
        db_session.commit()

        data = {
            "id": new_flight.id,
            "flight": flight,
            "destination": destination,
            "check_in": request.form["check_in"],
            "depature": request.form["depature"],
            "status": status
        }

        pusher_client.trigger('table', 'new-record', {'data': data})

        return redirect("/create", code=302)
    else:
        flights = Flight.query.all()
        return render_template('backend.html', flights=flights)


@app.route('/edit/<int:id>', methods=["POST", "GET"])
def update_flight(id):
    if request.method == "POST":
        flight = request.form["flight"]
        destination = request.form["destination"]
        check_in = datetime.strptime(
            request.form["check_in"], '%d-%m-%Y %H:%M %p')
        depature = datetime.strptime(
            request.form["depature"], '%d-%m-%Y %H:%M %p')
        status = request.form["status"]

        edit_flight = Flight.query.get(id)
        edit_flight.flight = flight
        edit_flight.destination = destination
        edit_flight.check_in = check_in
        edit_flight.depature = depature
        edit_flight.status = status
        db_session.commit()

        data = {
            "id": id,
            "flight": flight,
            "destination": destination,
            "check_in": request.form["check_in"],
            "depature": request.form["depature"],
            "status": status
        }

        pusher_client.trigger('table', 'update-record', {'data': data})

        return redirect("/create", code=302)
    else:
        new_flight = Flight.query.get(id)
        new_flight.check_in = new_flight.check_in.strftime("%d-%m-%Y %H:%M %p")
        new_flight.depature = new_flight.depature.strftime("%d-%m-%Y %H:%M %p")
        return render_template('update-flight.html', data=new_flight)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# run Flask app
if __name__ == "__main__":
    app.run()
