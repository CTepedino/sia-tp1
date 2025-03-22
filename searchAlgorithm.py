from frontierSets import Collection, Queue, Stack
from sokobanRules import SokobanRules


def search(level, frontier: Collection):
    game = SokobanRules(level)
    current_node = game.copy_state()

    explored = set()
    nodes_expanded = 0

    while current_node is not None:

        if current_node.is_solved():
            return current_node.path

        nodes_expanded += 1
        explored.add(current_node)
        for direction in current_node.get_valid_moves():

            game.load_state(current_node)
            game.move_to(direction)

            new_state = game.copy_state()
            if new_state not in explored:
                frontier.add(new_state)



        current_node = frontier.next()

    return None

def bfs(level):
    return search(level, Queue())

def dfs(level):
    return search(level, Stack())

if __name__ == "__main__":
    level = [
        "#######",
        "#P    #",
        "# B T #",
        "#######"
    ]
    solution = bfs(level)
    print(solution)

    solution = dfs(level)
    print(solution)