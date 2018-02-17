import PyQt5.QtWidgets
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QLineF, QRectF
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

        self.central_widget = QWidget()
        self.layout_container = QVBoxLayout()
        self.central_widget.setLayout(self.layout_container)
        self.setCentralWidget(self.central_widget)
        #self.layout_container.addWidget(GraphicsView())
        
        self.machine_ui = slot_machine_widget()
        self.layout_container.addWidget(self.machine_ui)

        self.button_group = QHBoxLayout()
        self.layout_container.addLayout(self.button_group)
        self.btn_spin = QPushButton('spin')
        self.button_group.addWidget(self.btn_spin)

        self.btn_spin.clicked.connect(self.spin)

        symbols = [['A', 'A', 'A'], ['B', 'B', 'B'], ['C', 'C', 'C']]
        self.machine_ui.show_symbols(symbols)

        payline = PaylineItem(0, [QPoint(0, 25),
                                  QPoint(25, 25),
                                  QPoint(75, 75),
                                  QPoint(125, 25),
                                  QPoint(175, 75),
                                  QPoint(225, 125),
                                  QPoint(250, 125)])
        payline.setPos(0, 0)
        self.machine_ui.scene().addItem(payline)

        ''' create paylines generated with machine setting '''
        w, h = 50, 50
        off = 25
        payline_points = []
        for payline in self.machine.paylines:
            points = []
            for reel, row in enumerate(payline):
                if reel is 0:
                    points.append(QPoint(0, row * h + off))

                points.append(QPoint(reel * w + off, row * h + off))

                if reel is len(payline) - 1:
                    points.append(QPoint((reel + 1) * w, row * h + off))

            payline_points.append(points)
        
        '''
        for line_data in payline_points:
            paylineItem = PaylineItem(line_data)
            self.machine_ui.scene().addItem(paylineItem)
            '''


    def spin(self):
        spin_result = slot_machine.spin(self.machine, 10)
        symbols = spin_result.symbols
        symbols_per_line = get_symbols_per_line(self.machine.reel_heights, symbols)
        self.machine_ui.clear_symbols()
        self.machine_ui.show_symbols(symbols_per_line)
        
        for line_result in spin_result.line_results:
            win_payline = self.machine.paylines[line_result.line_id]
            self.machine_ui.show_payline(line_result.line_id, win_payline)


class slot_machine_widget(QGraphicsView):
    central_widget = None
    layout_container = None

    def __init__(self):
        super(slot_machine_widget, self).__init__()

        self.setScene(QGraphicsScene())

    def clear_symbols(self):
       self.scene().clear()

    def show_symbols(self, symbols):
        print(symbols)
        for row, r in enumerate(symbols):
            for reel, code in enumerate(r):
                symbol = SymbolItem(code)
                x = reel * symbol.width()
                y = row * symbol.height()
                symbol.setPos(x, y)
                self.scene().addItem(symbol)

        '''show win paylines'''

    def show_payline(self, line_id, line_data):
        w, h = 50, 50
        off = 25

        points = []
        for reel, row in enumerate(line_data):
            if reel is 0:
                points.append(QPoint(0, row * h + off))

            points.append(QPoint(reel * w + off, row * h + off))

            if reel is len(line_data) - 1:
                points.append(QPoint((reel + 1) * w, row * h + off))

        line_item = PaylineItem(line_id, points)
        self.scene().addItem(line_item)


class GraphicsView(QGraphicsView):
    start = None
    end = None
    item = None
    path = None

    def __init__(self):
        super(GraphicsView, self).__init__()
        self.setScene(QGraphicsScene())

        self.path = QPainterPath()
        self.item = GraphicsPathItem()
        self.scene().addItem(self.item)

        ellipse = QGraphicsEllipseItem(0, 0, 60, 40)
        self.scene().addItem(ellipse)

        symbol = SymbolItem('SSS')
        self.scene().addItem(symbol)

    def mousePressEvent(self, evnet):
        self.start = self.mapToScene(event.pos())
        self.path.moveTo(self.start)

    def mouseMoveEvent(self, event):
        self.end = self.mapToScene(event.pos())
        self.path.lineTo(self.end)
        self.start = self.end
        self.item.setPath(self.path)

class GraphicsPathItem(QGraphicsPathItem):
    def __init__(self):
        super(GraphicsPathItem, self).__init__()
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(10)
        self.setPen(pen)


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
