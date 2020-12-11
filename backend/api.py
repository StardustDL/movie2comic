import json
import os
from flask import Flask, request, make_response
from flask.helpers import send_file
from flask_cors import CORS
from .session import Session, SessionStage
from .serialization.json import Encoder


app = Flask(__name__)
CORS(app)


def notfound():
    return make_response("Not Found", 404)


def ok_string(text):
    return make_response(text, 200)


def ok_json(obj):
    return json.dumps(obj, cls=Encoder), 200, {"Content-Type": "application/json"}


@app.route('/api/session', methods=['POST'])
def createSession():
    session = Session()
    file = request.files.get("file")
    if file:
        session.initialize()
        if session.input(file):
            return ok_string(session.id)
        else:
            session.clear()
            return notfound()
    return notfound()


@app.route('/api/session/<sid>/stage', methods=['GET'])
def getSessionStage(sid):
    session = Session(sid)
    return ok_string(str(session.stage().value))


@app.route('/api/session/<sid>/input', methods=['GET'])
def getInput(sid):
    session = Session(sid)
    path = session.input_file
    if os.path.exists(path):
        return send_file(path, mimetype="video/mp4")
    return notfound()


@app.route('/api/session/<sid>/keyframes', methods=['PUT'])
def startKeyframeExtractor(sid):
    print(sid)
    session = Session(sid)
    if session.work_keyframes():
        return ok_string(session.id)
    return notfound()


@app.route('/api/session/<sid>/keyframes', methods=['GET'])
def getKeyframes(sid):
    session = Session(sid)
    result = session.keyframes()
    if result:
        return {
            "frames": [{"name": fr.name, "time": fr.time} for fr in result.frames]
        }
    else:
        return notfound()


@app.route('/api/session/<sid>/keyframes/<name>', methods=['GET'])
def getKeyframe(sid, name):
    session = Session(sid)
    path = session.keyframe_path(name)
    if path:
        return send_file(path, mimetype="image/jpeg")
    return notfound()


@app.route('/api/session/<sid>', methods=['DELETE'])
def deleteSession(sid):
    session = Session(sid)
    if session.stage() is not SessionStage.Created:
        session.clear()
        return ok_string(session.id)
    return notfound()
