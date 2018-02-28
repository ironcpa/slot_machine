class PaylineResult:
    def __init__(self, line_id, coin_out):
        self.line_id = line_id
        self.coin_out = coin_out


class ScatterResult:
    def __init__(self, symbol, count, coin_out, freespins=0, child_results=None):
        self.symbol = symbol
        self.count = count
        self.coin_out = coin_out
        self.freespins = freespins
        if child_results:
            self.child_results = child_results
        else:
            self.child_results = []


class Result:
    def __init__(self,
                 spin_type,
                 coin_in,
                 stop_pos,
                 symbols,
                 line_results,
                 scatter_results=[]):
        self.spin_type = spin_type
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
