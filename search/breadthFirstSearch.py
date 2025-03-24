from .utils.frontierSets import Queue
from .utils.searchAlgorithm import search


def bfs(level):
    return search(level, Queue())
