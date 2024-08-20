import numpy as np
from constants import EMPTY, HUMAN, AI, COLUMNS, ROWS, COLUMN_BITS, ROW_BITS
from InternalState import InternalState


class BoardState:
    def __init__(self, state: InternalState):
        self.state = state
        self.score = 0
        self.tree_id = self.state.get_decimal_state()

    def get_possible_moves(self) -> list[int]:
        #  0 in array -> EMPTY
        #  1 in array -> player 1 -> RED
        #  2 in array -> player 2 -> YELLOW
        #  BINARY 0 -> RED
        #  BINARY 1 -> YELLOW
        columns_available = []

        for col in range(COLUMNS):
            column_representation, _, _ = self.get_column_representation(col)

            num_rows_occupied = int(column_representation[:ROW_BITS], 2)

            if num_rows_occupied < ROWS:
                columns_available.append(col)
        return columns_available

    def insert(self, col: int, player: int) -> 'BoardState':
        if col in self.get_possible_moves():
            column_representation, start, end = self.get_column_representation(col)
            # -----------

            new_rows_string = self.increment_binary(column_representation[:ROW_BITS])
            num_rows_occupied = int(new_rows_string, 2)
            #  to get the disks, it is the last "ROWS" bit from the column representation
            disks = column_representation[-ROWS:]
            # print(f"olddisks: {disks}")
            #  inserting the new disk
            # print(f"player in insert {player}")
            new_disks = self.replace_character_in_string(disks, num_rows_occupied - 1,
                                                        str(self.get_player_binary(player)))

            # print(f"newdisks: {new_disks}")
            new_column_representation = new_rows_string + new_disks
            # print(f"newcol {new_column_representation}")

            new_binary_state = self.get_new_binary_state(start, new_column_representation, end)
            # print(f"newbinaryrep {new_binary_representation}")
            decimal = int(new_binary_state, 2)
            return BoardState(InternalState(decimal)), True
        print(f"ERROR CAN NOT INSERT IN COLUMN {col}")
        return self, False

    def get_new_binary_state(self, start: int, new_col_representation: str, end: int) -> str:
        binary_state = self.state.get_binary_state()
        return binary_state[:start] + new_col_representation + binary_state[end:]

    def get_column_representation(self, col: int) -> (str, int, int):
        binary_state = self.state.get_binary_state()

        start = col * COLUMN_BITS
        end = start + COLUMN_BITS

        return binary_state[start: end], start, end

    def replace_character_in_string(self, original_string: str, index: int, new_char: str) -> str:
        return original_string[:index] + new_char + original_string[index + 1:]

    def get_player_binary(self, player: int):  # player 1 is red and else is 2 which is yellow
        #  0 in array -> EMPTY
        #  1 in array -> player 1 -> RED
        #  2 in array -> player 2 -> YELLOW
        #  BINARY 0 -> RED
        #  BINARY 1 -> YELLOW
        return 0 if player == 1 else 1

    def increment_binary(self, num: str) -> str:
        decimal_num = int(num, 2)
        decimal_num += 1
        binary_state = bin(decimal_num)[2:]
        binary_state = '0' * (3 - len(binary_state)) + binary_state
        return binary_state

    def get_neighbors(self, player: int):
        neighbors = []
        possible_moves = self.get_possible_moves()
        opposing = 1 if player == 2 else 2

        for col in possible_moves:
            next_state, _ = self.insert(col, opposing)
            neighbors.append((col, next_state))

        return neighbors

    def is_terminal(self):
        return all(self.state.get_binary_state()[i:i+3] == '110' for i in range(0, len(self.state.get_binary_state()), 9))

    def get_heuristic(self, player):
        return 20 if player == AI else -20 
    
    def get_score(self, player):
        return 100 if player == AI else -100
        # return self.__getConnected4s(player) - self.__getConnected4s(opposing)

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

# binary_string = '010 000000 100 000001 001 000001 100 001110 011 000001 001 000001 000 000000'
# binary_string = '010 000000 100 000100 001 100000 100 111000 011 001000 001 100000 000 000000'
# binary_string2 = '010 000000 101 010100 001 100000 100 111000 011 001000 001 100000 000 000000'
#              '010 000000 100 000100 001 100000 100 111000 011 001000 101 010000 000 00000'
#               '010 000000 100 000100 001 100000 100 111000 011 001000 101 01000000000000'
# decimal_number = int(binary_string.replace(" ", ""), 2)

# b = InternalState(decimal_number)

# bs = BoardState(b)
# print("MAIN ")
# print(bs.state.get_numpy_format())
