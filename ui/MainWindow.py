from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from graphviz import Source

from core.FiniteAutomaton import get_dot_content
from core.Regex import Regex
from ui.layout.MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        super(MainWindow, self).setupUi(self)
        self.statusbar.showMessage("Copyright (C) 2019 张志林 MPL v2")

    @pyqtSlot()
    def on_pb_generate_fa_clicked(self):
        regex = self.le_regex.text()
        if len(regex):
            nfa = Regex.regex2nfa(regex)
            s = Source(get_dot_content(nfa.head))
            png_buf = s.pipe('png')
            nfa_map = QPixmap()
            nfa_map.loadFromData(png_buf)
            self.lbl_graph_nfa.setPixmap(nfa_map)
            self.grp_test.setEnabled(True)
        else:
            QMessageBox.critical(self, "错误", "请输入正确的正规表达式")
