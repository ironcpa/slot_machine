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

    def assert_common_spin_results(self, coin_in, results):
        fst = results[0]
        self.assertTrue(len(results) > 0)
        self.assertTrue(fst.coin_in == coin_in)
        assert_true(self.assertTrue, fst.coin_in, coin_in)
        self.assertTrue(fst.symbols is not None)

    def test_spin(self):
        results = sm.spin(self.machine, 1)
        if len(results) == 1:
            self.assert_common_spin_results(1, results)

        results = sm.spin(self.machine, 2)
        if len(results) == 1:
            self.assert_common_spin_results(2, results)

    def test_reserve_spin(self):
        test_stop = (0, 0, 0)
        results = sm.spin(self.machine, 1, test_stop)
        assert_true(self.assertTrue, 0, len(results))

        test_stop = (0, 0, 1)
        results = sm.spin(self.machine, 1, test_stop)
        assert_true(self.assertTrue, 0, len(results))

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
        results = sm.spin(machine, 1, test_stop)
        fst = results[0]
        coin_out = fst.coin_out
        assert_true(self.assertTrue, 100, coin_out)

        results = sm.spin(machine, 2, test_stop)
        fst = results[0]
        coin_out = fst.coin_out
        assert_true(self.assertTrue, 200, coin_out)

        test_stop = (1, 1, 1)
        results = sm.spin(machine, 1, test_stop)
        fst = results[0]
        coin_out = fst.coin_out
        assert_true(self.assertTrue, 50, coin_out)

        results = sm.spin(machine, 2, test_stop)
        fst = results[0]
        coin_out = fst.coin_out
        assert_true(self.assertTrue, 100, coin_out)

        test_stop = (0, 0, 1)
        results = sm.spin(machine, 1, test_stop)
        fst = results[0]
        coin_out = fst.coin_out
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
        results = sm.spin(machine, 1, test_stop)
        assert_true(self.assertTrue, 3, len(results))
        assert_true(self.assertTrue, 100, results[0].coin_out)
        assert_true(self.assertTrue, 50, results[1].coin_out)
        assert_true(self.assertTrue, 20, results[2].coin_out)

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
        results = sm.spin(machine, 1, test_stop)
        assert_true(self.assertTrue, 2, len(results))
        assert_true(self.assertTrue, 100, results[0].coin_out)
        assert_true(self.assertTrue, 100, results[1].coin_out)

        test_stop = (3, 3, 3)
        results = sm.spin(machine, 1, test_stop)
        assert_true(self.assertTrue, 4, len(results))
        assert_true(self.assertTrue, 50, results[0].coin_out)
        assert_true(self.assertTrue, 50, results[1].coin_out)
        assert_true(self.assertTrue, 50, results[2].coin_out)
        assert_true(self.assertTrue, 50, results[3].coin_out)

        test_stop = (6, 6, 6)
        results = sm.spin(machine, 1, test_stop)
        assert_true(self.assertTrue, 5, len(results))
        assert_true(self.assertTrue, 20, results[0].coin_out)
        assert_true(self.assertTrue, 20, results[1].coin_out)
        assert_true(self.assertTrue, 20, results[2].coin_out)
        assert_true(self.assertTrue, 20, results[3].coin_out)
        assert_true(self.assertTrue, 20, results[4].coin_out)

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
        results = sm.spin(machine, 1, test_stop)
        assert_true(self.assertTrue, 200, results[0].coin_out)
        assert_true(self.assertTrue, 80, results[1].coin_out)
        assert_true(self.assertTrue, 30, results[2].coin_out)
        assert_true(self.assertTrue, 200 + 80 + 30, sm.get_total_coin_out(results))

        test_stop = (1, 1, 1)
        results = sm.spin(machine, 1, test_stop)
        assert_true(self.assertTrue, 80, results[0].coin_out)
        assert_true(self.assertTrue, 30, results[1].coin_out)
        assert_true(self.assertTrue, 80 + 30, sm.get_total_coin_out(results))

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
        results = sm.spin(machine, 1, test_stop)
        assert_true(self.assertTrue, 3, len(results))
        assert_true(self.assertTrue, 30, results[0].coin_out)
        assert_true(self.assertTrue, 200, results[1].coin_out)
        assert_true(self.assertTrue, 80, results[2].coin_out)
        assert_true(self.assertTrue, 30 + 200 + 80, sm.get_total_coin_out(results))

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
        results = sm.spin(machine, 1, test_stop)
        assert_true(self.assertTrue, 200, results[0].coin_out)
