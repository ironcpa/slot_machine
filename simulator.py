from collections import namedtuple
from slot_machine import spin, create_sample_machine, make_spin_log
import local_window


Summary = namedtuple('Summary', 'spins wins coin_in coin_out')


def simulate_slot(machine, count, stop_plan=None):
    coin_in = 1 * len(machine.paylines)

    results = []
    for n in range(count):
        if stop_plan:
            result = spin(machine, coin_in, False, stop_plan[n])
        else:
            result = spin(machine, coin_in)

        results.append(result)

    return results


def make_summary(spin_results):
    total_coin_in = 0
    total_coin_out = 0
    total_wins = 0

    for r in spin_results:
        total_coin_in += r.coin_in

        r_coin_out = 0
        for lr in r.line_results:
            r_coin_out += lr.coin_out

        total_wins += 1 if r_coin_out > 0 else 0
        total_coin_out += r_coin_out

    summary = Summary(len(spin_results),
                      total_wins,
                      total_coin_in,
                      total_coin_out)

    return summary


def make_summary_print_format(summary):
    format_str = '{} spins, {} wins, total coin in : {}, total coin out : {}'
    form = format_str.format(summary.spins,
                             summary.wins,
                             summary.coin_in,
                             summary.coin_out)

    return form


def payout(summary):
    payout = summary.coin_out / summary.coin_in
    return payout


def loss_rate(summary):
    loss_rate = summary.wins / summary.spins
    return loss_rate


if __name__ == '__main__':
    machine = create_sample_machine()

    results = simulate_slot(machine, 10)
    for n, r in enumerate(results):
        print(make_spin_log(0, machine.reel_heights, n, r))

    summary = make_summary(results)
    print(make_summary_print_format(summary))

    local_window.show_spin_results_window(machine, results)
