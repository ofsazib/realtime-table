from flask import Flask, request, jsonify, render_template, redirect
import os
import json
import pusher
from datetime import datetime

from database import db_session
from models import Flight


app = Flask(__name__)

@app.route('/')
def index():
    flights = Flight.query.all()
    return render_template('index.html', flights=flights)


@app.route('/create', methods=["POST", "GET"])
def create():
    if request.method == "POST":
        flight = request.form["flight"]
        destination = request.form["destination"]
        check_in = datetime.strptime(request.form["check_in"], '%d-%m-%Y %H:%M %p')
        depature = datetime.strptime(request.form["depature"], '%d-%m-%Y %H:%M %p')
        status = request.form["status"]
        new_flight = Flight(flight, destination, check_in, depature, status)
        db_session.add(new_flight)
        db_session.commit()

        return redirect("/create", code=302)
    else:
        flights = Flight.query.all()
        return render_template('backend.html', flights=flights)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# run Flask app
if __name__ == "__main__":
    app.run()