import time

from frontierSets import Collection
from sokobanRules import SokobanRules, Directions

class SearchResults:
    def __init__(self, level: [str], path: [Directions], nodes_expanded: int, nodes_in_frontier: int, time: float):
        self.level = level
        self.solution = path
        self.nodes_expanded = nodes_expanded
        self.nodes_in_frontier = nodes_in_frontier
        self.time = f"{time:.2f}s"

    def to_dict(self):
        return {
            "level": self.level,
            "solved": True if self.solution else False,
            "solution": [direction.value for direction in self.solution],
            "cost": len(self.solution),
            "nodes_expanded": self.nodes_expanded,
            "nodes_in_frontier": self.nodes_in_frontier,
            "time": self.time
        }


def search(level, frontier: Collection):
    start_time = time.time()
    game = SokobanRules(level)
    current_node = game.copy_state()

    explored = set()
    nodes_expanded = 0

    while current_node is not None:
        if current_node.is_solved():
            end_time = time.time()
            return SearchResults(level, current_node.path, nodes_expanded, len(frontier), end_time - start_time)

        nodes_expanded += 1
        explored.add(current_node)
        for direction in current_node.get_valid_moves():

            game.load_state(current_node)
            game.move_to(direction)

            new_state = game.copy_state()
            if new_state not in explored:
                frontier.add(new_state)



        current_node = frontier.next()

    end_time = time.time()
    return SearchResults(level, None, nodes_expanded, len(frontier), end_time - start_time)
