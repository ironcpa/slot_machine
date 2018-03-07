import unittest
from unittest import TestCase
from slot_data import Symbol, Paytable, Payline, ScatterPaytable
import slot_machine as sm
from slot_machine import SlotMachine2, Result, PaylineResult
from slot_machine import make_payline_log, make_reel


def assert_true(func, assert_val, actual_val):
    assert_result = assert_val == actual_val
    if not assert_result:
        print('expect:', assert_val, 'actual:', actual_val)
    func(assert_result)


class TestSlotMachine(TestCase):
    def setUp(self):
        self.machine = SlotMachine2(
                           reel_heights=(1, 1, 1),
                           symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                       Symbol(1, 'A', 'a', None),
                                       Symbol(2, 'B', 'b', None),
                                       Symbol(3, 'C', 'c', None)),
                           paylines=(Payline(id=0, r0=0, r1=0, r2=0),),
                           paytables=(Paytable('A', 3, 100),
                                      Paytable('A', 2, 30),
                                      Paytable('B', 3, 50),
                                      Paytable('C', 3, 20)),
                           reels={'normal':
                                  make_reel(
                                     'normal',
                                     ('A', 'B', 'C', 'A', 'B', 'C'),
                                     ('B', 'C', 'D', 'A', 'B', 'C'),
                                     ('C', 'D', 'E', 'A', 'B', 'C'))})

    def tearDown(self):
        pass

    def test_machine(self):
        assert_true(self.assertTrue, self.machine.reel_heights[0], 1)
        assert_true(self.assertTrue, self.machine.reel_heights[1], 1)
        assert_true(self.assertTrue, self.machine.reel_heights[2], 1)

    def assert_common_spin_results(self, result):
        self.assertTrue(len(result.line_results) > 0)
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
        result = sm.spin(self.machine, 1, False, test_stop)
        assert_true(self.assertTrue, 0, result.len())

        test_stop = (0, 0, 1)
        result = sm.spin(self.machine, 1, False, test_stop)
        assert_true(self.assertTrue, 0, result.len())

    def test_coin_out(self):
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None)),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),),
                               paytables=(Paytable('A', 3, 100),
                                          Paytable('A', 2, 30),
                                          Paytable('B', 3, 50),
                                          Paytable('C', 3, 20)),
                               reels={'normal': make_reel('normal',
                                                          ('A', 'B', 'C'),
                                                          ('A', 'B', 'C'),
                                                          ('A', 'B', 'C'))})
        # pay table
        # A x 3 : 100
        # A x 2 : 30
        # B x 3 : 50
        # C x 3 : 20

        test_stop = (0, 0, 0)
        result = sm.spin(machine, 1, False, test_stop)
        coin_out = result.fst().coin_out
        assert_true(self.assertTrue, 100, coin_out)

        result = sm.spin(machine, 2, False, test_stop)
        coin_out = result.fst().coin_out
        assert_true(self.assertTrue, 200, coin_out)

        test_stop = (1, 1, 1)
        result = sm.spin(machine, 1, False, test_stop)
        coin_out = result.fst().coin_out
        assert_true(self.assertTrue, 50, coin_out)

        result = sm.spin(machine, 2, False, test_stop)
        coin_out = result.fst().coin_out
        assert_true(self.assertTrue, 100, coin_out)

        test_stop = (0, 0, 1)
        result = sm.spin(machine, 1, False, test_stop)
        coin_out = result.fst().coin_out
        assert_true(self.assertTrue, 30, coin_out)

    def test_multi_row_slot(self):
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None)),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                         Payline(id=1, r0=1, r1=1, r2=1),
                                         Payline(id=2, r0=2, r1=2, r2=2),
                                         Payline(id=3, r0=0, r1=1, r2=2)),
                               paytables=(Paytable('A', 3, 100),
                                          Paytable('A', 2, 30),
                                          Paytable('B', 3, 50),
                                          Paytable('C', 3, 20)),
                               reels={'normal': make_reel('normal',
                                                          ('A', 'B', 'C'),
                                                          ('A', 'B', 'C'),
                                                          ('A', 'B', 'C'))})
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
        result = sm.spin(machine, 1*4, False, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 3, len(line_results))
        assert_true(self.assertTrue, 100, line_results[0].coin_out)
        assert_true(self.assertTrue, 50, line_results[1].coin_out)
        assert_true(self.assertTrue, 20, line_results[2].coin_out)

        # more complex paylines
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None)),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                         Payline(id=1, r0=1, r1=1, r2=1),
                                         Payline(id=2, r0=2, r1=2, r2=2),
                                         Payline(id=3, r0=0, r1=1, r2=2),
                                         Payline(id=3, r0=2, r1=1, r2=0)),
                               paytables=(Paytable('A', 3, 100),
                                          Paytable('A', 2, 30),
                                          Paytable('B', 3, 50),
                                          Paytable('C', 3, 20)),
                               reels={'normal': make_reel(
                                                'normal',
                                                ('A', 'B', 'A', 'B', 'C',
                                                 'B', 'C', 'C', 'C'),
                                                ('C', 'A', 'C', 'B', 'B',
                                                 'B', 'C', 'C', 'C'),
                                                ('A', 'B', 'A', 'B', 'C',
                                                 'B', 'C', 'C', 'C'))})

        test_stop = (0, 0, 0)
        result = sm.spin(machine, 1*5, False, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 2, len(line_results))
        assert_true(self.assertTrue, 100, line_results[0].coin_out)
        assert_true(self.assertTrue, 100, line_results[1].coin_out)

        test_stop = (3, 3, 3)
        result = sm.spin(machine, 1*5, False, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 4, len(line_results))
        assert_true(self.assertTrue, 50, line_results[0].coin_out)
        assert_true(self.assertTrue, 50, line_results[1].coin_out)
        assert_true(self.assertTrue, 50, line_results[2].coin_out)
        assert_true(self.assertTrue, 50, line_results[3].coin_out)

        test_stop = (6, 6, 6)
        result = sm.spin(machine, 1*5, False, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 5, len(line_results))
        assert_true(self.assertTrue, 20, line_results[0].coin_out)
        assert_true(self.assertTrue, 20, line_results[1].coin_out)
        assert_true(self.assertTrue, 20, line_results[2].coin_out)
        assert_true(self.assertTrue, 20, line_results[3].coin_out)
        assert_true(self.assertTrue, 20, line_results[4].coin_out)

    def test_total_payout(self):
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None)),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                         Payline(id=1, r0=1, r1=1, r2=1),
                                         Payline(id=2, r0=2, r1=2, r2=2),
                                         Payline(id=3, r0=0, r1=1, r2=2)),
                               paytables=(Paytable('A', 3, 100),
                                          Paytable('A', 2, 30),
                                          Paytable('B', 3, 50),
                                          Paytable('C', 3, 20)),
                               reels={'normal': make_reel('normal',
                                                          ('A', 'B', 'C'),
                                                          ('A', 'B', 'C'),
                                                          ('A', 'B', 'C'))})

        test_stop = (0, 0, 0)
        results = sm.spin(machine, 1*4, False, test_stop)
        assert_true(self.assertTrue, 170, sm.get_total_coin_out(results))

    def test_paytable(self):
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None)),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                         Payline(id=1, r0=1, r1=1, r2=1),
                                         Payline(id=2, r0=2, r1=2, r2=2),
                                         Payline(id=3, r0=0, r1=1, r2=2)),
                               paytables=(Paytable('A', 3, 200),
                                          Paytable('A', 2, 100),
                                          Paytable('B', 3, 80),
                                          Paytable('C', 3, 30)),
                               reels={'normal': make_reel('normal',
                                                          ('A', 'B', 'C'),
                                                          ('A', 'B', 'C'),
                                                          ('A', 'B', 'C'))})

        test_stop = (0, 0, 0)
        results = sm.spin(machine, 1*4, False, test_stop)
        assert_true(self.assertTrue,
                    200 + 80 + 30,
                    sm.get_total_coin_out(results))

    def test_wild(self):
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None)),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                         Payline(id=1, r0=1, r1=1, r2=1),
                                         Payline(id=2, r0=2, r1=2, r2=2),
                                         Payline(id=3, r0=0, r1=1, r2=2)),
                               paytables=(Paytable('A', 3, 200),
                                          Paytable('A', 2, 100),
                                          Paytable('B', 3, 80),
                                          Paytable('C', 3, 30)),
                               reels={'normal': make_reel(
                                                'normal',
                                                ('W', 'B', 'C', 'W'),
                                                ('A', 'W', 'C', 'W'),
                                                ('A', 'B', 'W', 'W'))})

        test_stop = (0, 0, 0)
        result = sm.spin(machine, 1*4, False, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 200, line_results[0].coin_out)
        assert_true(self.assertTrue, 80, line_results[1].coin_out)
        assert_true(self.assertTrue, 30, line_results[2].coin_out)
        assert_true(self.assertTrue,
                    200 + 80 + 30,
                    sm.get_total_coin_out(result))

        test_stop = (1, 1, 1)
        result = sm.spin(machine, 1*4, False, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 80, line_results[0].coin_out)
        assert_true(self.assertTrue, 30, line_results[1].coin_out)
        assert_true(self.assertTrue, 80 + 30, sm.get_total_coin_out(result))

    def test_circular_reel(self):
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None)),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                         Payline(id=1, r0=1, r1=1, r2=1),
                                         Payline(id=2, r0=2, r1=2, r2=2),),
                               paytables=(Paytable('A', 3, 200),
                                          Paytable('A', 2, 100),
                                          Paytable('B', 3, 80),
                                          Paytable('C', 3, 30)),
                               reels={'normal': make_reel('normal',
                                                          ('W', 'B', 'C'),
                                                          ('A', 'W', 'C'),
                                                          ('A', 'B', 'W'))})

        test_stop = (2, 2, 2)
        result = sm.spin(machine, 1*3, False, test_stop)
        line_results = result.line_results
        assert_true(self.assertTrue, 3, result.len())
        assert_true(self.assertTrue, 30, line_results[0].coin_out)
        assert_true(self.assertTrue, 200, line_results[1].coin_out)
        assert_true(self.assertTrue, 80, line_results[2].coin_out)
        assert_true(self.assertTrue,
                    30 + 200 + 80,
                    sm.get_total_coin_out(result))

    def test_wild_payout(self):
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None)),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                         Payline(id=1, r0=1, r1=1, r2=1),
                                         Payline(id=2, r0=2, r1=2, r2=2),),
                               paytables=(Paytable('W', 3, 200),
                                          Paytable('A', 3, 200),
                                          Paytable('A', 2, 100),
                                          Paytable('B', 3, 80),
                                          Paytable('C', 3, 30)),
                               reels={'normal': make_reel('normal',
                                                          ('W', 'B', 'C'),
                                                          ('W', 'W', 'C'),
                                                          ('W', 'B', 'W'))})

        test_stop = (0, 0, 0)
        result = sm.spin(machine, 1*3, False, test_stop)
        assert_true(self.assertTrue, 200, result.line_results[0].coin_out)

    def test_print_spin_log(self):
        line_results = [PaylineResult(0, 0),
                        PaylineResult(1, 1)]
        result = Result('normal', 1, 1, 1, ['a', 'b', 'c'], line_results)

        reel_heights = (1, 1, 1)
        log = make_payline_log(0, reel_heights, result)
        self.assertEqual('line00, 1, 0\nline01, 1, 1\n', log)

    def test_scatter_simple(self):
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None),
                                           Symbol(4, 'S', 's', 'scatter'),),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                         Payline(id=1, r0=1, r1=1, r2=1),
                                         Payline(id=2, r0=2, r1=2, r2=2),),
                               paytables=(Paytable('W', 3, 200),
                                          Paytable('A', 3, 200),
                                          Paytable('A', 2, 100),
                                          Paytable('B', 3, 80),
                                          Paytable('C', 3, 30),),
                               scatter_paytables=(
                                   ScatterPaytable('S', 3, 'payout', 100),),
                               reels={'normal': make_reel(
                                                'normal',
                                                ('S', 'B', 'C', 'A'),
                                                ('S', 'A', 'C', 'B'),
                                                ('S', 'B', 'A', 'C')),
                                      'freespin': make_reel(
                                                'free',
                                                ('S', 'B', 'C', 'A'),
                                                ('S', 'A', 'C', 'B'),
                                                ('S', 'B', 'A', 'C'))})
        test_stop = (0, 0, 0)
        result = sm.spin(machine, 1, False, test_stop)
        self.assertEqual(len(result.scatter_results), 1)
        scatter_result = result.scatter_results[0]
        self.assertEqual(scatter_result.symbol, 'S')
        self.assertEqual(scatter_result.count, 3)
        self.assertEqual(scatter_result.coin_out, 100)

        # no scatter result
        test_stop = (1, 0, 0)
        result = sm.spin(machine, 1, False, test_stop)
        self.assertEqual(len(result.scatter_results), 0)

    def test_scatter_freespin(self):
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None),
                                           Symbol(4, 'S', 's', 'scatter')),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                         Payline(id=1, r0=1, r1=1, r2=1),
                                         Payline(id=2, r0=2, r1=2, r2=2),),
                               paytables=(Paytable('W', 3, 200),
                                          Paytable('A', 3, 200),
                                          Paytable('A', 2, 100),
                                          Paytable('B', 3, 80),
                                          Paytable('C', 3, 30)),
                               scatter_paytables=(
                                   ScatterPaytable('S', 3, 'freespin', 1),
                               ),
                               reels={'normal': make_reel(
                                                'normal',
                                                ('S', 'B', 'C', 'A'),
                                                ('S', 'A', 'C', 'B'),
                                                ('S', 'B', 'A', 'C')),
                                      'freespin': make_reel(
                                                  'free',
                                                  ('A',),
                                                  ('A',),
                                                  ('A',),)})
        test_stop = (0, 0, 0)
        result = sm.spin(machine, 1*3, False, test_stop)

        scatter_result = result.scatter_results[0]

        self.assertEqual(len(result.scatter_results), 1)
        scatter_result = result.scatter_results[0]
        self.assertEqual(scatter_result.symbol, 'S')
        self.assertEqual(scatter_result.count, 3)
        self.assertEqual(scatter_result.coin_out, 0)
        self.assertEqual(scatter_result.freespins, 1)
        self.assertEqual(len(scatter_result.child_results), 1)
        freespin_result = scatter_result.child_results[0]
        self.assertEqual(len(freespin_result.line_results), 3)
        self.assertEqual(freespin_result.symbols,
                         ('A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'))
        for i, r in enumerate(freespin_result.line_results):
            self.assertEqual(r.coin_out, 200)

    def test_freespin_stop_reserve(self):
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None),
                                           Symbol(4, 'S', 's', 'scatter')),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                         Payline(id=1, r0=1, r1=1, r2=1),
                                         Payline(id=2, r0=2, r1=2, r2=2),),
                               scatter_paytables=(
                                   ScatterPaytable('S', 3, 'freespin', 2),
                               ),
                               paytables=(Paytable('W', 3, 200),
                                          Paytable('A', 3, 200),
                                          Paytable('A', 2, 100),
                                          Paytable('B', 3, 80),
                                          Paytable('C', 3, 30)),
                               reels={'normal': make_reel(
                                                'normal',
                                                ('S', 'B', 'C', 'A'),
                                                ('S', 'A', 'C', 'B'),
                                                ('S', 'B', 'A', 'C')),
                                      'freespin': make_reel(
                                                'freespin',
                                                ('A', 'B', 'C'),
                                                ('A', 'B', 'C'),
                                                ('A', 'B', 'C'),)})
        test_stops = [(0, 0, 0), (0, 0, 0), (1, 1, 1)]
        result = sm.spin(machine, 1*3, False, test_stops)
        scatter_result = result.scatter_results[0]

        self.assertEqual(len(scatter_result.child_results), 2)

        freespin_result = scatter_result.child_results[0]
        self.assertEqual(freespin_result.stop_pos, (0, 0, 0))
        self.assertEqual(freespin_result.symbols,
                         ('A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'))
        freespin_line_results = freespin_result.line_results
        self.assertEqual(freespin_line_results[0].coin_out, 200)
        self.assertEqual(freespin_line_results[1].coin_out, 80)
        self.assertEqual(freespin_line_results[2].coin_out, 30)

        freespin_result = scatter_result.child_results[1]
        self.assertEqual(freespin_result.stop_pos, (1, 1, 1))
        self.assertEqual(freespin_result.symbols,
                         ('B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A'))
        freespin_line_results = freespin_result.line_results
        self.assertEqual(freespin_line_results[0].coin_out, 80)
        self.assertEqual(freespin_line_results[1].coin_out, 30)
        self.assertEqual(freespin_line_results[2].coin_out, 200)

    def test_freespin_retrigger(self):
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None),
                                           Symbol(4, 'S', 's', 'scatter'),),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                         Payline(id=1, r0=1, r1=1, r2=1),
                                         Payline(id=2, r0=2, r1=2, r2=2),),
                               paytables=(Paytable('W', 3, 200),
                                          Paytable('A', 3, 200),
                                          Paytable('A', 2, 100),
                                          Paytable('B', 3, 80),
                                          Paytable('C', 3, 30)),
                               scatter_paytables=(
                                   ScatterPaytable('S', 3, 'freespin', 2),
                               ),
                               reels={'normal': make_reel(
                                                 'normal',
                                                 ('S', 'B', 'C', 'A'),
                                                 ('S', 'A', 'C', 'B'),
                                                 ('S', 'B', 'A', 'C')),
                                      'freespin': make_reel(
                                                 'freespin',
                                                 ('S', 'A', 'B', 'C'),
                                                 ('S', 'A', 'B', 'C'),
                                                 ('S', 'A', 'B', 'C'),)})

        test_stops = [(0, 0, 0), (1, 1, 1), (0, 0, 0), (1, 1, 1)]
        result = sm.spin(machine, 1*3, False, test_stops)
        self.assertEqual(result.stop_pos, (0, 0, 0))
        self.assertEqual(result.symbols,
                         ('S', 'B', 'C', 'S', 'A', 'C', 'S', 'B', 'A'))

        scatter_result = result.scatter_results[0]

        freespin_result = scatter_result.child_results[0]
        self.assertEqual(freespin_result.stop_pos, (1, 1, 1))
        self.assertEqual(freespin_result.symbols,
                         ('A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'))
        freespin_line_results = freespin_result.line_results
        self.assertEqual(freespin_line_results[0].coin_out, 200)
        self.assertEqual(freespin_line_results[1].coin_out, 80)
        self.assertEqual(freespin_line_results[2].coin_out, 30)

        freespin_result = scatter_result.child_results[1]
        self.assertEqual(freespin_result.stop_pos, (0, 0, 0))
        self.assertEqual(freespin_result.symbols,
                         ('S', 'A', 'B', 'S', 'A', 'B', 'S', 'A', 'B'))
        freespin_line_results = freespin_result.line_results
        self.assertEqual(len(freespin_line_results), 2)
        self.assertEqual(freespin_line_results[0].coin_out, 200)
        self.assertEqual(freespin_line_results[1].coin_out, 80)
        scatter_result = freespin_result.scatter_results[0]

        freespin_result = scatter_result.child_results[0]
        self.assertEqual(freespin_result.symbols,
                         ('A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'))
        freespin_line_results = freespin_result.line_results
        self.assertEqual(len(freespin_line_results), 3)
        self.assertEqual(freespin_line_results[0].coin_out, 200)
        self.assertEqual(freespin_line_results[1].coin_out, 80)
        self.assertEqual(freespin_line_results[2].coin_out, 30)

    def test_freespin_retrigger2(self):
        machine = SlotMachine2(reel_heights=(3, 3, 3),
                               symboldefs=(Symbol(0, 'W', 'wild', 'wild'),
                                           Symbol(1, 'A', 'a', None),
                                           Symbol(2, 'B', 'b', None),
                                           Symbol(3, 'C', 'c', None)),
                               paylines=(Payline(id=0, r0=0, r1=0, r2=0),
                                         Payline(id=1, r0=1, r1=1, r2=1),
                                         Payline(id=2, r0=2, r1=2, r2=2),),
                               paytables=(Paytable('A', 3, 200),
                                          Paytable('A', 2, 100),
                                          Paytable('B', 3, 80),
                                          Paytable('C', 3, 30)),
                               scatter_paytables=(
                                   ScatterPaytable('S', 3, 'freespin', 3),
                               ),
                               reels={'normal': make_reel(
                                                 'normal',
                                                 ('S', 'B', 'C', 'A'),
                                                 ('S', 'A', 'C', 'B'),
                                                 ('S', 'B', 'A', 'C')),
                                      'freespin': make_reel(
                                                 'freespin',
                                                 ('S', 'A', 'B', 'C'),
                                                 ('S', 'A', 'B', 'C'),
                                                 ('S', 'A', 'B', 'C'))})

        test_stops = [(0, 0, 0),
                      (0, 0, 0),
                      (1, 1, 1),
                      (1, 1, 1),
                      (1, 1, 1),
                      (1, 1, 1),
                      (1, 1, 1),
                      (1, 1, 1)]
        """
        test scinario ====================================
        N0(Sx3) ->
                  F0(Sx3)                     -> F1 -> F2
                         -> F00 -> F01 -> F02
        ==================================================
        """
        # N0
        result = sm.spin(machine, 1*3, False, test_stops)
        self.assertEqual(result.stop_pos, (0, 0, 0))
        self.assertEqual(result.symbols,
                         ('S', 'B', 'C', 'S', 'A', 'C', 'S', 'B', 'A'))

        scatter_result = result.scatter_results[0]
        self.assertEqual(len(scatter_result.child_results), 3)

        # F0
        freespin_result = scatter_result.child_results[0]
        self.assertEqual(freespin_result.stop_pos, (0, 0, 0))
        self.assertEqual(freespin_result.symbols,
                         ('S', 'A', 'B', 'S', 'A', 'B', 'S', 'A', 'B'))
        freespin_line_results = freespin_result.line_results
        self.assertEqual(len(freespin_line_results), 2)
        self.assertEqual(freespin_line_results[0].coin_out, 200)
        self.assertEqual(freespin_line_results[1].coin_out, 80)

        inner_scatter_result = freespin_result.scatter_results[0]
        self.assertEqual(len(inner_scatter_result.child_results), 3)

        # F00
        freespin_result = inner_scatter_result.child_results[0]
        self.assertEqual(freespin_result.stop_pos, (1, 1, 1))
        self.assertEqual(freespin_result.symbols,
                         ('A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'))
        freespin_line_results = freespin_result.line_results
        self.assertEqual(len(freespin_line_results), 3)
        self.assertEqual(freespin_line_results[0].coin_out, 200)
        self.assertEqual(freespin_line_results[1].coin_out, 80)
        self.assertEqual(freespin_line_results[2].coin_out, 30)

        # F01
        freespin_result = inner_scatter_result.child_results[1]
        self.assertEqual(freespin_result.stop_pos, (1, 1, 1))
        self.assertEqual(freespin_result.symbols,
                         ('A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'))
        freespin_line_results = freespin_result.line_results
        self.assertEqual(len(freespin_line_results), 3)
        self.assertEqual(freespin_line_results[0].coin_out, 200)
        self.assertEqual(freespin_line_results[1].coin_out, 80)
        self.assertEqual(freespin_line_results[2].coin_out, 30)

        # F02
        freespin_result = inner_scatter_result.child_results[2]
        self.assertEqual(freespin_result.stop_pos, (1, 1, 1))
        self.assertEqual(freespin_result.symbols,
                         ('A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'))
        freespin_line_results = freespin_result.line_results
        self.assertEqual(len(freespin_line_results), 3)
        self.assertEqual(freespin_line_results[0].coin_out, 200)
        self.assertEqual(freespin_line_results[1].coin_out, 80)
        self.assertEqual(freespin_line_results[2].coin_out, 30)

        # F1
        freespin_result = scatter_result.child_results[1]
        self.assertEqual(freespin_result.symbols,
                         ('A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'))
        freespin_line_results = freespin_result.line_results
        self.assertEqual(len(freespin_line_results), 3)
        self.assertEqual(freespin_line_results[0].coin_out, 200)
        self.assertEqual(freespin_line_results[1].coin_out, 80)
        self.assertEqual(freespin_line_results[2].coin_out, 30)

        # F2
        freespin_result = scatter_result.child_results[2]
        self.assertEqual(freespin_result.symbols,
                         ('A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'))
        freespin_line_results = freespin_result.line_results
        self.assertEqual(len(freespin_line_results), 3)
        self.assertEqual(freespin_line_results[0].coin_out, 200)
        self.assertEqual(freespin_line_results[1].coin_out, 80)
        self.assertEqual(freespin_line_results[2].coin_out, 30)


"""
todo: collect n log summary data

00 spin: coin_in=10
    stop=(0, 2, 6, 5, 4)
    symbols=
        ['W', 'B', 'S', 'E', 'D']
        ['A', 'C', 'W', 'W', 'E']
        ['B', 'D', 'A', 'A', 'S']
    win lines =======
        line00, 10, 100
        line03, 10, 200
        line05, 10, 100
        line07, 10, 400
    win scatters ====
        'S'x3
        child results
            00 spin: coin_in=10
            stop=(0, 0, 0, 0, 0)
            symbols=
                ['W', 'B', 'S', 'E', 'D']
                ['A', 'C', 'W', 'W', 'E']
                ['B', 'D', 'A', 'A', 'S']
            win lines =======
                line00, 10, 100
                line03, 10, 200
                line05, 10, 100
                line07, 10, 400
            win scatters ====
                'S'x3
"""

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSlotMachine)
    unittest.TextTestRunner(verbosity=2).run(suite)
