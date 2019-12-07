import unittest

from core import FiniteAutomaton, DFA


class MyTestCase(unittest.TestCase):
    def test_dfa_match_0(self):
        # (a|b)*abb
        nodes = [DFA.State(0), DFA.State(1), DFA.State(2), DFA.State(3)]
        dfa_tab = (
            {'a': 1, 'b': 0},
            {'a': 1, 'b': 2},
            {'a': 1, 'b': 3},
            {'a': 1, 'b': 0}
        )

        for i, kv in enumerate(dfa_tab):
            for k, v in kv.items():
                nodes[i].move[k] = nodes[v]

        s0, f = nodes[0], {nodes[3]}
        print(FiniteAutomaton.get_dot_content(f, s0))

        test_cases = [
            ("bab", False),
            ("a", False),
            ("b", False),
            ("axbcbz@#a", False),
            ("aabbbabb", True),
            ("abb", True)
        ]

        for test_case in test_cases:
            self.assertEqual(DFA.dfa_match(s0, f, test_case[0]), test_case[1])

    def test_dfa_match_1(self):
        """
        test_dfa_match_0()的一个分支测试
        主要测试自动机状态标识符为字符串是否也能够正常工作
        """
        # (a|b)*abb
        nodes = [DFA.State('s0'), DFA.State('s1'),
                 DFA.State('s2'), DFA.State('s3')]
        dfa_tab = (
            {'a': 1, 'b': 0},
            {'a': 1, 'b': 2},
            {'a': 1, 'b': 3},
            {'a': 1, 'b': 0}
        )

        for i, kv in enumerate(dfa_tab):
            for k, v in kv.items():
                nodes[i].move[k] = nodes[v]

        s0, f = nodes[0], {nodes[3]}
        print(FiniteAutomaton.get_dot_content(f, s0))

        test_cases = [
            ("bab", False),
            ("a", False),
            ("b", False),
            ("axbcbz@#a", False),
            ("aabbbabb", True),
            ("abb", True)
        ]

        for test_case in test_cases:
            self.assertEqual(DFA.dfa_match(s0, f, test_case[0]), test_case[1])


if __name__ == '__main__':
    unittest.main()
