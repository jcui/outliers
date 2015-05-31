from flask import (Flask, abort, request)
from service import service

app = Flask(__name__)

def run(debug):
    app.debug = debug
    app.run()

def abort_bad_request(message):
    abort(400, message)

def abort_not_found(message):
    abort(404, message)

def abort_internal_error(message):
    abort(500, message)

def get_threshold(threshold):
    try:
        return service.get_threshold(threshold)
    except service.ThresholdOutOfRangeException as e:
        abort_bad_request(e.message)
    except service.ThresholdNotAnIntegerException as e:
        abort_bad_request(e.message)

@app.route('/clusters/caches/outliers')
def get_all_outliers():
    threshold = get_threshold(request.args.get('threshold'))
    try:
        return service.get_all_outliers(threshold)
    except service.QueryCachesFailedException as e:
        abort_internal_error(e.message)

@app.route('/clusters/<cluster>/caches/outliers')
def get_cluster_outliers(cluster):
    threshold = get_threshold(request.args.get('threshold'))
    try:
        return service.get_cluster_outliers(cluster, threshold)
    except service.ClusterNotFoundException as e:
        abort_not_found(e.message)
    except service.QueryCachesFailedException as e:
        abort_internal_error(e.message)
