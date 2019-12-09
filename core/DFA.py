from core import FiniteAutomatonState


class State(FiniteAutomatonState):
    def __init__(self, name, is_end=False):
        super(State, self).__init__(name, is_end)


class SimpleDFA:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail
        self.tail.is_end = True

    def match(self, text):
        if isinstance(self.head, State):
            return dfa_match(self.head, text)
        else:
            return False


class DFA:
    def __init__(self, head, tails=None):
        self.head = head
        self.tails = set() if tails is None else tails
        for t in self.tails:
            t.is_end = True

    def match(self, text):
        if isinstance(self.head, State):
            return dfa_match(self.head, text)
        else:
            return False


def dfa_match(start, text):
    state = start
    for c in text:
        try:
            state = state.move[c]
        except KeyError:
            return False
    return state.is_end
