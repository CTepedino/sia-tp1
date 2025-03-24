from .utils.searchAlgorithm import search
from .utils.frontierSets import Sorted
from sokoban.rules import GameState

def heuristic_plus_cost(heuristic):
    def f(state: GameState):
        h = heuristic(state)
        g = len(state.path)
        return g + h, h

    return f

def a_star(level, heuristic):
    return search(level, Sorted(heuristic_plus_cost(heuristic)))

