from exceptions import (ClusterNotFoundException,
                        ThresholdNotAnIntegerException,
                        ThresholdOutOfRangeException)

def get_default_threshold():
    # todo: check configuration for default threshold
    return 20

def validate_threshold(threshold):
    try:
        threshold = int(threshold)
    except ValueError:
        raise ThresholdNotAnIntegerException(
            'outlier threshold must be an integer')
    if threshold <= 0 or threshold >= 100:
        raise ThresholdOutOfRangeException(
            'outlier threshold must be between 1% and 99%')
    return threshold

def get_threshold(threshold):
    if threshold is None:
        return get_default_threshold()
    else:
        return validate_threshold(threshold)

def get_all_outliers(threshold):
    return 'threshold  %d' % threshold

def cluster_exists(cluster):
    return False

def get_cluster_outliers(cluster, threshold):
    if not cluster_exists(cluster):
        raise ClusterNotFoundException(
            'cluster "%s" does not exist' % cluster)
    return 'cluster %s threshold %d' % (cluster, threshold)
