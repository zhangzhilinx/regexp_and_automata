from collections import deque


class FiniteAutomatonState:
    def __init__(self, name):
        self._name = name
        self._next = dict()

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


def get_dot_content(finals, start):
    content = "digraph FA {\nrankdir = LR\n"
    content += "root = \"%s\"\n" % str(start)
    content += "start [shape=point]\n"
    content += "start -> \"%s\"\n" % str(start)
    bfs = deque([start])
    states = {start}
    while len(bfs):
        src = bfs.popleft()
        for toward, dst in src.move.items():  # src -[toward]-> dst
            content += "\"%s\" -> \"%s\" [label=\"%s\"]\n" \
                       % (str(src), str(dst), str(toward))
            if dst not in states:
                bfs.append(dst)
                states.add(dst)
    for state in states:
        if state in finals:
            content += "\"%s\" [shape=doublecircle]\n" % str(state)
        else:
            content += "\"%s\" [shape=circle]\n" % str(state)
    content += '}'
    return content
