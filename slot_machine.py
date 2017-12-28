import random
from collections import namedtuple


Symbol = namedtuple('Symbol', 'code is_wild')
Paytable = namedtuple('Paytable', 'symbol count payout')


class SlotMachine:
    def __init__(self, reel_heights, symboldefs, paytables, paylines, reels):
        self.reel_heights = reel_heights
        self.symboldefs = symboldefs
        self.paytables = paytables
        self.paylines = paylines
        self.reels = reels


class Result:
    def __init__(self, coin_in, stop_pos, symbols, coin_out):
        self.coin_in = coin_in
        self.stop_pos = stop_pos
        self.symbols = symbols      # symbol sequence by rows by top to bottom
        self.coin_out = coin_out


def get_line_symbols(reel_lens, symbols, payline):
    line_symbols = []
    reel_start = 0
    for reel, row in enumerate(payline):
        reel_start += reel_lens[reel-1] if reel != 0 else 0
        reel_end = reel_start + reel_lens[reel]
        line_symbols.append(symbols[reel_start:reel_end][row])
    return tuple(line_symbols)


def spin(machine, coin_in, stops=None):
    if not stops:
        stops = tuple(random.randrange(len(reel)) for reel in machine.reels)

    symbol_list = []
    for reel_no, reel_height in enumerate(machine.reel_heights):
        stop = stops[reel_no]
        reel = machine.reels[reel_no]
        reel_len = len(reel)
        for row in range(reel_height):
            i = (stop + row) % reel_len
            symbol_list.append(reel[i])
    symbols = tuple(symbol_list)

    results = []
    for payline in machine.paylines:
        line_symbols = get_line_symbols(machine.reel_heights, symbols, payline)
        payout_rate = calc_payout_rate(machine.symboldefs, machine.paytables, line_symbols)
        coin_out = coin_in * payout_rate

        if coin_out > 0:
            results.append(Result(coin_in, stops, symbols, coin_out))

    return results


def fst(iterable):
    return iterable[0]


def is_wild(symboldefs, symbol):
    for s in symboldefs:
        if s.code == symbol and s.is_wild:
            return True
    return False


def get_left_symbol(symboldefs, symbols):
    left_symbol = fst(symbols)
    if is_wild(symboldefs, left_symbol):
        for s in symbols:
            if not is_wild(symboldefs, s):
                left_symbol = s
                break
    return left_symbol


def get_left_match(symboldefs, symbols, left_symbol):
    matches = 0
    for s in symbols:
        if s == left_symbol or is_wild(symboldefs, s):
            matches += 1
        else:
            break
    return matches


def get_payout(paytables, symbol, matches):
    payout = 0
    for paytable in paytables:
        if paytable.symbol == symbol and matches == paytable.count:
            payout = paytable.payout
            break
    return payout


def calc_payout_rate(symboldefs, paytables, symbols):
    l_symbol = get_left_symbol(symboldefs, symbols)
    matches = get_left_match(symboldefs, symbols, l_symbol)
    return get_payout(paytables, l_symbol, matches)


def get_total_coin_out(results):
    return sum([r.coin_out for r in results])


if __name__ == '__main__':
    machine = SlotMachine((3, 3, 3, 3, 3),
                          (Symbol('W', True),
                           Symbol('A', False),
                           Symbol('B', False),
                           Symbol('C', False),
                           Symbol('D', False),
                           Symbol('E', False)),
                          (Paytable('A', 5, 100),
                           Paytable('A', 4, 50),
                           Paytable('A', 3, 20),
                           Paytable('B', 5, 80),
                           Paytable('B', 3, 40),
                           Paytable('B', 2, 10),
                           Paytable('C', 5, 30),
                           Paytable('C', 4, 20),
                           Paytable('C', 3, 10),
                           Paytable('D', 5, 20),
                           Paytable('D', 4, 10),
                           Paytable('D', 3, 5),
                           Paytable('E', 5, 20),
                           Paytable('E', 4, 10),
                           Paytable('E', 3, 5)),
                          ((0, 0, 0, 0, 0),
                           (1, 1, 1, 1, 1),
                           (2, 2, 2, 2, 2),
                           (0, 1, 1, 1, 2),
                           (2, 1, 1, 1, 0),
                           (0, 0, 0, 1, 2),
                           (2, 1, 0, 0, 0),
                           (0, 0, 1, 2, 2),
                           (2, 2, 1, 0, 0)),
                          (('W', 'A', 'B', 'C', 'D', 'E'),
                           ('W', 'A', 'B', 'C', 'D', 'E'),
                           ('W', 'A', 'B', 'C', 'D', 'E'),
                           ('W', 'A', 'B', 'C', 'D', 'E'),
                           ('W', 'A', 'B', 'C', 'D', 'E')))

    total_coin_out = 0
    for _ in range(20):
        results = spin(machine, 10)
        total_coin_out += get_total_coin_out(results)
    print('total coin out = ', total_coin_out)
