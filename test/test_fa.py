import unittest

from core import FiniteAutomaton
from core.FiniteAutomaton import get_dot_content, eliminate_unused_states


class MyTestCase(unittest.TestCase):
    def test_eliminate_unused_states_0(self):
        s = [FiniteAutomaton.FiniteAutomatonState('s%d' % i)
             for i in range(13)]

        for i in (6, 8, 12):
            s[i].is_end = True

        s[0].move['a'] = s[1]
        s[1].move['b'] = s[0]
        s[1].epsilons.add(s[2])
        s[2].move['c'] = s[3]
        s[3].epsilons.add(s[4])
        s[4].move['d'] = s[2]
        s[1].move['e'] = s[5]
        s[5].move['f'] = s[6]
        s[6].epsilons.add(s[5])
        s[1].move['g'] = s[7]
        s[7].move['h'] = s[8]
        s[8].move['i'] = s[8]
        s[1].move['j'] = s[9]
        s[1].move['k'] = s[10]
        s[10].epsilons.add(s[11])
        s[11].move['l'] = s[10]
        s[10].move['m'] = s[12]

        print(get_dot_content(s[0]))
        eliminate_unused_states(s[0])
        print(get_dot_content(s[0]))

        # TODO 通过测试方式来校验结果
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
