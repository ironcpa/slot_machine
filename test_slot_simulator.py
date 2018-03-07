import unittest
from unittest import TestCase
from slot_data import Symbol, Paytable, Payline
import slot_machine as sm
from slot_machine import Result, PaylineResult, \
                         SlotMachine2, make_reel
import simulator as ss
from simulator import simulate_slot


def make_test_result(line_bet, coin_in, coin_out):
    line_results = [PaylineResult(0, coin_out)]
    result = Result('normal', line_bet, coin_in, 1, ['a', 'b', 'c'], line_results)
    return result


def create_test_machine():
    machine = SlotMachine2(reel_heights=(3, 3, 3),
                           symboldefs=(Symbol(1, 'A', 'a', None),
                                       Symbol(2, 'B', 'b', None),
                                       Symbol(3, 'C', 'c', None)),
                           paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                     Payline(id=1, r0=1, r1=1, r2=1),
                                     Payline(id=2, r0=2, r1=2, r2=2),),
                           paytables=(Paytable('A', 3, 100),),
                           reels={'normal': make_reel(
                                             'normal',
                                             ('A', 'B', 'C'),
                                             ('A', 'B', 'C'),
                                             ('A', 'B', 'C'))})

    return machine


class TestSlotSimulator(TestCase):
    def test_single_run(self):
        results = simulate_slot(create_test_machine(), 1)

        self.assertEqual(len(results), 1)
        self.assertEqual(type(results[0]), sm.Result)

    def test_multi_run(self):
        results = simulate_slot(create_test_machine(), 2)

        self.assertEqual(len(results), 2)
        for r in results:
            self.assertEqual(type(r), sm.Result)

    def test_dummy_machine_summary_data(self):
        results = [make_test_result(10, 10, 10),
                   make_test_result(10, 10, 50),
                   make_test_result(10, 10, 100),
                   make_test_result(10, 10, 100),
                   make_test_result(10, 10, 0),
                   make_test_result(10, 10, 100)]
        summary = ss.make_summary(results)

        self.assertEqual(summary.spins, 6)
        self.assertEqual(summary.wins, 5)
        self.assertEqual(summary.coin_in, 60)
        self.assertEqual(summary.coin_out, 360)
        self.assertEqual(ss.payout(summary), 360 / 60)
        self.assertEqual(ss.loss_rate(summary), 5 / 6)

    def test_machine_summary_data(self):
        machine = create_test_machine()

        stop_plan = {0: (0, 0, 0),
                     1: (1, 1, 1),
                     2: (2, 2, 2)}

        results = simulate_slot(machine, 1, stop_plan)
        summary = ss.make_summary(results)

        self.assertEqual(summary.spins, 1)
        self.assertEqual(summary.wins, 1)
        self.assertEqual(summary.coin_in, 3)
        self.assertEqual(summary.coin_out, 100)

        results = simulate_slot(machine, 3, stop_plan)
        summary = ss.make_summary(results)

        self.assertEqual(summary.spins, 3)
        self.assertEqual(summary.wins, 3)
        self.assertEqual(summary.coin_in, 9)
        self.assertEqual(summary.coin_out, 300)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSlotSimulator)
    unittest.TextTestRunner(verbosity=2).run(suite)
