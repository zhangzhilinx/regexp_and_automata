from core import FiniteAutomatonState


class State(FiniteAutomatonState):
    def __init__(self, name, is_end=False):
        super(State, self).__init__(name, is_end)


class SimpleNFA:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail
        self.tail.is_end = True
