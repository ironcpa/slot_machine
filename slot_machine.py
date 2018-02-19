import random
import pdb
from collections import namedtuple

INDENT = ' ' * 4

Symbol = namedtuple('Symbol', 'code is_wild')
Paytable = namedtuple('Paytable', 'symbol count payout')
ScatterPaytable = namedtuple('ScatterPaytable', 'symbol count type reward')


class SlotMachine:
    def __init__(self, reel_heights, symboldefs, paytables, scatter_paytables, paylines, reels, free_reels=None):
        self.reel_heights = reel_heights
        self.symboldefs = symboldefs
        self.paytables = paytables
        self.scatter_paytables = scatter_paytables
        self.paylines = paylines
        self.reels = reels
        self.free_reels = free_reels


class PaylineResult:
    def __init__(self, line_id, coin_out):
        self.line_id = line_id
        self.coin_out = coin_out


class ScatterResult:
    def __init__(self, symbol, count, coin_out, freespins=0):
        self.symbol = symbol
        self.count = count
        self.coin_out = coin_out
        self.freespins = freespins
        self.child_results = []


class Result:
    def __init__(self, spin_type, coin_in, stop_pos, symbols, line_results, scatter_results = []):
        self.spin_type = spin_type
        self.coin_in = coin_in
        self.stop_pos = stop_pos
        self.symbols = symbols      # symbol sequence by rows by top to bottom
        self.line_results = line_results
        self.scatter_results = scatter_results

    def len(self):
        return len(self.line_results)

    def fst(self):
        if self.line_results and self.len() > 0:
            return self.line_results[0]
        return None


def get_line_symbols(reel_lens, symbols, payline):
    line_symbols = []
    reel_start = 0
    for reel, row in enumerate(payline):
        reel_start += reel_lens[reel-1] if reel != 0 else 0
        reel_end = reel_start + reel_lens[reel]
        line_symbols.append(symbols[reel_start:reel_end][row])
    return tuple(line_symbols)


def spin(machine, coin_in, is_free=False, reserved_reelstops=None):
    if reserved_reelstops and type(reserved_reelstops) is not list:
        reserved_reelstops = [reserved_reelstops]

    target_reel = None
    if is_free:
        target_reel = machine.free_reels
    else:
        target_reel = machine.reels

    if reserved_reelstops and len(reserved_reelstops) > 0:
        reelstop = reserved_reelstops.pop(0)
    else:
        reelstop = tuple(random.randrange(len(reel)) for reel in target_reel)

    symbol_list = []
    for reel_no, reel_height in enumerate(machine.reel_heights):
        stop = reelstop[reel_no]
        reel = target_reel[reel_no]
        reel_len = len(reel)
        for row in range(reel_height):
            i = (stop + row) % reel_len
            symbol_list.append(reel[i])
    symbols = tuple(symbol_list)

    line_results = []
    for i, payline in enumerate(machine.paylines):
        line_symbols = get_line_symbols(machine.reel_heights, symbols, payline)
        payout_rate = calc_payout_rate(machine.symboldefs, machine.paytables, line_symbols)
        coin_out = coin_in * payout_rate

        if coin_out > 0:
            line_results.append(PaylineResult(i, coin_out))

    scatter_results = get_scatter_results(machine, coin_in, symbol_list)
    for sr in scatter_results:
        if sr.freespins > 0:
            for _ in range(sr.freespins):
                sr.child_results.append(spin(machine, coin_in, True, reserved_reelstops))

    spin_type = 'free' if is_free else 'normal'
    return Result(spin_type, coin_in, reelstop, symbols, line_results, scatter_results) 

def get_scatter_results(machine, coin_in, symbol_list):
    scatter_results = []
    
    for table in machine.scatter_paytables:
        scatter = table.symbol 
        match = 0
        payout = 0
        freespins = 0
        for s in symbol_list:
            if s == scatter:
                match += 1
        if table.symbol == scatter and table.count == match:
            if table.type is 'payout':
                payout = coin_in * table.reward
            elif table.type is 'freespin':
                freespins = table.reward
            scatter_results.append(ScatterResult(scatter, match, payout, freespins))

    return scatter_results


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


def get_total_coin_out(spin_result):
    #return sum([r.coin_out for r in spin_result.line_results])

    coin_out = 0

    for l in spin_result.line_results:
        coin_out += l.coin_out
    for s in spin_result.scatter_results:
        coin_out += s.coin_out
        for cr in s.child_results:
            coin_out += get_total_coin_out(cr)

    return coin_out


def get_symbols_per_line(reel_heights, symbol_list):
    max_reel = len(reel_heights)
    max_row = reel_heights[0]
    lines = [[None for reel in range(max_reel)] for row in range(max_row)]
    for reel in range(max_reel):
        for row in range(max_row):
            lines[row][reel] = symbol_list[max_row * reel + row]
    return lines   


