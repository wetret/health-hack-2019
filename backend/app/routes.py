from app import app
from flask import Response
import json
import serial


arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600)


states = [1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 15]
current_state_index = 0


@app.before_first_request
def init_server():
    print("Init server..")
    try:
       arduino.open()
       print("Arduino port opened")
    except Exception:
        print("Arduino port already open")


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/init/")
def init():
    arduino.write(("-" + str(10)).encode())

    global current_state_index
    current_state_index = 0

    return_value = {
        "type": "init",
        "value": states[current_state_index],
        "success": "true"
    }

    return Response(json.dumps(return_value), mimetype="application/json")


@app.route("/increase/<steps>/", methods=['GET'])
def increase(steps):
    if check(steps):
        arduino.write(str(steps).encode())

        global current_state_index
        current_state_index = current_state_index + int(steps)

        if current_state_index > len(states):
            current_state_index = len(states)

        return_value = {
            "type": "increase",
            "value": states[current_state_index],
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
        arduino.write(("-" + str(steps)).encode())

        global current_state_index
        current_state_index = current_state_index - int(steps)

        if current_state_index < 0:
            current_state_index = 0

        return_value = {
          "type": "decrease",
          "value": states[current_state_index],
          "success": "true"
        }

        return Response(json.dumps(return_value), mimetype="application/json")
    else:
        return_value = {
            "error": "steps to high"
        }

        return Response(json.dumps(return_value), mimetype="application/json", status=400)


def check(steps):
    if int(steps) > 10:
        return False

    return True
