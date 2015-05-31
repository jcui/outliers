from exceptions import (ClusterNotFoundException,
                        QueryCachesFailedException,
                        ThresholdNotAnIntegerException,
                        ThresholdOutOfRangeException)
from caches import caches

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

def get_caches_by_cluster():
    try:
        return caches.get_caches_by_cluster()
    except caches.QueryFailedException as e:
        raise QueryCachesFailedException(e.message)

def get_cluster_outliers(cluster, threshold):
    caches_by_cluster = get_caches_by_cluster()
    if cluster not in caches_by_cluster:
        raise ClusterNotFoundException(
            'cluster "%s" does not exist' % cluster)
    return 'cluster %s threshold %d' % (cluster, threshold)

def get_all_outliers(threshold):
    return 'threshold  %d' % threshold
