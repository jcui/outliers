from flask import Flask, request, abort

app = Flask(__name__)

def run(debug):
    app.debug = debug
    app.run()

def abort_bad_request(message):
    abort(400, message)

def get_default_threshold():
    # todo: check configuration for default threshold
    return 20

def validate_threshold(threshold):
    try:
        threshold = int(threshold)
        if threshold < 0 or threshold > 100:
            abort_bad_request('outlier threshold must be between 0 and 100')
        return threshold
    except ValueError:
        abort_bad_request('outlier threshold must be an integer')

def get_threshold(threshold):
    if threshold is None:
        return get_default_threshold()
    else:
        return validate_threshold(threshold)

@app.route('/clusters/caches/outliers')
def get_all_outliers():
    threshold = get_threshold(request.args.get('threshold'))
    return 'threshold  %d' % threshold

@app.route('/clusters/<cluster>/caches/outliers')
def get_cluster_outliers(cluster):
    threshold = get_threshold(request.args.get('threshold'))
    return 'cluster %s threshold %d' % (cluster, threshold)
