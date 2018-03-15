from collections import namedtuple


Summary = namedtuple('Summary', 'spins wins coin_in coin_out')

MachineInfo = namedtuple('MachineInfo', 'name layout paylines scatter_spec')
RTPData = namedtuple('RTPData', '')
ScatterHit = namedtuple('ScatterHit', 'match reward value')


class SimCollector():
    def __init__(self):
        self.line_bet = 0
        self.spins = 0
        self.wins = []
        self.scatter_hits = []


class SimSummary():
    def __init__(self):
        self.machine_info = MachineInfo()
        self.category_data = {}
        self.rtp_data = RTPData()

