import net_slot_machine
import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
import slot_ui
import slot_data

from slot_ui import SlotMachineWidget


class MainWindow(QMainWindow):
    central_widget = None
    layout_container = None

    def __init__(self):
        super(MainWindow, self).__init__()

        reel_heights, payline_def = net_slot_machine.get_slot_def()

        self.spin_results = []

        self.add_to_results(self.spin_results)
        self.curr_show_result_seq = self.total_spins()

        self.setGeometry(0, 0, 800, 600)

        self.setFocusPolicy(Qt.NoFocus)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.machine_ui = SlotMachineWidget(reel_heights,
                                            payline_def)
        self.machine_ui.setFocusPolicy(Qt.NoFocus)
        self.layout.addWidget(self.machine_ui)

        self.button_group = QHBoxLayout()
        self.layout.addLayout(self.button_group)
        self.btn_spin = QPushButton('spin')
        self.btn_spin.setFocusPolicy(Qt.NoFocus)
        self.button_group.addWidget(self.btn_spin)

        self.btn_spin.clicked.connect(self.spin)

        '''
        if self.total_spins() > 0:
            self.show_last_spin()
        else:
            # gen init spin
            test_stops = (5, 5, 5, 5, 5)
            self.spin(test_stops)
        '''

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return:
            if len(self.spin_results) == 0 \
               or self.curr_show_result_seq == len(self.spin_results) - 1:
                self.spin()
            else:
                self.show_next_spin()
        elif key == Qt.Key_Left:
            self.show_prev_spin()
        elif key == Qt.Key_Right:
            self.show_next_spin()
        elif key == Qt.Key_Home:
            self.show_first_spin()
        elif key == Qt.Key_End:
            self.show_last_spin()
        else:
            event.ignore()

    def total_spins(self):
        return len(self.spin_results)

    def spin(self, test_stops=None):
        """diff from local_window"""
        # spin_result = net_slot_machine.spin(10, False, test_stops)
        json_res = net_slot_machine.spin(10, False, test_stops)
        json_results = json.loads(json_res)['results']

        spin_results = []
        for r in json_results:
            spin_results.append(slot_data.to_spin_result(r))

        self.curr_show_result_seq = len(self.spin_results)
        self.add_to_results(spin_results)

        self.show_spin(self.curr_show_result_seq)
        print('spin : {}, len={}'.format(self.curr_show_result_seq,
                                         len(self.spin_results)))

    def add_to_results(self, spin_results):
        print('debug:', spin_results)

        """diff from local_windows spin_result"""
        if type(spin_results) is not list:
            spin_results = [spin_results]

        for r in spin_results:
            self.spin_results.append(r)
            for sr in r.scatter_results:
                for cr in sr.child_results:
                    self.add_to_results(cr)

    def show_spin(self, nth):
        show_result = self.spin_results[nth]
        self.machine_ui.show_result(nth, self.total_spins(), show_result)

    def show_prev_spin(self):
        if self.curr_show_result_seq == 0:
            print('no more prev results')
            return

        self.curr_show_result_seq -= 1
        self.show_spin(self.curr_show_result_seq)
        print('show prev: {}, len={}'.format(self.curr_show_result_seq,
                                             self.total_spins()))

    def show_next_spin(self):
        if self.curr_show_result_seq == len(self.spin_results)-1:
            print('no more next results')
            return

        self.curr_show_result_seq += 1
        self.show_spin(self.curr_show_result_seq)
        print('show next: {}, len={}'.format(self.curr_show_result_seq,
                                             self.total_spins()))

    def show_first_spin(self):
        self.curr_show_result_seq = 0
        self.show_spin(self.curr_show_result_seq)

    def show_last_spin(self):
        self.curr_show_result_seq = self.total_spins()-1
        self.show_spin(self.curr_show_result_seq)


if __name__ == '__main__':
    slot_ui.turn_off_pyqt_loop_log()

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
