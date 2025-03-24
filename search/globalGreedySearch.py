from .utils.frontierSets import Sorted
from .utils.searchAlgorithm import search


def greedy(level, heuristic):
    return search(level, Sorted(heuristic))

