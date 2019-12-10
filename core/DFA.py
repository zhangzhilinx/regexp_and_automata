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

    def search(self, text, start=0):
        if isinstance(self.head, State):
            return dfa_search(self.head, text, start)
        else:
            return -1, 0


def dfa_match(state_head, text):
    state = state_head
    for c in text:
        try:
            state = state.move[c]
        except KeyError:
            return False
    return state.is_end


def dfa_search(state_head, text, start=0):
    size = len(text)
    state = state_head
    pi = end = start
    while pi < size:
        try:
            state = state.move[text[pi]]
            pi += 1
            if state.is_end:
                end = pi
        except KeyError:
            if end > start:
                return start, end - start
            start += 1
            state = state_head
            pi = start
    if end > start:
        return start, end - start
    else:
        return -1, 0
