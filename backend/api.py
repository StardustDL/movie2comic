from flask import Flask, request, make_response
from flask_cors import CORS
from .session import Session

app = Flask(__name__)
CORS(app)


def notfound():
    return make_response("Not Found", 404)


def ok_string(text):
    return make_response(text, 200)


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


@app.route('/api/session/<sid>', methods=['DELETE'])
def deleteSession(sid):
    session = Session(sid)
    if session.exists():
        session.clear()
        return ok_string(session.id)
    return notfound()
