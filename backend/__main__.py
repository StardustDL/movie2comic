if __name__ == "__main__":
    from . import api
    api.app.run(host="0.0.0.0", port=80, debug=True)
