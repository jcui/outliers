from flask import (Flask, Response, abort, json, request)
from service import service

app = Flask(__name__)

OUTLIER_DESCRIPTION = \
    'outlier throughputs differ from average by more than threshold %'

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

def serialize_outliers(outlier_throughputs):
    return [{'uuid' : uuid, 'throughput' : throughput}
            for uuid, throughput in outlier_throughputs.iteritems()]

def make_response_dict(cluster,
                       outlier_throughputs,
                       cluster_average,
                       threshold):
    return {'cluster' : cluster,
            'outliers' : serialize_outliers(outlier_throughputs),
            'averageThroughput' : cluster_average,
            'threshold' : threshold,
            'description' : OUTLIER_DESCRIPTION}

def make_json_response(content):
    return Response(json.dumps(content, indent=2),
                    status=200,
                    mimetype='application/json')

@app.route('/v1/clusters/<cluster>/caches/outliers')
def get_cluster_outliers(cluster):
    threshold = get_valid_threshold(request.args.get('threshold'))
    try:
        outlier_throughputs, cluster_average = \
            service.get_cluster_outliers(cluster, threshold)
    except service.ClusterNotFoundException as e:
        abort_not_found(e.message)
    except service.CachesRequestFailedException as e:
        abort_internal_error(e.message)
    response_dict = make_response_dict(cluster,
                                       outlier_throughputs,
                                       cluster_average,
                                       threshold)
    return make_json_response(response_dict)

@app.route('/v1/clusters/caches/outliers')
def get_all_outliers():
    threshold = get_valid_threshold(request.args.get('threshold'))
    try:
        all_outliers = service.get_all_outliers(threshold)
    except service.CachesRequestFailedException as e:
        abort_internal_error(e.message)
    response_dicts = []
    for cluster_outliers in all_outliers:
        cluster, outlier_throughputs, cluster_average = cluster_outliers
        response_dicts.append(make_response_dict(cluster,
                                                 outlier_throughputs,
                                                 cluster_average,
                                                 threshold))
    return make_json_response(response_dicts)
