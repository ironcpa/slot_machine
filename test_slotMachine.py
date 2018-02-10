import unittest
from unittest import TestCase
import slot_machine as sm
from slot_machine import *


def assert_true(func, assert_val, actual_val):
    assert_result = assert_val == actual_val
    if not assert_result:
        print('expect:', assert_val, 'actual:', actual_val)
    func(assert_result)


class TestSlotMachine(TestCase):
    def setUp(self):
        self.machine = SlotMachine((1, 1, 1),
                                   (Symbol('W', True),
                                    Symbol('A', False),
                                    Symbol('B', False),
                                    Symbol('C', False)),
                                   (Paytable('A', 3, 100),
                                    Paytable('A', 2, 30),
                                    Paytable('B', 3, 50),
                                    Paytable('C', 3, 20)),
                                   ((0, 0, 0),),
                                   (('A', 'B', 'C', 'A', 'B', 'C'),
                                    ('B', 'C', 'D', 'A', 'B', 'C'),
                                    ('C', 'D', 'E', 'A', 'B', 'C')))

    def tearDown(self):
        pass

    def test_machine(self):
        assert_true(self.assertTrue, self.machine.reel_heights[0], 1)
        assert_true(self.assertTrue, self.machine.reel_heights[1], 1)
        assert_true(self.assertTrue, self.machine.reel_heights[2], 1)

    def assert_common_spin_results(self, result):
        self.assertTrue(len(results) > 0)
        self.assertTrue(result.symbols is not None)

    def test_spin(self):
        result = sm.spin(self.machine, 1)
        if result.len() == 1:
            self.assert_common_spin_results(result)

        result = sm.spin(self.machine, 2)
        if result.len() == 1:
            self.assert_common_spin_results(result)

    def test_reserve_spin(self):
        test_stop = (0, 0, 0)
        result = sm.spin(self.machine, 1, test_stop)
        assert_true(self.assertTrue, 0, result.len())

        test_stop = (0, 0, 1)
        result = sm.spin(self.machine, 1, test_stop)
        assert_true(self.assertTrue, 0, result.len())

    def test_coin_out(self):
        machine = SlotMachine((3, 3, 3),
                              (Symbol('W', True),
                               Symbol('A', False),
                               Symbol('B', False),
                               Symbol('C', False)),
                              (Paytable('A', 3, 100),
                               Paytable('A', 2, 30),
                               Paytable('B', 3, 50),
                               Paytable('C', 3, 20)),
                              ((0, 0, 0),),
                              (('A', 'B', 'C'),
                               ('A', 'B', 'C'),
                               ('A', 'B', 'C')))
        # pay table
        # A x 3 : 100
        # A x 2 : 30
        # B x 3 : 50
        # C x 3 : 20

        test_stop = (0, 0, 0)
        result = sm.spin(machine, 1, test_stop)
        coin_out = result.fst().coin_out
        assert_true(self.assertTrue, 100, coin_out)

        result = sm.spin(machine, 2, test_stop)
        coin_out = result.fst().coin_out
        assert_true(self.assertTrue, 200, coin_out)

        test_stop = (1, 1, 1)
        result = sm.spin(machine, 1, test_stop)
        coin_out = result.fst().coin_out
        assert_true(self.assertTrue, 50, coin_out)

        result = sm.spin(machine, 2, test_stop)
        coin_out = result.fst().coin_out
        assert_true(self.assertTrue, 100, coin_out)

        test_stop = (0, 0, 1)
        result = sm.spin(machine, 1, test_stop)
        coin_out = result.fst().coin_out
        assert_true(self.assertTrue, 30, coin_out)

    def test_multi_row_slot(self):
        machine = SlotMachine((3, 3, 3),
                              (Symbol('W', True),
                               Symbol('A', False),
                               Symbol('B', False),
                               Symbol('C', False)),
                              (Paytable('A', 3, 100),
                               Paytable('A', 2, 30),
                               Paytable('B', 3, 50),
                               Paytable('C', 3, 20)),
                              ((0, 0, 0), (1, 1, 1), (2, 2, 2), (0, 1, 2)),
                              (('A', 'B', 'C'),
                               ('A', 'B', 'C'),
                               ('A', 'B', 'C')))
        # pay table
        # A x 3 : 100
        # A x 2 : 30
        # B x 3 : 50
        # C x 3 : 20

        # payline
        # 0, 0, 0
        # 1, 1, 1
        # 2, 2, 2
        # 0, 1, 2

        test_stop = (0, 0, 0)
        result = sm.spin(machine, 1, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 3, len(line_results))
        assert_true(self.assertTrue, 100, line_results[0].coin_out)
        assert_true(self.assertTrue, 50, line_results[1].coin_out)
        assert_true(self.assertTrue, 20, line_results[2].coin_out)

        # more complex paylines
        machine = SlotMachine((3, 3, 3),
                              (Symbol('W', True),
                               Symbol('A', False),
                               Symbol('B', False),
                               Symbol('C', False)),
                              (Paytable('A', 3, 100),
                               Paytable('A', 2, 30),
                               Paytable('B', 3, 50),
                               Paytable('C', 3, 20)),
                              ((0, 0, 0), (1, 1, 1), (2, 2, 2), (0, 1, 2), (2, 1, 0)),
                              (('A', 'B', 'A', 'B', 'C', 'B', 'C', 'C', 'C'),
                               ('C', 'A', 'C', 'B', 'B', 'B', 'C', 'C', 'C'),
                               ('A', 'B', 'A', 'B', 'C', 'B', 'C', 'C', 'C')))

        test_stop = (0, 0, 0)
        result = sm.spin(machine, 1, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 2, len(line_results))
        assert_true(self.assertTrue, 100, line_results[0].coin_out)
        assert_true(self.assertTrue, 100, line_results[1].coin_out)

        test_stop = (3, 3, 3)
        result = sm.spin(machine, 1, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 4, len(line_results))
        assert_true(self.assertTrue, 50, line_results[0].coin_out)
        assert_true(self.assertTrue, 50, line_results[1].coin_out)
        assert_true(self.assertTrue, 50, line_results[2].coin_out)
        assert_true(self.assertTrue, 50, line_results[3].coin_out)

        test_stop = (6, 6, 6)
        result = sm.spin(machine, 1, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 5, len(line_results))
        assert_true(self.assertTrue, 20, line_results[0].coin_out)
        assert_true(self.assertTrue, 20, line_results[1].coin_out)
        assert_true(self.assertTrue, 20, line_results[2].coin_out)
        assert_true(self.assertTrue, 20, line_results[3].coin_out)
        assert_true(self.assertTrue, 20, line_results[4].coin_out)

    def test_total_payout(self):
        machine = SlotMachine((3, 3, 3),
                              (Symbol('W', True),
                               Symbol('A', False),
                               Symbol('B', False),
                               Symbol('C', False)),
                              (Paytable('A', 3, 100),
                               Paytable('A', 2, 30),
                               Paytable('B', 3, 50),
                               Paytable('C', 3, 20)),
                              ((0, 0, 0), (1, 1, 1), (2, 2, 2), (0, 1, 2)),
                              (('A', 'B', 'C'),
                               ('A', 'B', 'C'),
                               ('A', 'B', 'C')))

        test_stop = (0, 0, 0)
        results = sm.spin(machine, 1, test_stop)
        assert_true(self.assertTrue, 170, sm.get_total_coin_out(results))

    def test_paytable(self):
        machine = SlotMachine((3, 3, 3),
                              (Symbol('W', True),
                               Symbol('A', False),
                               Symbol('B', False),
                               Symbol('C', False)),
                              (Paytable('A', 3, 200),
                               Paytable('A', 2, 100),
                               Paytable('B', 3, 80),
                               Paytable('C', 3, 30)),
                              ((0, 0, 0), (1, 1, 1), (2, 2, 2), (0, 1, 2)),
                              (('A', 'B', 'C'),
                               ('A', 'B', 'C'),
                               ('A', 'B', 'C')))

        test_stop = (0, 0, 0)
        results = sm.spin(machine, 1, test_stop)
        assert_true(self.assertTrue, 200 + 80 + 30, sm.get_total_coin_out(results))

    def test_wild(self):
        machine = SlotMachine((3, 3, 3),
                              (Symbol('W', True),
                               Symbol('A', False),
                               Symbol('B', False),
                               Symbol('C', False)),
                              (Paytable('A', 3, 200),
                               Paytable('A', 2, 100),
                               Paytable('B', 3, 80),
                               Paytable('C', 3, 30)),
                              ((0, 0, 0), (1, 1, 1), (2, 2, 2), (0, 1, 2)),
                              (('W', 'B', 'C', 'W'),
                               ('A', 'W', 'C', 'W'),
                               ('A', 'B', 'W', 'W')))

        test_stop = (0, 0, 0)
        result = sm.spin(machine, 1, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 200, line_results[0].coin_out)
        assert_true(self.assertTrue, 80, line_results[1].coin_out)
        assert_true(self.assertTrue, 30, line_results[2].coin_out)
        assert_true(self.assertTrue, 200 + 80 + 30, sm.get_total_coin_out(result))

        test_stop = (1, 1, 1)
        result = sm.spin(machine, 1, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 80, line_results[0].coin_out)
        assert_true(self.assertTrue, 30, line_results[1].coin_out)
        assert_true(self.assertTrue, 80 + 30, sm.get_total_coin_out(result))

    def test_circular_reel(self):
        machine = SlotMachine((3, 3, 3),
                              (Symbol('W', True),
                               Symbol('A', False),
                               Symbol('B', False),
                               Symbol('C', False)),
                              (Paytable('A', 3, 200),
                               Paytable('A', 2, 100),
                               Paytable('B', 3, 80),
                               Paytable('C', 3, 30)),
                              ((0, 0, 0), (1, 1, 1), (2, 2, 2)),
                              (('W', 'B', 'C'),
                               ('A', 'W', 'C'),
                               ('A', 'B', 'W')))

        test_stop = (2, 2, 2)
        result = sm.spin(machine, 1, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 3, result.len())
        assert_true(self.assertTrue, 30, line_results[0].coin_out)
        assert_true(self.assertTrue, 200, line_results[1].coin_out)
        assert_true(self.assertTrue, 80, line_results[2].coin_out)
        assert_true(self.assertTrue, 30 + 200 + 80, sm.get_total_coin_out(result))

    def test_wild_payout(self):
        machine = SlotMachine((3, 3, 3),
                              (Symbol('W', True),
                               Symbol('A', False),
                               Symbol('B', False),
                               Symbol('C', False)),
                              (Paytable('W', 3, 200),
                               Paytable('A', 3, 200),
                               Paytable('A', 2, 100),
                               Paytable('B', 3, 80),
                               Paytable('C', 3, 30)),
                              ((0, 0, 0), (1, 1, 1), (2, 2, 2)),
                              (('W', 'B', 'C'),
                               ('W', 'W', 'C'),
                               ('W', 'B', 'W')))

        test_stop = (0, 0, 0)
        result = sm.spin(machine, 1, test_stop)
        assert_true(self.assertTrue, 200, result.line_results[0].coin_out)

    def test_print_spin_log(self):
        line_results = [PaylineResult(0, 0),
                        PaylineResult(1, 1),]
        result = Result(1, 1, ['a', 'b', 'c'], line_results)

        log = create_logs(5, result)
        print(log)
        self.assertEqual('line00, 1, 1, [a, b, c], 0\nline01, 1, 1, [a, b, c], 1\n', log)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSlotMachine)
    unittest.TextTestRunner(verbosity=2).run(suite)
