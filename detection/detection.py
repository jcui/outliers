def make_dict_subset(keys, input_dict):
    return {key : input_dict[key] for key in keys if key in input_dict}

def is_outlier(throughput, average, threshold):
    return average > 0.00000000001 and \
           (abs(throughput - average) / float(average)) > (threshold / 100.0)

def find_outliers_throughput(caches_throughput, average, threshold):
    return {uuid : throughput
            for uuid, throughput in caches_throughput.iteritems()
            if is_outlier(throughput, average, threshold)}

def find_outliers(cluster_caches, all_caches_throughput, threshold):
    caches_throughput = make_dict_subset(cluster_caches,
                                         all_caches_throughput)
    cluster_average = 0
    outliers_throughput = {}
    if len(caches_throughput) > 0:
        cluster_average = \
            sum(caches_throughput.values()) / len(caches_throughput)
        outliers_throughput = find_outliers_throughput(caches_throughput,
                                                       cluster_average,
                                                       threshold)
    return (outliers_throughput, cluster_average)
