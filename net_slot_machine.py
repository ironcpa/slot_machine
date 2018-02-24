import urllib.request
import json


spin_url_form = 'http://localhost:5000/spin?coin_in={}&times={}'
slot_def_url = 'http://localhost:5000/slot_def'


def get_slot_def():
    '''
    return (3, 3, 3, 3, 3), \
           ((0, 0, 0, 0, 0),
            (1, 1, 1, 1, 1),
            (2, 2, 2, 2, 2),
            (0, 1, 1, 1, 2),
            (2, 1, 1, 1, 0),
            (0, 0, 0, 1, 2),
            (2, 1, 0, 0, 0),
            (0, 0, 1, 2, 2),
            (2, 2, 1, 0, 0))
            '''
    slot_def_json = urllib.request.urlopen(slot_def_url).read()
    dic = json.loads(slot_def_json)
    return dic['reel_heights'], dic['paylines']


def spin(coin_in, is_free=False, plan_stops=None):
    url = spin_url_form.format(coin_in, 1)
    data = urllib.request.urlopen(url).read()
    return data


def spins(coin_in, times, plan_stops=None):
    url = spin_url_form.format(coin_in, times)
    res_data = urllib.request.urlopen(url).read()
    return res_data
