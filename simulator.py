from collections import namedtuple
import slot_machine
from slot_machine import *

Summary = namedtuple('Summary', 'spins coin_in coin_out')


def simulate_slot(count):
    results = []
    for n in range(count):
        line_results = [PaylineResult(0, 0),
                        PaylineResult(1, 1),]
        result = Result('normal', 1, 1, ['a', 'b', 'c'], line_results)
        results.append(result)

    return results

def make_summary(spin_results):
    total_coin_in = 0
    total_coin_out = 0
    for r in spin_results:
        total_coin_in += r.coin_in
        for lr in r.line_results:
            total_coin_out += lr.coin_out

    summary = Summary(len(spin_results), total_coin_in, total_coin_out)

    return summary

def payout(summary):
    payout = summary.coin_out / summary.coin_in
    return payout
