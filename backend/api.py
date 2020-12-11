from flask import Flask

app = Flask(__name__)


@app.route('/api/demo', methods=['GET'])
def demo():
    return "gunicorn and flask demo."
