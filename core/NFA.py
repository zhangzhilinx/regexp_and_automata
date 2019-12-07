from core import FiniteAutomatonState


class State(FiniteAutomatonState):
    def __init__(self, name):
        super(State, self).__init__(name)