def get_payline_symbols(reel_lens, symbols, payline):
    return get_line_symbols(reel_lens, symbols, payline)


def make_indents(tabs):
    return INDENT * tabs
    

def create_log_header(tabs, s):
    max_len = 60
    tail_len = max_len - tabs * len(INDENT)
    if tail_len < 0:
        tail_len = 0
    return ('{:=<'+str(tail_len)+'}').format(s + ' ')


def make_spin_log(tabs, reel_heights, spin_result):
    log = ''
    indents = make_indents(tabs)

    log += '{:02d} spin: coin_in={}\n'.format(i, spin_result.coin_in)
    log += indents + 'stop={}\n'.format(spin_result.stop_pos)
    log += indents + create_log_header(tabs, 'symbols') + '\n'
    symbols_txt = INDENT + ('\n'+indents+INDENT).join([str(x) for x in get_symbols_per_line(reel_heights, spin_result.symbols)])
    log += indents + '{}\n'.format(symbols_txt)
    if len(spin_result.line_results) > 0:
        log += indents + '{}\n'.format(create_log_header(tabs, 'win lines') + ' ' + str(len(spin_result.line_results)))
    log += make_payline_log(tabs+1, reel_heights, spin_result)
    if len(spin_result.scatter_results) > 0:
        log += indents + create_log_header(tabs, 'scatter result') + '\n'
        log += make_scatter_log(tabs+1, reel_heights, spin_result)

    total_coin_out = get_total_coin_out(spin_result)
    log += indents + 'total coin out = {}\n'.format(total_coin_out)

    return log


def create_symbol_log(lines):
    symbols = '['
    for i, l in enumerate(lines):
        symbols += ', '.join(l)
        symbols += ' : ' if (i+1) < len(lines) else ''
    symbols += ']'

    return symbols


def make_payline_log(tabs, reel_heights, result):
    indents = make_indents(tabs)

    lines = get_symbols_per_line(reel_heights, result.symbols)
    symbols = create_symbol_log(lines)

    line_results = result.line_results
    log = ''
    for r in line_results:
        log += indents + 'line{:02d}, {}, {}\n'.format(r.line_id, result.coin_in, r.coin_out)

    return log


def make_scatter_log(tabs, reel_heights, result):
    log = ''
    indents = make_indents(tabs)

    scatter_results = result.scatter_results
    for sr in scatter_results:
        log += indents + 'scatters: {}, {}, {}\n'.format(sr.symbol, sr.count, sr.freespins) 
        if len(sr.child_results) > 0:
            log += indents + create_log_header(tabs, 'child results') + '\n'
            for n, cr in enumerate(sr.child_results):
                log += indents + make_spin_log(tabs+1, reel_heights, cr)

    return log


if __name__ == '__main__':
    machine = SlotMachine((3, 3, 3, 3, 3),
                          (Symbol('W', True),
                           Symbol('A', False),
                           Symbol('B', False),
                           Symbol('C', False),
                           Symbol('D', False),
                           Symbol('E', False),
                           Symbol('S', False)),
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
                          (ScatterPaytable('S', 3, 'freespin', 3),),
                          ((0, 0, 0, 0, 0),
                           (1, 1, 1, 1, 1),
                           (2, 2, 2, 2, 2),
                           (0, 1, 1, 1, 2),
                           (2, 1, 1, 1, 0),
                           (0, 0, 0, 1, 2),
                           (2, 1, 0, 0, 0),
                           (0, 0, 1, 2, 2),
                           (2, 2, 1, 0, 0)),
                          (('W', 'A', 'B', 'C', 'D', 'E', 'S'),
                           ('W', 'A', 'B', 'C', 'D', 'E'),
                           ('W', 'A', 'B', 'C', 'D', 'E', 'S'),
                           ('W', 'A', 'B', 'C', 'D', 'E'),
                           ('W', 'A', 'B', 'C', 'D', 'E', 'S')),
                          (('S', 'W', 'A', 'B', 'C', 'D', 'E'),
                           ('S', 'W', 'A', 'B', 'C', 'D', 'E'),
                           ('S', 'W', 'A', 'B', 'C', 'D', 'E'),
                           ('S', 'W', 'A', 'B', 'C', 'D', 'E'),
                           ('S', 'W', 'A', 'B', 'C', 'D', 'E')))

    test_spins = 10
    total_spins = 0
    total_coin_out = 0
    for i in range(test_spins):
        results = spin(machine, 10, False, (4, 0, 4, 0, 4))
        #results = spin(machine, 10, False, (0, 0, 0, 0, 0))
        #results = spin(machine, 10)
        #make_spin_log(machine.reel_heights, results)
        print(make_spin_log(0, machine.reel_heights, results))

