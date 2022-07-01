import os
from flask import jsonify, abort
from . import create_app
from .tasks import get, app

#app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Flask endpoints
@app.route("/entries", methods=["GET"])
def get_entries():
    task = get.delay(None)
    result = task.wait(timeout=None)
    return jsonify(result), 200

@app.route("/prices/<id>", methods=["GET"])
def get_entry(id):
    task = get.delay(id)
    result = task.wait(timeout=None)
    if result is None:
        abort(404)
    return jsonify(result), 200