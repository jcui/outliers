from flask import (Flask, abort, jsonify, request)
from service import service

app = Flask(__name__)

OUTLIER_DESCRIPTION = 'outlier throughput exceeds average by threshold %'

def run(debug):
    app.debug = debug
    app.run()

def abort_bad_request(message):
    abort(400, message)

def abort_not_found(message):
    abort(404, message)

def abort_internal_error(message):
    abort(500, message)

def get_valid_threshold(threshold):
    try:
        return service.get_valid_threshold(threshold)
    except service.ThresholdOutOfRangeException as e:
        abort_bad_request(e.message)
    except service.ThresholdNotAnIntegerException as e:
        abort_bad_request(e.message)

def serialize_outliers(outliers_throughput):
    return [{'uuid' : uuid, 'throughput' : throughput}
            for uuid, throughput in outliers_throughput.iteritems()]

@app.route('/v1/clusters/caches/outliers')
def get_all_outliers():
    threshold = get_valid_threshold(request.args.get('threshold'))
    try:
        return service.get_all_outliers(threshold)
    except service.CachesRequestFailedException as e:
        abort_internal_error(e.message)

@app.route('/v1/clusters/<cluster>/caches/outliers')
def get_cluster_outliers(cluster):
    threshold = get_valid_threshold(request.args.get('threshold'))
    try:
        outliers_throughput, cluster_average = \
            service.get_cluster_outliers(cluster, threshold)
    except service.ClusterNotFoundException as e:
        abort_not_found(e.message)
    except service.CachesRequestFailedException as e:
        abort_internal_error(e.message)
    return jsonify(cluster=cluster,
                   outliers=serialize_outliers(outliers_throughput),
                   averageThroughput=cluster_average,
                   threshold=threshold,
                   message=OUTLIER_DESCRIPTION)
