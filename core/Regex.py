from collections import deque

from core import NFA, DFA
from core.FiniteAutomaton import FiniteAutomatonState
from core.FiniteAutomaton import find_all_reachable_states, EPSILON


class TypedToken:
    TYPE_CHR = 'CHAR'
    # TYPE_DOT = 'DOT'
    TYPE_LPA, TYPE_RPA = 'LPA', 'RPA'
    TYPE_ALT, TYPE_CAT = 'ALTER', 'CONCAT'
    TYPE_QUES, TYPE_PLUS, TYPE_STAR = 'QUES', 'PLUS', 'STAR'
    PROP_CAT = '\x1F'

    OPR_MAPPER = {
        # '.': TYPE_DOT,
        '(': TYPE_LPA, ')': TYPE_RPA,
        '|': TYPE_ALT, PROP_CAT: TYPE_CAT,
        '?': TYPE_QUES, '+': TYPE_PLUS, '*': TYPE_STAR,
    }

    def __init__(self, _type, _prop):
        self._type = _type
        self._prop = _prop
        pass

    @property
    def type(self):
        return self._type

    @property
    def prop(self):
        return self._prop

    def __repr__(self):
        return "(%s, '%s')" % (self._type, self._prop)


class RegexLexer:
    @staticmethod
    def get_tokens(pattern):
        tokens = []
        for c in pattern:
            tokens.append(TypedToken(
                TypedToken.OPR_MAPPER.get(c, TypedToken.TYPE_CHR),
                c
            ))
        return tokens


class RegexParser:
    """
    简单的Regex语法的解析器，生成正规表达式的后缀表达式

    解析器使用固定写法的递归下降法实现，文法如下：
    regex'   = regex $
    regex    = term [|] regex
             | term
    term     = factor term
             | factor
    factor   = unit [*]
             | unit [?]
             | unit [+]
             | unit
    unit     = ( regex )
             | char
    """

    class PostBuilder:
        class ParseError(Exception):
            def __init__(self, msg):
                self.message = msg

        def __init__(self, tokens):
            self.tokens = deque(tokens)
            self.__post = []

        def __unit(self):
            first_type = self.tokens[0].type
            if first_type == TypedToken.TYPE_LPA:
                self.tokens.popleft()
                self.__regex()
                if self.tokens.popleft().type != TypedToken.TYPE_RPA:
                    raise self.ParseError("语法错误，期望遇到右括号")
            elif first_type == TypedToken.TYPE_CHR:
                self.__post.append(self.tokens.popleft())
            else:
                raise self.ParseError("语法错误，期望遇到左括号或者字符")

        def __factor(self):
            self.__unit()
            if len(self.tokens) \
                    and self.tokens[0].type in (TypedToken.TYPE_QUES,
                                                TypedToken.TYPE_PLUS,
                                                TypedToken.TYPE_STAR):
                self.__post.append(self.tokens.popleft())

        def __term(self):
            self.__factor()
            if len(self.tokens) \
                    and self.tokens[0].type not in (TypedToken.TYPE_ALT,
                                                    TypedToken.TYPE_RPA):
                self.__term()
                self.__post.append(TypedToken(TypedToken.TYPE_CAT,
                                              TypedToken.PROP_CAT))

        def __regex(self):
            # if not len(self.tokens) \
            #         or self.tokens[0].type == TypedToken.TYPE_RPA:
            #     return
            self.__term()
            if len(self.tokens) and self.tokens[0].type == TypedToken.TYPE_ALT:
                opr = self.tokens.popleft()
                self.__regex()
                self.__post.append(opr)

        def get_post(self):
            self.__regex()
            return self.__post

    @classmethod
    def parse2post(cls, tokens):
        return cls.PostBuilder(tokens).get_post()


