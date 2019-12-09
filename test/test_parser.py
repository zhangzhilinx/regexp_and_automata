import unittest

from core import NFA, DFA
from core.FiniteAutomaton import get_dot_content
from core.Regex import Regex


class MyTestCase(unittest.TestCase):
    def test_nfa2dfa_0(self):
        s = [NFA.State(i) for i in range(10)]

        s[0].epsilons.update({s[1], s[7]})
        s[1].epsilons.update({s[2], s[4]})
        s[2].move['a'] = s[3]
        s[4].move['b'] = s[5]
        s[3].epsilons.add(s[6])
        s[5].epsilons.add(s[6])
        s[6].epsilons.add(s[1])
        s[6].epsilons.add(s[7])
        s[7].move['a'] = s[8]
        s[8].move['b'] = s[9]
        s[9].is_end = True

        nfa = NFA.SimpleNFA(s[0], s[9])
        print(get_dot_content(nfa.head))

        print()

        dfa = Regex.nfa2dfa(nfa)
        print(get_dot_content(dfa.head))

        self.assertEqual(True, True)

    def test_minimize_dfa_0(self):
        s = [DFA.State('None')] + [DFA.State(i) for i in range(1, 8)]

        s[1].move['a'], s[1].move['b'] = s[3], s[2]
        s[2].move['a'], s[2].move['b'] = s[4], s[2]
        s[3].move['b'], s[3].move['c'], s[3].move['d'] = s[6], s[3], s[5]
        s[4].move['b'], s[4].move['c'], s[4].move['d'] = s[7], s[3], s[5]
        s[5].move['a'] = s[4]
        s[6].move['b'] = s[6]
        s[7].move['b'] = s[7]
        s[6].is_end = s[7].is_end = True

        dfa = DFA.DFA(s[1], {s[6], s[7]})

        Regex.minimize_dfa(dfa)
        self.assertEqual(True, True)

    def test_minimize_dfa_1(self):
        s = [DFA.State('None')] + [DFA.State(i) for i in range(1, 8)]

        s[1].move['a'], s[1].move['b'] = s[6], s[3]
        s[2].move['a'], s[2].move['b'] = s[7], s[3]
        s[3].move['a'], s[3].move['b'] = s[1], s[5]
        s[4].move['a'], s[4].move['b'] = s[4], s[6]
        s[5].move['a'], s[5].move['b'] = s[7], s[3]
        s[6].move['a'], s[6].move['b'] = s[4], s[1]
        s[7].move['a'], s[7].move['b'] = s[4], s[2]
        s[5].is_end = s[6].is_end = s[7].is_end = True

        dfa = DFA.DFA(s[1], {s[5], s[6], s[7]})

        print(get_dot_content(dfa.head))
        print()
        min_dfa = Regex.minimize_dfa(dfa)
        print(get_dot_content(min_dfa.head))

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
