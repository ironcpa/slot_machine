import unittest
from unittest import TestCase
import slot_machine as sm
from slot_machine import *
import simulator as ss
from simulator import *


def make_test_result(coin_in, coin_out):
    line_results = [PaylineResult(0, coin_out)]
    result = Result('normal', coin_in, 1, ['a', 'b', 'c'], line_results)
    return result


class TestSlotSimulator(TestCase):
    def test_single_run(self):
        results = simulate_slot(1)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(type(results[0]), sm.Result)

    def test_multi_run(self):
        results = simulate_slot(2)

        self.assertEqual(len(results), 2)
        for r in results:
            self.assertEqual(type(r), sm.Result)

    def test_summary_data(self):
        results = simulate_slot(10)
        summary = ss.make_summary(results)

        self.assertEqual(summary.spins, 10)
        
        results = [make_test_result(10, 10),
                   make_test_result(10, 50),
                   make_test_result(10, 100),
                   make_test_result(10, 100),
                   make_test_result(10, 100)]
        summary = ss.make_summary(results)

        self.assertEqual(summary.spins, 5)
        self.assertEqual(summary.coin_in, 50)
        self.assertEqual(summary.coin_out, 360)
        self.assertEqual(ss.payout(summary), 360 / 50)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSlotSimulator)
    unittest.TextTestRunner(verbosity=2).run(suite)
