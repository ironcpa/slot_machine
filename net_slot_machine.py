import urllib.request


url_form = 'http://localhost:5000/spin?coin_in={}&times={}'


def spin(coin_in, is_free=False, plan_stops=None):
    url = url_form.format(coin_in, 1)
    data = urllib.request.urlopen(url).read()
    return data


def spins(coin_in, times, plan_stops=None):
    url = url_form.format(coin_in, times)
    res_data = urllib.request.urlopen(url).read()
    return res_data
