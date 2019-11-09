from app import app
from flask import Response
import json
import serial


arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600)


@app.before_first_request
def init_server():
    print("Init server..")
    try:
       arduino.open()
    except Exception:
        print("Arduino port already open")


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/init/<value>")
def init(value):
    return_value = {
        "type": "init",
        "value": value,
        "success": "true"
    }

    return Response(json.dumps(return_value), mimetype="application/json")


@app.route("/increase/<steps>/", methods=['GET'])
def increase(steps):
    if check(steps):
        arduino.write(steps.encode())

        return_value = {
            "type": "increase",
            "value": steps,
            "success": "true"
        }

        return Response(json.dumps(return_value), mimetype="application/json")
    else:
        return_value = {
            "error": "steps to high"
        }

        return Response(json.dumps(return_value), mimetype="application/json", status=400)


@app.route("/decrease/<steps>/", methods=['GET'])
def decrease(steps):
    if check(steps):
        arduino.write(steps.encode())

        return_value = {
          "type": "decrease",
          "value": steps,
          "success": "true"
        }

        return Response(json.dumps(return_value), mimetype="application/json")
    else:
        return_value = {
            "error": "steps to high"
        }

        return Response(json.dumps(return_value), mimetype="application/json", status=400)


def check(steps):
    if int(steps) > 16:
        return False

    return True
