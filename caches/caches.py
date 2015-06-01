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
        raise RequestFailedException(url)

def make_dict_of_lists(jsons, key, value):
    result = defaultdict(list)
    for json in jsons:
        if key in json and value in json:
            result[json[key]].append(json[value])
    return result

def make_dict_of_items(jsons, key, value):
    return {json[key] : json[value]
            for json in jsons
            if key in json and value in json}

def get_caches_by_cluster():
    # todo: cache result, refresh at intervals.
    response = get_with_error_checking(CACHES_BASE_URL)
    return make_dict_of_lists(response.json(), 'cluster', 'uuid')

def get_cache_throughputs():
    response = get_with_error_checking(CACHES_BASE_URL + 'throughput')
    return make_dict_of_items(response.json(), 'uuid', 'value')

