import urllib.request


url_form = 'http://localhost:5000/spin?coin_in={}&times={}'


class DummySlotMachine:
    def __init__(self,
                 reel_heights=(),
                 paylines=()):
        self.reel_heights = reel_heights
        self.paylines = paylines


def get_dummy_machine():
    return DummySlotMachine(reel_heights=(3, 3, 3, 3, 3),
                            paylines=((0, 0, 0, 0, 0),
                                      (1, 1, 1, 1, 1),
                                      (2, 2, 2, 2, 2),
                                      (0, 1, 1, 1, 2),
                                      (2, 1, 1, 1, 0),
                                      (0, 0, 0, 1, 2),
                                      (2, 1, 0, 0, 0),
                                      (0, 0, 1, 2, 2),
                                      (2, 2, 1, 0, 0)))


def spin(coin_in, is_free=False, plan_stops=None):
    url = url_form.format(coin_in, 1)
    data = urllib.request.urlopen(url).read()
    return data


def spins(coin_in, times, plan_stops=None):
    url = url_form.format(coin_in, times)
    res_data = urllib.request.urlopen(url).read()
    return res_data
