from collections import deque

EPSILON = 'EPSILON'


class FiniteAutomatonState:
    def __init__(self, name, is_end=False):
        self._name = name
        self._next = dict()
        self.is_end = is_end
        self.epsilons = set()

    def __eq__(self, other):
        return self._name == other.name and self._next == other.move

    def __hash__(self):
        return hash(self._name)

    def __repr__(self):
        return '%s' % (repr(self._name))

    def __str__(self):
        return '%s' % (str(self._name))

    @property
    def name(self):
        return self._name

    @property
    def move(self):
        return self._next


def get_dot_content(start):
    content = "digraph FA {\nrankdir = LR\n"
    content += "root = \"%s\"\n" % str(start)
    content += "start [shape=point]\n"
    content += "start -> \"%s\"\n" % str(start)
    bfs = deque([start])
    states = {start}
    while len(bfs):
        src = bfs.popleft()
        for toward, dst in src.move.items():  # src -[toward]-> dst
            for d in (dst,) if isinstance(dst, FiniteAutomatonState) else dst:
                content += "\"%s\" -> \"%s\" [label=\"%s\"]\n" \
                           % (str(src), str(d), str(toward))
                if d not in states:
                    bfs.append(d)
                    states.add(d)
        for dst in src.epsilons:  # src -[ε]-> dst
            content += "\"%s\" -> \"%s\" [label=\"ε\"]\n" \
                       % (str(src), str(dst))
            if dst not in states:
                bfs.append(dst)
                states.add(dst)
    for state in states:
        if state.is_end:
            content += "\"%s\" [shape=doublecircle]\n" % str(state)
        else:
            content += "\"%s\" [shape=circle]\n" % str(state)
    content += '}'
    return content


def find_all_reachable_states(start):
    number = 0
    states, symbols = {start: number}, {EPSILON}
    number += 1
    bfs = deque([start])
    while len(bfs):
        src = bfs.popleft()
        for toward, dst in src.move.items():
            symbols.add(toward)
            for d in (dst,) if isinstance(dst, FiniteAutomatonState) else dst:
                if d not in states:
                    bfs.append(d)
                    states[d] = number
                    number += 1
        for dst in src.epsilons:
            if dst not in states:
                bfs.append(dst)
                states[dst] = number
                number += 1
    return [k for k, v in sorted(states.items(),
                                 key=lambda e: e[1])], list(symbols)


def eliminate_duplicate_states(start):
    states, _ = find_all_reachable_states(start)
    final_reachable, final_unreachable = set(), set()

    for state in states:
        if state.is_end:
            final_reachable.add(state)
        else:
            final_unreachable.add(state)

    # 尝试搜索任何可以达到终态的状态，并加入到可达终态的状态集合
    # 直到某一次 找不到任何状态 可以到达 任何可达终态的状态
    found_new = True
    while found_new:
        found_new = False
        for state in final_unreachable:
            for _, to in state.move.items():
                for t in (to,) if isinstance(to, FiniteAutomatonState) else to:
                    if t in final_reachable:
                        final_reachable.add(state)
                        final_unreachable.remove(state)
                        found_new = True
                        break
                else:
                    continue
                break
            else:
                for to in state.epsilons:
                    if to in final_reachable:
                        final_reachable.add(state)
                        final_unreachable.remove(state)
                        found_new = True
                        break
                else:
                    continue
                break
            break

    visited = {k: False for k, _ in find_all_reachable_states(start)}

    def states_pruning(src):
        visited[src] = True
        need_remove_move, need_remove_eps = set(), set()

        for toward, dst in src.move.items():
            for d in (dst,) if isinstance(dst, FiniteAutomatonState) else dst:
                if d in final_reachable:
                    if not visited[d]:
                        states_pruning(d)
                else:
                    need_remove_move.add(toward)
        for dst in src.epsilons:
            if dst in final_reachable:
                if not visited[dst]:
                    states_pruning(dst)
            else:
                need_remove_eps.add(dst)

        [src.move.pop(i) for i in need_remove_move]
        [src.epsilons.remove(i) for i in need_remove_eps]

    states_pruning(start)


"""
无效的代码：试图用纯DFS法自顶向下找出所有可达终态的状态是不可行的

这是原先的思路，可以通过带标记的DFS搜索完成这个任务，但是：
即使是使用了带标记法的DFS，也无法保证在试图完成任务时不陷入无限循环
除非使用为每次DFS搜索创建对应的标记数组，同时乱序DFS（按顺序DFS必死）
也还没实现完，不过这样的代码实现，不要也罢，仅作前车之鉴
"""
# def eliminate_duplicate_states(start):
#     """
#     [原地修改]
#     :param start:
#     :return:
#     """
#
#     # 避免单条路径上循环
#     visited = {k: False for k in find_all_reachable_states(start)}
#
#     def states_dfs(src):
#         visited[src] = True
#         child_can_reach_final = False
#         for toward, dst in src.move.items():
#             if not visited[dst]:
#                 if not states_dfs(dst):
#                     src.move.pop(toward)
#                 else:
#                     child_can_reach_final = True
#         for dst in src.epsilons:
#             if not visited[dst]:
#                 if not states_dfs(dst):
#                     src.epsilons.remove(dst)
#                 else:
#                     child_can_reach_final = True
#
#         visited[src] = False
#         return True if src.is_end else child_can_reach_final
#
#     states_dfs(start)
