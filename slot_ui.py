import PyQt5.QtWidgets
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QLineF, QRectF, QEvent
from PyQt5.QtGui import QPainterPath, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QVBoxLayout, QGraphicsScene, QMainWindow, QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsItem, QGraphicsTextItem, QGraphicsRectItem
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QGraphicsLineItem

import slot_machine
from slot_machine import *


class MainWindow(QMainWindow):
    central_widget = None
    layout_container = None

    def __init__(self):
        super(MainWindow, self).__init__()

        self.curr_show_result_seq = 0
        self.spin_results = []

        self.machine = SlotMachine((3, 3, 3, 3, 3),
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

        self.setGeometry(0, 0, 800, 600)

        self.setFocusPolicy(Qt.NoFocus)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        
        self.machine_ui = SlotMachineWidget(self.machine)
        self.machine_ui.setFocusPolicy(Qt.NoFocus)
        self.layout.addWidget(self.machine_ui)

        self.button_group = QHBoxLayout()
        self.layout.addLayout(self.button_group)
        self.btn_spin = QPushButton('spin')
        self.btn_spin.setFocusPolicy(Qt.NoFocus)
        self.button_group.addWidget(self.btn_spin)

        self.btn_spin.clicked.connect(self.spin)

        self.spin()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        mod = QApplication.keyboardModifiers()
        if key == Qt.Key_Return:
            self.spin()
        elif key == Qt.Key_Left:
            self.show_prev_spin()
        elif key == Qt.Key_Right:
            self.show_next_spin()
        else:
            event.ignore()

    def spin(self):
        spin_result = slot_machine.spin(self.machine, 10)
        self.machine_ui.show_result(self.curr_show_result_seq, spin_result)
        
        self.curr_show_result_seq = len(self.spin_results)
        self.spin_results.append(spin_result)
        print('spin : {}, len={}'.format(self.curr_show_result_seq, len(self.spin_results)))

    def show_prev_spin(self):
        if self.curr_show_result_seq == 0:
            print('no more prev results')
            return

        self.curr_show_result_seq -= 1
        show_result = self.spin_results[self.curr_show_result_seq]
        print('show prev: {}, len={}'.format(self.curr_show_result_seq, len(self.spin_results)))
        self.machine_ui.show_result(self.curr_show_result_seq, show_result)

    def show_next_spin(self):
        if self.curr_show_result_seq == len(self.spin_results)-1:
            print('no more next results')
            return

        self.curr_show_result_seq += 1
        show_result = self.spin_results[self.curr_show_result_seq]
        print('show next: {}, len={}'.format(self.curr_show_result_seq, len(self.spin_results)))
        self.machine_ui.show_result(self.curr_show_result_seq, show_result)


class SlotMachineWidget(QGraphicsView):
    central_widget = None
    layout_container = None

    def __init__(self, machine):
        super(SlotMachineWidget, self).__init__()

        self.payline_off = 25

        self.pay_h = 20
        self.scatter_h = 20

        self.machine = machine
        self.spin_result = None

        self.setScene(QGraphicsScene())

        self.spin_no_display = QGraphicsTextItem('0')
        self.spin_no_display.setPos(0, 0)
        self.scene().addItem(self.spin_no_display)

    def show_result(self, spin_no, spin_result):
        self.spin_result = spin_result

        self.clear_all()

        self.show_symbols(self.spin_result.symbols)
        self.show_paylines(self.spin_result.line_results)
        self.show_payout(self.spin_result.line_results)
        self.show_scatter(self.spin_result.scatter_results)
        self.show_spin_no(spin_no)

    def clear_all(self):
        self.scene().clear()

    def show_spin_no(self, no):

        self.spin_no_display = QGraphicsTextItem('spin no: {}'.format(no + 1))
        self.spin_no_display.setPos(0, -20)
        self.scene().addItem(self.spin_no_display)

    def show_symbols(self, symbols):
        symbols_per_line = get_symbols_per_line(self.machine.reel_heights, symbols)

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
            win_payline = self.machine.paylines[line_result.line_id]
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

    def show_scatter(self, scatter_results):
        scatter_h = 20
        scatter_y = 50 * 3 + len(self.spin_result.line_results) * self.pay_h + 10
        
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
        super(ScatterResultItem, self).__init__(self.format_result(scatter_result))

    def format_result(self, data):
        return 'scatter: {}x{} x{}, {}'.format(data.symbol, data.count, data.coin_out, data.coin_out)


def turn_off_pyqt_loop_log():
    # to remove log on pdb debuggin
    from PyQt5.QtCore import pyqtRemoveInputHook
    from pdb import set_trace
    pyqtRemoveInputHook()


if __name__ == '__main__':
    turn_off_pyqt_loop_log()

    '''
    app = QApplication(sys.argv)
    view = TestView()
    view.show()
    sys.exit(app.exec_())
    '''

    '''
    app = QtWidgets.QApplication(sys.argv)
    w = SimpleExample()
    w.show()
    sys.exit(app.exec_())
    '''

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
