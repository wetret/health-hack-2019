from app import app
from flask import Response
import json


@app.before_first_request
def init_server():
    print("Init server..")


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/init/<value>")
def init(value):
    return "Deine Mutti hat value"


@app.route("/decrease/<steps>/", methods=['GET'])
def decrease(steps):
    return_value = {
      "type": "decrease",
      "value": steps,
      "success": "true"
    }

    return Response(json.dumps(return_value), mimetype="application/json")


@app.route("/increase/<steps>", methods=['GET'])
def increase(steps):
    return_value = {
        "type": "increase",
        "value": steps,
        "success": "true"
    }

    return Response(json.dumps(return_value), mimetype="application/json")
