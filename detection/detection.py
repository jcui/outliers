def make_dict_subset(keys, input_dict):
    return {key : input_dict[key] for key in keys if key in input_dict}

def is_outlier(throughput, average, threshold):
    return average > 0.00000000001 and \
           (abs(throughput - average) / float(average)) > (threshold / 100.0)

def find_outlier_throughputs(cache_throughputs, average, threshold):
    return {uuid : throughput
            for uuid, throughput in cache_throughputs.iteritems()
            if is_outlier(throughput, average, threshold)}

def find_outliers(cluster_caches, all_cache_throughputs, threshold):
    cache_throughputs = make_dict_subset(cluster_caches,
                                         all_cache_throughputs)
    cluster_average = 0
    outlier_throughputs = {}
    if len(cache_throughputs) > 0:
        cluster_average = \
            sum(cache_throughputs.values()) / len(cache_throughputs)
        outlier_throughputs = find_outlier_throughputs(cache_throughputs,
                                                       cluster_average,
                                                       threshold)
    return (outlier_throughputs, cluster_average)
