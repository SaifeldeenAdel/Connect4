import numpy as np
from constants import EMPTY, HUMAN, AI, COLUMNS, ROWS, NUM_BITS_PER_COLUMN
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
        binary_state = self.state.get_binary_state()
        num_occupied = NUM_BITS_PER_COLUMN - ROWS

        for col in range(COLUMNS):
            start = col * NUM_BITS_PER_COLUMN
            end = start + NUM_BITS_PER_COLUMN

            column_representation = binary_state[start: end]

            num_rows_occupied = int(column_representation[:num_occupied], 2)

            if num_rows_occupied < ROWS:
                columns_available.append(col)
        return columns_available

    # Returns a list of columns that have empty rows left
    # def get_possible_moves(self) -> list[int]:
    #    possible_moves = []
    #    for col in range(COLUMNS):
    #        if self.state[0, col] == EMPTY:  # Check if the top cell of the column is empty
    #            possible_moves.append(col)
    #    return possible_moves

    def insert(self, col: int, player: int) -> 'BoardState':
        if col in self.get_possible_moves():
            binary_state = self.state.get_binary_state()
            num_occupied = NUM_BITS_PER_COLUMN - ROWS

            start = col * NUM_BITS_PER_COLUMN
            end = start + NUM_BITS_PER_COLUMN

            column_representation = binary_state[start: end]
            new_rows_string = self.increment_binary(column_representation[:num_occupied]) # numrows occupied
            num_rows_occupied = int(new_rows_string,2)
            disks = column_representation[-ROWS:]
            #print(f"olddisks: {disks}")
            new_disks = self.replace_character_in_string(disks, num_rows_occupied, str(self.get_player_binary(player)))
            #print(f"newdisks: {new_disks}")
            new_column_representation = new_rows_string + new_disks
            #print(f"newcol {new_column_representation}")
            new_binary_representation = binary_state[:start] + new_column_representation + binary_state[end:]
            #print(f"newbinaryrep {new_binary_representation}")
            decimal = int(new_binary_representation, 2)
            return BoardState(InternalState(decimal))
        print(f"ERROR CAN NOT INSERT IN COLUMN {col}")

    def replace_character_in_string(self, original_string: str, index: int, new_char: str) -> str:
        return original_string[:index] + new_char + original_string[index + 1:]

    def get_player_binary(self, player: int):  # plater 1 is red and else is 2 which is yellow
        return 0 if player == 1 else 1

    def increment_binary(self,num: str)-> str:
        decimal_num = int(num, 2)
        decimal_num += 1
        binary_state = bin(decimal_num)[2:]
        binary_state = '0' * (3 - len(binary_state)) + binary_state
        return binary_state

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


# binary_string = '010 000000 100 000001 001 000001 100 001110 011 000001 001 000001 000 000000'
binary_string = '010 000000 100 000100 001 100000 100 111000 011 001000 001 100000 000 000000'
binary_string2 ='010 000000 101 010100 001 100000 100 111000 011 001000 001 100000 000 000000'
 #              '010 000000 100 000100 001 100000 100 111000 011 001000 101 010000 000 00000'
#               '010 000000 100 000100 001 100000 100 111000 011 001000 101 01000000000000'
decimal_number = int(binary_string.replace(" ", ""), 2)

b = InternalState(decimal_number)

bs = BoardState(b)
print("MAIN ")
print(bs.state.get_numpy_format())


l = bs.get_neighbors(2)
for s in l:
    print('smth')
    print(s.state.get_numpy_format())

#print("BEFORE")
#print(bs.state.get_numpy_format())

#new_board = bs.insert(1, 2)

#print("AFTER INSERTION")
#print(new_board.state.get_numpy_format())

#new_board2 = bs.insert(5, 2)

#print("AFTER INSERTION2")
#print(new_board2.state.get_numpy_format())

#new_board3 = bs.insert(6, 2)

#print("AFTER INSERTION3")
#print(new_board3.state.get_numpy_format())
