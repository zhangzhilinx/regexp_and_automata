import unittest

from core import NFA
from core.FiniteAutomaton import get_dot_content
from core.parser import Regex


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
        dfa = Regex.nfa2dfa(nfa)

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
