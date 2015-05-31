from exceptions import QueryFailedException
import requests

CACHES_BASE_URL = ('http://ocinterview--frontend-1096888245'
                   '.us-west-2.elb.amazonaws.com/caches/')

def get_with_error_checking(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def get_caches_by_cluster():
    try:
        url = CACHES_BASE_URL
        response = get_with_error_checking(url)
    except requests.exceptions.RequestException:
        raise QueryFailedException('request failed: ' + url)
    return response.json()
