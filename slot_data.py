from collections import namedtuple


# Symbol = namedtuple('Symbol', 'code is_wild')
Paytable = namedtuple('Paytable', 'symbol count payout')
ScatterPaytable = namedtuple('ScatterPaytable', 'symbol count type reward')

Symbol = namedtuple('Symbol', 'id code desc type')
BetRange = namedtuple('BetRange', 'line_bet total_bet unlock_level')
ReelSymbol = namedtuple('ReelSymbol', 'symbol weight')


class Payline:
    def __init__(self, id, r0=None, r1=None, r2=None, r3=None, r4=None):
        self.id = id
        self.r0 = r0
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4
        self.rows = (r0, r1, r2, r3, r4)

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return (e for e in self.rows)


class ReelData:
    def __init__(self, name):
        self.name = name
        self._reels = []

    def add_symbol(self, reel, symbol, weight):
        if len(self._reels) < reel+1:
            self._reels.append([])

        self._reels[reel].append(ReelSymbol(symbol, weight))

    def reel(self, index):
        return self._reels[index]

    def reel_len(self, index):
        return len(self._reels[index])

    def __iter__(self):
        return (e for e in self._reels)


class PaylineResult:
    def __init__(self, line_id, coin_out):
        self.line_id = line_id
        self.coin_out = coin_out


class ScatterResult:
    def __init__(self,
                 symbol,
                 count,
                 coin_out,
                 freespins=0,
                 child_results=None):
        if child_results is None:
            child_results = []

        self.symbol = symbol
        self.count = count
        self.coin_out = coin_out
        self.freespins = freespins
        self.child_results = child_results


class Result:
    def __init__(self,
                 spin_type,
                 line_bet,
                 coin_in,
                 stop_pos,
                 symbols,
                 line_results,
                 scatter_results=[]):
        self.spin_type = spin_type
        self.line_bet = line_bet
        self.coin_in = coin_in
        self.stop_pos = stop_pos
        self.symbols = symbols      # symbol sequence by rows by top to bottom
        self.line_results = line_results
        self.scatter_results = scatter_results

    def __repr__(self):
        return '{}, in={}, stop={}, symbols={}, ' \
               'lines={}, scatters={}'.format(self.spin_type,
                                              self.coin_in,
                                              self.stop_pos,
                                              self.symbols,
                                              len(self.line_results),
                                              len(self.scatter_results))

    def len(self):
        return len(self.line_results)

    def fst(self):
        if self.line_results and self.len() > 0:
            return self.line_results[0]
        return None


def to_spin_result(dict_result):
    print('debug:', dict_result)

    line_results = []
    for lr in dict_result['line_results']:
        line_results.append(PaylineResult(lr['line_id'], lr['coin_out']))

    scatter_results = []
    for sr in dict_result['scatter_results']:
        child_results = []
        for cr in sr['child_results']:
            child_results.append(to_spin_result(cr))
        scatter_result = ScatterResult(sr['symbol'],
                                       sr['count'],
                                       sr['coin_out'],
                                       sr['freespins'],
                                       child_results)
        scatter_results.append(scatter_result)

    spin_result = Result(dict_result['spin_type'],
                         dict_result['line_bet'],
                         dict_result['coin_in'],
                         dict_result['stop_pos'],
                         dict_result['symbols'],
                         line_results,
                         scatter_results)
    return spin_result


def get_symbols_per_line(reel_heights, symbol_list):
    max_reel = len(reel_heights)
    max_row = reel_heights[0]
    lines = [[None for reel in range(max_reel)] for row in range(max_row)]
    for reel in range(max_reel):
        for row in range(max_row):
            lines[row][reel] = symbol_list[max_row * reel + row]
    return lines
