from core import FiniteAutomatonState


class State(FiniteAutomatonState):
    def __init__(self, name):
        super(State, self).__init__(name)


def dfa_match(start, finals, test_str):
    state = start
    for c in test_str:
        try:
            state = state.move[c]
        except KeyError:
            return False
    print(state)
    return state in finals
