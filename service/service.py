from caches import caches
from detection import detection
from exceptions import (ClusterNotFoundException,
                        CachesRequestFailedException,
                        ThresholdNotAnIntegerException,
                        ThresholdOutOfRangeException)

def get_default_threshold():
    # todo: check configuration for default threshold,
    #       can be set using api call.
    DEFAULT_THRESHOLD = 20
    return DEFAULT_THRESHOLD

def validate_threshold(threshold):
    try:
        threshold = int(threshold)
    except ValueError:
        raise ThresholdNotAnIntegerException(
            'outlier threshold must be an integer')
    if threshold <= 0:
        raise ThresholdOutOfRangeException(
            'outlier threshold must be at least 1')
    return threshold

def get_valid_threshold(threshold):
    if threshold is None:
        return get_default_threshold()
    else:
        return validate_threshold(threshold)

def get_caches_by_cluster():
    try:
        return caches.get_caches_by_cluster()
    except caches.RequestFailedException as e:
        raise CachesRequestFailedException(e.message)

def get_cache_throughputs():
    try:
        return caches.get_cache_throughputs()
    except caches.RequestFailedException as e:
        raise CachesRequestFailedException(e.message)

def get_cluster_outliers(cluster, threshold):
    caches_by_cluster = get_caches_by_cluster()
    if cluster not in caches_by_cluster:
        raise ClusterNotFoundException(
            'cluster "%s" does not exist' % cluster)
    all_cache_throughputs = get_cache_throughputs()
    return detection.find_outliers(caches_by_cluster[cluster],
                                   all_cache_throughputs,
                                   threshold)

def get_all_outliers(threshold):
    caches_by_cluster = get_caches_by_cluster()
    all_cache_throughputs = get_cache_throughputs()
    all_outliers = []
    for cluster, cluster_caches in caches_by_cluster.iteritems():
        outlier_throughputs, cluster_average = \
            detection.find_outliers(cluster_caches,
                                    all_cache_throughputs,
                                    threshold)
        if len(outlier_throughputs) > 0:
            all_outliers.append((cluster,
                                 outlier_throughputs,
                                 cluster_average))
    return all_outliers

