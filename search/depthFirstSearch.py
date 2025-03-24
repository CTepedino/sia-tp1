from .utils.frontierSets import Stack
from .utils.searchAlgorithm import search


def dfs(level):
    return search(level, Stack())

