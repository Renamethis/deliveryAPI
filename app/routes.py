import os
import io
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import jsonify, abort, Response
from .tasks import get, chart, app
from flask_cors import cross_origin

# Flask endpoints to read data from database 
@app.route("/entries", methods=["GET"])
@cross_origin(origin='*')
def get_entries():
    task = get.delay(None)
    result = task.wait(timeout=None)
    response = jsonify(result)
    return response, 200

@app.route("/entries/<id>", methods=["GET"])
def get_entry(id):
    task = get.delay(id)
    result = task.wait(timeout=None)
    if result is None:
        abort(404)
    response = jsonify(result)
    return response, 200

# Build chart flask endpoint
@app.route('/entries/chart', methods=["GET"])
def build_chart():
    task = chart.delay()
    dates, prices = task.wait(timeout=None)
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    fmt = mdates.DateFormatter('%d.%m')
    axis.xaxis.set_major_formatter(fmt)
    for label in axis.get_xticklabels():
        label.set_rotation(45)
    axis.plot(pd.to_datetime(dates, format="%d/%m/%Y"), prices, 
                             marker='o', markersize=2, color=(0, 1, 1))
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
        