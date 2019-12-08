#!/usr/bin/env python
from core.FiniteAutomaton import find_all_reachable_states, get_dot_content
from core.parser import RegexLexer, Regex

if __name__ == '__main__':
    nfa = Regex.regex2nfa("((ab|a)(b(c?)d|c))(d*)")
    dfa = Regex.nfa2dfa(nfa)
    states, symbols = find_all_reachable_states(nfa.head)
    dot = get_dot_content(nfa.head)
    print(dot)
    pass
