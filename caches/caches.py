import requests
from collections import defaultdict
from exceptions import RequestFailedException

CACHES_BASE_URL = ('http://ocinterview--frontend-1096888245'
                   '.us-west-2.elb.amazonaws.com/caches/')

def get_with_error_checking(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException:
        raise RequestFailedException(
            str(response.status_code) + ': ' + url)

def dict_of_lists(json_list, key, value):
    result = defaultdict(list)
    for json in json_list:
        if key in json and value in json:
            result[json[key]].append(json[value])
    return result

def dict_of_items(json_list, key, value):
    return {json[key] : json[value]
            for json in json_list
            if key in json and value in json}

def get_caches_by_cluster():
    # todo: if caches/clusters do not change often, can save result
    #       in thread-safe structure, refresh at intervals.
    response = get_with_error_checking(CACHES_BASE_URL)
    return dict_of_lists(response.json(), 'cluster', 'uuid')

def get_caches_throughput():
    response = get_with_error_checking(CACHES_BASE_URL + 'throughput')
    return dict_of_items(response.json(), 'uuid', 'value')
