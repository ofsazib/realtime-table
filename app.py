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
    return render_template('index.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# run Flask app
if __name__ == "__main__":
    app.run()