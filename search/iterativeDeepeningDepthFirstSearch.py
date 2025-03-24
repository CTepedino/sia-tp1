from .utils.searchAlgorithm import search
from .utils.frontierSets import Sorted

def iddfs(level, depth_iteration):
    return search(level, Sorted(lambda state: (((len(state.path)-1) // depth_iteration), -1 * len(state.path))))
