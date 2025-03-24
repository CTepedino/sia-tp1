import enum
from copy import copy

class Directions(enum.Enum):
    UP = "Up"
    DOWN = "Down"
    LEFT = "Left"
    RIGHT = "Right"

class GameState:
    def __init__(self, player, boxes, walls, targets, path_from_start: [Directions]):
        self.player = player
        self.boxes = frozenset(boxes)
        self.walls = walls
        self.targets = targets
        self.path = copy(path_from_start)

    def __eq__(self, other):
        if isinstance(other, GameState):
            return (self.player == other.player and
                    self.boxes == other.boxes)
        return False

    def __hash__(self):
        return hash((self.player, self.boxes))

    def get_valid_moves(self):
        moves = []
        directions = {
            (0,-1): Directions.UP,
            (0,1): Directions.DOWN,
            (-1, 0): Directions.LEFT,
            (1, 0): Directions.RIGHT
        }
        for direction in directions:
            moved_pos = (self.player[0] + direction[0], self.player[1] + direction[1])
            if moved_pos not in self.walls:
                if moved_pos in self.boxes:
                    moved_box_pos = (moved_pos[0] + direction[0], moved_pos[1] + direction[1])
                    if moved_box_pos not in self.walls and moved_box_pos not in self.boxes:
                        moves.append(directions[direction])
                else:
                    moves.append(directions[direction])
        return moves

    def is_solved(self):
        return self.boxes == self.targets

    def __repr__(self):
        return f"[Player: {self.player}, Boxes: {self.boxes}]"

class SokobanRules:
    def __init__(self, level: [str]):
        self.boxes = set()
        self.targets = set()
        self.walls = set()
        self.player = None
        self.path = []

        for y, row in enumerate(level):
            for x, cell in enumerate(row):
                match cell:
                    case "P": self.player = (x, y)
                    case "#": self.walls.add((x, y))
                    case "B": self.boxes.add((x, y))
                    case "T": self.targets.add((x, y))
                    case "_" | " ": pass
                    case _: raise Exception("invalid level")

        if len(self.boxes) != len(self.targets) or self.player is None:
            raise Exception("invalid level")


    def is_solved(self):
        return self.boxes == self.targets

    def move(self, dx, dy):
        new_pos = (self.player[0] + dx, self.player[1] + dy)

        if new_pos in self.walls:
            return

        if new_pos in self.boxes:
            new_box_pos = (new_pos[0] + dx, new_pos[1] + dy)
            if new_box_pos in self.walls or new_box_pos in self.boxes:
                return
            self.boxes.remove(new_pos)
            self.boxes.add(new_box_pos)

        self.player = new_pos

    def move_to(self, direction: Directions):
        match direction:
            case Directions.UP: self.move(0, -1)
            case Directions.DOWN: self.move(0, 1)
            case Directions.LEFT: self.move(-1,0)
            case Directions.RIGHT: self.move(1,0)
        self.path.append(direction)

    def copy_state(self):
        return GameState(self.player, self.boxes, self.walls, self.targets, self.path)

    def load_state(self, state: GameState):
        self.player = state.player
        self.boxes = set(state.boxes)
        self.path = list(state.path)