class Regex:
    class RegexPost2NFA:
        """
        [线程不安全]
        """

        def __init__(self):
            self.__count = 0
            self.nfa_stk = []

        def allocate_nfa_state(self):
            state = NFA.State(self.__count)
            self.__count += 1
            return state

        def process_chr(self, token: TypedToken):
            s0 = self.allocate_nfa_state()
            s1 = self.allocate_nfa_state()
            s0.move[token.prop] = s1
            self.nfa_stk.append(NFA.SimpleNFA(s0, s1))

        def process_alt(self, *args):
            n1 = self.nfa_stk.pop()
            n0 = self.nfa_stk.pop()
            s0 = self.allocate_nfa_state()
            s0.epsilons.update({n0.head, n1.head})
            s1 = self.allocate_nfa_state()
            n0.tail.is_end = n1.tail.is_end = False
            n0.tail.epsilons.add(s1)
            n1.tail.epsilons.add(s1)
            self.nfa_stk.append(NFA.SimpleNFA(s0, s1))

        def process_cat(self, *args):
            n1 = self.nfa_stk.pop()
            n0 = self.nfa_stk.pop()
            n0.tail.is_end = False
            n0.tail.epsilons.add(n1.head)
            self.nfa_stk.append(NFA.SimpleNFA(n0.head, n1.tail))

        def process_ques(self, *args):
            nfa = self.nfa_stk.pop()
            nfa.head.epsilons.add(nfa.tail)
            self.nfa_stk.append(nfa)

        def process_plus(self, *args):
            nfa = self.nfa_stk.pop()
            s0, s1 = self.allocate_nfa_state(), self.allocate_nfa_state()
            s0.epsilons.add(nfa.head)
            nfa.tail.is_end = False
            nfa.tail.epsilons.update({s1, nfa.head})
            self.nfa_stk.append(NFA.SimpleNFA(s0, s1))

        def process_star(self, *args):
            nfa = self.nfa_stk.pop()
            s0, s1 = self.allocate_nfa_state(), self.allocate_nfa_state()
            s0.epsilons.update({nfa.head, s1})  # 与+的不同之处
            nfa.tail.is_end = False
            nfa.tail.epsilons.update({s1, nfa.head})
            self.nfa_stk.append(NFA.SimpleNFA(s0, s1))

        def post2nfa(self, post):
            self.__count = 0
            self.nfa_stk = []

            for token in post:
                if token.type == TypedToken.TYPE_CHR:
                    self.process_chr(token)
                elif token.type == TypedToken.TYPE_ALT:
                    self.process_alt()
                elif token.type == TypedToken.TYPE_CAT:
                    self.process_cat()
                elif token.type == TypedToken.TYPE_QUES:
                    self.process_ques()
                elif token.type == TypedToken.TYPE_PLUS:
                    self.process_plus()
                elif token.type == TypedToken.TYPE_STAR:
                    self.process_star()
                else:
                    raise Exception("未知的Token类型")
            assert len(self.nfa_stk), 1
            return self.nfa_stk[0]

    lexer = RegexLexer()
    nfa_builder = RegexPost2NFA()

    @classmethod
    def regex2nfa(cls, pattern):
        tokens = cls.lexer.get_tokens(pattern)
        post = RegexParser.parse2post(tokens)
        return cls.nfa_builder.post2nfa(post)

    @classmethod
    def nfa2dfa(cls, nfa):
        def closure(state):
            bfs, result = deque([state]), {state}
            while len(bfs):
                src = bfs.popleft()
                for dst in src.epsilons:
                    if dst not in result:
                        bfs.append(dst)
                        result.add(dst)
            return result

        states, symbols = find_all_reachable_states(nfa.head)
        table = {s: {sym: None for sym in symbols} for s in states}
        closures = {s: closure(s) for s in states}

        for s in states:
            for sym in filter(lambda e: e != EPSILON, symbols):
                dst = s.move.get(sym, None)
                table[s][sym] = set()
                if dst is not None:
                    if isinstance(dst, FiniteAutomatonState):
                        table[s][sym].add(s.move[sym])
                    else:
                        table[s][sym].update(s.move[sym])
            table[s][EPSILON] = set(s.epsilons)

        number = 0
        dfa_move_symbols = symbols.copy()
        dfa_move_symbols.remove(EPSILON)
        dfa_head = DFA.State(number)
        dfa_closures = {dfa_head: closures[nfa.head]}
        dfa_table = {dfa_head: dict()}
        dfa_tails = set()
        number += 1
        bfs = deque([dfa_head])
        while len(bfs):
            state = bfs.popleft()
            for sym in dfa_move_symbols:
                new_closure = set()
                for row in dfa_closures[state]:  # 寻找所有后继状态
                    for x in table[row][sym]:
                        # new_closure.update(closure(x))
                        new_closure.update(closures[x])

                # print('[%s] -%s-> [%s]' % (state, sym, new_closure))
                if len(new_closure):
                    for k, v in dfa_closures.items():
                        if new_closure == v:
                            dfa_table[state][sym] = k
                            break
                    else:
                        dfa_node = DFA.State(number)
                        number += 1
                        bfs.append(dfa_node)
                        dfa_closures[dfa_node] = new_closure
                        dfa_table[state][sym] = dfa_node
                        dfa_table[dfa_node] = {k: None
                                               for k in dfa_move_symbols}
                        for i in new_closure:
                            if i.is_end:
                                dfa_node.is_end = True
                                dfa_tails.add(dfa_node)
                                break
                else:
                    # RECORD: 注意考虑闭包结果为空的情况
                    dfa_table[state][sym] = None
                    pass

        # dfa_states = dfa_closures.keys()
        # dfa_states = dfa_table.keys()

        # 按照状态表构建自动机状态之间的连接
        for s in dfa_table.keys():
            for k, v in dfa_table[s].items():
                if v is not None:
                    s.move[k] = v

        return DFA.DFA(dfa_head, dfa_tails)

    @classmethod
    def minimize_dfa(cls, dfa):
        """
        [原地修改]
        :param dfa:
        :return:
        """
        states, symbols = find_all_reachable_states(dfa.head)
        table = {s: {sym: s.move.get(sym, None)
                     for sym in symbols}
                 for s in states}

        non_final_states, final_states = set(), set()
        for s in states:
            if s.is_end:
                final_states.add(s)
            else:
                non_final_states.add(s)

        # subsets储存着多个不相交的子集
        subsets = [non_final_states, final_states]

        # 分割出各个不相交等价状态子集的集合
        found_new = True
        while found_new:
            found_new = False
            for subset in subsets:
                # 当前子集中所有NFA状态及其邻边状态
                # {状态: {字符: 该状态在该字符下转移的目标状态}}
                x = {s: table[s].copy() for s in subset}
                # 将x转换成所属集合表，用于检查等价性。转换成如下格式：
                # {状态: {字符: 该字符下转移的目标状态属于subsets中的哪个子集}}
                for s, move in x.items():
                    for toward, d in move.items():
                        for item in subsets:
                            if d in item:
                                x[s][toward] = item
                                break
                        else:
                            # 如果上述的目标状态无法在subsets的任何子中找到
                            # 即:目标状态为None(该状态在该字符下没有目标转移状态)
                            # 那就设为None
                            x[s][toward] = None
                bucket = dict()
                for s, v in x.items():
                    if v is not None:
                        bk = tuple(sorted(
                            [(i[0],
                              None if i[1] is None else tuple(
                                  sorted(i[1], key=lambda e: e.name))
                              )
                             for i in v.items()]
                        ))
                        if bk in bucket:
                            bucket[bk].add(s)
                        else:
                            bucket[bk] = {s}
                new_subsets = bucket.values()
                if len(new_subsets) > 1:
                    found_new = True
                    subsets.remove(subset)
                    subsets.extend(new_subsets)
                    break

        # 为前面分割出的各个不相交子集选出代表元素
        # 同时需要保证原DFA的起始状态一定是该状态所在子集的代表元素
        agent = dict()
        for subset in subsets:
            if dfa.head in subset:
                for s in subset:
                    agent[s] = dfa.head
            else:
                sorted_subset = tuple(sorted(subset, key=lambda s: s.name))
                for s in sorted_subset:
                    agent[s] = sorted_subset[0]

        # 重建DFA状态之间的联系
        new_states = tuple(set(agent.values()))
        for src in new_states:
            for toward, dst in src.move.items():
                src.move[toward] = agent[dst]

        return DFA.DFA(dfa.head, set([s for s in new_states if s.is_end]))
