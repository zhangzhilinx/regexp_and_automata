from core import FiniteAutomatonState


class State(FiniteAutomatonState):
    def __init__(self, name, is_end=False):
        super(State, self).__init__(name, is_end)


def dfa_match(start, test_str):
    state = start
    for c in test_str:
        try:
            state = state.move[c]
        except KeyError:
            return False
    print(state)
    return state.is_end
