import numpy as np
from constants import EMPTY, HUMAN, AI, COLUMNS, ROWS
from InternalState import InternalState


class BoardState:
    def __init__(self, state: InternalState, id: int = None):
        self.state = state
        self.score = 0
        self.tree_id = id

    # Returns a list of columns that have empty rows left
    def get_possible_moves(self) -> list[int]:
        possible_moves = []
        for col in range(COLUMNS):
            if self.state[0, col] == EMPTY:  # Check if the top cell of the column is empty
                possible_moves.append(col)
        return possible_moves

    # Inserts into an empty column
    def insert(self, col: int, player: int) -> np.ndarray:
        if col in self.get_possible_moves():
            new_state = self.state.copy()

            for row in range(ROWS - 1, -1, -1):
                if new_state[row, col] == EMPTY:
                    new_state[row, col] = player
                    return BoardState(new_state)
        print("Invalid Move")
        return self

    def get_neighbors(self, player: int):
        neighbors = []
        possible_moves = self.get_possible_moves()

        for col in possible_moves:
            next_state = self.insert(col, player)
            neighbors.append(next_state)

        return neighbors

    def is_terminal(self, player):
        return not np.any(self.state == 0)

    def get_heuristic(self, player):
        pass

    def __getConnected4s(self, player):
        count = 0
        # Check horizontal lines
        for row in range(self.state.shape[0]):
            for col in range(self.state.shape[1] - 3):
                if np.all(self.state[row, col:col + 4] == player):
                    count += 1

        # Check vertical lines
        for col in range(self.state.shape[1]):
            for row in range(self.state.shape[0] - 3):
                if np.all(self.state[row:row + 4, col] == player):
                    count += 1

        # Check positive diagonals (bottom-left to top-right)
        for row in range(3, self.state.shape[0]):
            for col in range(self.state.shape[1] - 3):
                if np.all([self.state[row - i, col + i] == player for i in range(4)]):
                    count += 1

        # Check negative diagonals (top-left to bottom-right)
        for row in range(self.state.shape[0] - 3):
            for col in range(self.state.shape[1] - 3):
                if np.all([self.state[row + i, col + i] == player for i in range(4)]):
                    count += 1

        return count  # This can be multiplied by some large factor for the heuristic

    def __getConnected3s(self, player):
        pass

    def __getCenterDistribution(self, player):
        pass

    def __repr__(self) -> str:
        return str(self.state)
