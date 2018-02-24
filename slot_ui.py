from PyQt5.QtCore import QPoint, QLineF, QRectF
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtWidgets import QGraphicsLineItem

import slot_data


class SlotMachineWidget(QGraphicsView):
    central_widget = None
    layout_container = None

    def __init__(self, reel_heights, paylines):
        super(SlotMachineWidget, self).__init__()

        self.payline_off = 25

        self.pay_h = 20
        self.scatter_h = 20

        self.reel_heights = reel_heights
        self.paylines = paylines

        self.setScene(QGraphicsScene())

    '''
    def __init__(self, machine):
        super(SlotMachineWidget, self).__init__()

        self.payline_off = 25

        self.pay_h = 20
        self.scatter_h = 20

        self.machine = machine

        self.setScene(QGraphicsScene())
    '''

    def show_result(self, spin_no, total_spins, spin_result):
        self.clear_all()

        self.show_symbols(spin_result.symbols)
        self.show_paylines(spin_result.line_results)
        self.show_payout(spin_result.line_results)
        self.show_scatter(spin_result.scatter_results,
                          len(spin_result.line_results))
        self.show_spin_no(spin_no, total_spins, spin_result.spin_type)

    def clear_all(self):
        self.scene().clear()

    def show_spin_no(self, no, total_spins, spin_type):
        str_spin_no = 'spin no: {} / {} {}'.format(no + 1,
                                                   total_spins, spin_type)
        self.spin_no_display = QGraphicsTextItem(str_spin_no)
        self.spin_no_display.setPos(0, -20)
        self.scene().addItem(self.spin_no_display)

    def show_symbols(self, symbols):
        symbols_per_line = slot_data.get_symbols_per_line(self.reel_heights,
                                                          symbols)

        print(symbols_per_line)
        for row, r in enumerate(symbols_per_line):
            for reel, code in enumerate(r):
                symbol = SymbolItem(code)
                x = reel * symbol.width()
                y = row * symbol.height()
                symbol.setPos(x, y)
                self.scene().addItem(symbol)

    def show_paylines(self, line_results):
        for line_result in line_results:
            win_payline = self.paylines[line_result.line_id]
            self.show_payline(line_result.line_id, win_payline)

    def show_payline(self, line_id, payline_def):
        w, h = 50, 50
        off = self.payline_off

        points = []
        for reel, row in enumerate(payline_def):
            if reel is 0:
                points.append(QPoint(0, row * h + off))

            points.append(QPoint(reel * w + off, row * h + off))

            if reel is len(payline_def) - 1:
                points.append(QPoint((reel + 1) * w, row * h + off))

        line_item = PaylineItem(line_id, points)
        self.scene().addItem(line_item)

    def show_payout(self, line_wins):
        pay_y = 50 * 3 + 10

        for i, win_data in enumerate(line_wins):
            lr = LineResultItem(win_data)
            self.scene().addItem(lr)
            lr.setPos(0, pay_y + i * self.pay_h)

    def show_scatter(self, scatter_results, line_win_count):
        scatter_h = 20
        scatter_y = 50 * 3 + line_win_count * self.pay_h + 10

        for i, win_data in enumerate(scatter_results):
            sr = ScatterResultItem(win_data)
            self.scene().addItem(sr)
            sr.setPos(0, scatter_y + i * scatter_h)


class SymbolItem(QGraphicsRectItem):
    def __init__(self, code):
        super(SymbolItem, self).__init__()

        self.setRect(0, 0, 50, 50)

        text_item = QGraphicsTextItem(code)
        text_item.setParentItem(self)

        # self.setBrush(QBrush(QColor('#f2a2e7')))
        self.select_color(code)

    def select_color(self, code):
        if code is 'S':
            self.setBrush(QBrush(QColor('#efb3e7')))

    def width(self):
        return self.boundingRect().width()

    def height(self):
        return self.boundingRect().height()


class PaylineItem(QGraphicsItem):
    def __init__(self, line_id, points):
        super(PaylineItem, self).__init__()

        self.line_id = line_id
        self.points = points

        self.bounding_rect = QRectF(0, 0, 50*5, 50*3)

        self.set_lines()

    def boundingRect(self):
        return self.bounding_rect

    def paint(self, painter, option, widget=None):
        pass

    def set_lines(self):
        for i, p in enumerate(self.points):
            if i is len(self.points) - 1:
                break

            np = self.points[i+1]

            line = QLineF(p, np)
            item = QGraphicsLineItem(line)
            item.setParentItem(self)

        if len(self.points) > 0:
            marker = QGraphicsTextItem(str(self.line_id))
            line_start_y = self.points[0].y()
            marker.setPos(-25, line_start_y - 25 / 2.0)
            marker.setParentItem(self)


class LineResultItem(QGraphicsTextItem):
    def __init__(self, line_result):
        super(LineResultItem, self).__init__(self.format_result(line_result))

    def format_result(self, data):
        return 'line[{}]: x{}'.format(data.line_id, data.coin_out)


class ScatterResultItem(QGraphicsTextItem):
    def __init__(self, scatter_result):
        super(ScatterResultItem,
              self).__init__(self.format_result(scatter_result))

    def format_result(self, data):
        return 'scatter: {}x{} x{}, free={}'.format(data.symbol,
                                                    data.count,
                                                    data.coin_out,
                                                    data.freespins)


def turn_off_pyqt_loop_log():
    # to remove log on pdb debuggin
    from PyQt5.QtCore import pyqtRemoveInputHook
    # from pdb import set_trace
    pyqtRemoveInputHook()
