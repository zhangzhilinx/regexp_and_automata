#!/usr/bin/env python
import sys

from PyQt5.QtWidgets import QApplication

from core.DFA import dfa_match
from core.FiniteAutomaton import find_all_reachable_states, get_dot_content
from core.Regex import Regex
from ui.MainWindow import MainWindow


def test():
    nfa = Regex.regex2nfa("((ab|a)(b(c?)d|c))(d*)")
    states, symbols = find_all_reachable_states(nfa.head)
    with open('./var/main_nfa.dot', 'w', encoding='utf-8') as f:
        print(get_dot_content(nfa.head), file=f)

    print()

    dfa = Regex.nfa2dfa(nfa)
    with open('./var/main_dfa.dot', 'w', encoding='utf-8') as f:
        print(get_dot_content(dfa.head), file=f)

    print()

    min_dfa = Regex.minimize_dfa(dfa)
    with open('./var/main_min_dfa.dot', 'w', encoding='utf-8') as f:
        print(get_dot_content(min_dfa.head), file=f)

    print()

    dfa_match(min_dfa.head, 'abbcddddd')
    pass


if __name__ == '__main__':
    # test()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
