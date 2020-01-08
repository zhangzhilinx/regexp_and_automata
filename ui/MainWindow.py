import graphviz
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QResizeEvent, QTextCursor
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel
from graphviz import Source

from core import DFA
from core.FiniteAutomaton import get_dot_content
from core.Regex import Regex
from ui.GraphView import GraphView
from ui.layout.MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        super(MainWindow, self).setupUi(self)

        self.statusbar.addPermanentWidget(
            QLabel("Copyright (C) 2019 张志林 MPL v2")
        )

        self._graph_views = [self.graphview_nfa,
                             self.graphview_dfa,
                             self.graphview_min_dfa]
        self._had_fit_in = [False] * len(self._graph_views)
        self._search_outset = 0

        for graph_view in self._graph_views:
            graph_view.set_renderer(GraphView.TYPE_OPENGL)
            graph_view.set_high_quality_antialiasing(True)

        self.statusbar.showMessage("[就绪] 已启用OpenGL绘制与抗锯齿")
        self._min_dfa = None

    @pyqtSlot(int, name='on_tabwdg_graph_currentChanged')
    def on_tabwdg_graph_current_changed(self, idx):
        if idx < len(self._had_fit_in) and not self._had_fit_in[idx]:
            graph_view = self._graph_views[idx]
            graph_view.fitInView(graph_view.sceneRect(),
                                 Qt.KeepAspectRatioByExpanding)
            self._had_fit_in[idx] = True

    @pyqtSlot(name='on_te_test_str_textChanged')
    def on_te_test_str_text_changed(self):
        self._reset_search_outset()

    @pyqtSlot()
    def on_pb_generate_fa_clicked(self):
        regex = self.le_regex.text()
        if len(regex):
            def render_graph_view_from_dot(graph_view: GraphView, fa):
                try:
                    # fa_png = Source(get_dot_content(fa.head)).pipe('png')
                    # fa_pixmap = QPixmap()
                    # fa_pixmap.loadFromData(fa_png)
                    # graph_view.load_pixmap(fa_pixmap,
                    #                        Qt.SmoothTransformation)
                    fa_svg = Source(get_dot_content(fa.head)).pipe('svg')
                    graph_view.load_svg_bytes(fa_svg)
                    graph_view.fitInView(graph_view.sceneRect(),
                                         Qt.KeepAspectRatioByExpanding)
                except graphviz.ExecutableNotFound:
                    self.statusbar.showMessage("[错误] 未安装Graphviz程序")

            nfa = Regex.regex2nfa(regex)
            render_graph_view_from_dot(self.graphview_nfa, nfa)

            dfa = Regex.nfa2dfa(nfa)
            render_graph_view_from_dot(self.graphview_dfa, dfa)

            min_dfa = Regex.minimize_dfa(dfa)
            render_graph_view_from_dot(self.graphview_min_dfa, min_dfa)

            self._min_dfa = min_dfa

            self._had_fit_in = [False] * len(self._graph_views)
            self._reset_search_outset()
            self.grp_test.setEnabled(True)
            self.statusbar.showMessage("[消息] 自动机及其图像生成完毕，"
                                       "可以鼠标用拖动调整位置或者使用滚轮缩放")
        else:
            QMessageBox.critical(self, "错误", "请输入正确的正规表达式")

    @pyqtSlot()
    def on_pb_test_match_clicked(self):
        if isinstance(self._min_dfa, DFA.DFA):
            is_succeed = self._min_dfa.match(self.te_test_str.toPlainText())
            QMessageBox.information(self, "匹配结果",
                                    "匹配成功" if is_succeed else "匹配失败")

    @pyqtSlot()
    def on_pb_test_search_clicked(self):
        if isinstance(self._min_dfa, DFA.DFA):
            text = self.te_test_str.toPlainText()
            search_pos, search_len = self._min_dfa.search(text,
                                                          self._search_outset)
            if search_pos != -1:
                self._search_outset = search_pos + search_len
                cur = self.te_test_str.textCursor()
                cur.setPosition(search_pos)
                cur.setPosition(search_pos + search_len,
                                QTextCursor.KeepAnchor)
                self.te_test_str.setTextCursor(cur)
                self.statusbar.showMessage("[成功] 向后查找时查找到新的匹配文本",
                                           2000)
            else:
                self._reset_search_outset()

                cur = self.te_test_str.textCursor()
                cur.setPosition(cur.position())
                self.te_test_str.setTextCursor(cur)

                self.statusbar \
                    .showMessage("[失败] 向后查找时找不到任何新的匹配文本，"
                                 "查找起始指针将回到文本头部以便重新查找",
                                 2000)

    def _reset_search_outset(self):
        self._search_outset = 0
