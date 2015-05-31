from collections import namedtuple

Outliers = namedtuple('Outliers', 'outliers_throughput cluster_average')

def dict_subset(key_list, input_dict):
    return {key : input_dict[key] for key in key_list if key in input_dict}

def is_outlier(throughput, average, threshold):
    return average > 0.00000000001 \
           and (abs(throughput - average) / float(average)) > (threshold / 100.0)

def get_outliers_throughput(caches_throughput, average, threshold):
    return {uuid : throughput
            for uuid, throughput in caches_throughput.iteritems()
            if is_outlier(throughput, average, threshold)}

def find_outliers(caches_in_cluster, all_caches_throughput, threshold):
    caches_throughput = dict_subset(caches_in_cluster,
                                    all_caches_throughput)
    cluster_average = 0
    outliers_throughput = {}
    if (len(caches_throughput) > 0):
        cluster_average = sum(caches_throughput.values()) / len(caches_throughput)
        outliers_throughput = get_outliers_throughput(caches_throughput,
                                                      cluster_average,
                                                      threshold)
    return Outliers(outliers_throughput, cluster_average)
