import numpy as np
from constants import EMPTY, HUMAN, AI, COLUMNS, ROWS, COLUMN_BITS, ROW_BITS, ONE_END_OPEN_BIAS, THREES_BIAS, FOURS_BIAS
from InternalState import InternalState
import random
import uuid

class BoardState:
    def __init__(self, state: InternalState):
        self.state = state
        self.score = 0
        self.tree_id = uuid.uuid4()

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

    def get_column_representation(self, col: int) -> tuple[str, int, int]:
        binary_state = self.state.get_binary_state()

        start = col * COLUMN_BITS
        end = start + COLUMN_BITS

        return binary_state[start: end], start, end

    def replace_character_in_string(self, original_string: str, index: int, new_char: str) -> str:
        return original_string[:index] + new_char + original_string[index + 1:]

    def get_player_binary(self, player: int):  # player 1 is red and else is 2 which is yellow
        #  0 in aCOLUMN_BITSrray -> EMPTY
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

    def get_heuristic(self, maximizer, minimizer):
        # threes = self.__getConnected3s(maximizer) - self.__getConnected3s(minimizer)
        # fours = self.__getConnected4s(maximizer) - self.__getConnected4s(minimizer)
        # return FOURS_BIAS * fours + THREES_BIAS * threes
        return random.randint(-5,5)
    
    def get_score(self, maximizer, minimizer):
        return self.__getConnected4s(maximizer) - self.__getConnected4s(minimizer)

    def __getConnected4s(self, player):
        count = 0
        current_state = self.state.get_numpy_format()
        # check rows
        for row in current_state:
            for i in range(0, COLUMNS-3):
                if row[i] == player and row[i+1] == player and row[i+2] == player and row[i+3] == player:
                    count += 1
        # check columns
        for col in range(COLUMNS):
            for i in range(0, ROWS-3):
                if current_state[i][col] == player and current_state[i+1][col] == player and current_state[i+2][col] == player and current_state[i+3][col] == player:
                    count += 1
        # check +ve diagonals
        for i in range(0, ROWS-3):
            for j in range(0, COLUMNS-3):
                if current_state[i][j] == player and current_state[i+1][j+1] == player and current_state[i+2][j+2] == player and current_state[i+3][j+3] == player:
                    count += 1
        # check -ve diagonals 
        for i in range(0, ROWS-3):
            for j in range(3, COLUMNS):
                if current_state[i][j] == player and current_state[i+1][j-1] == player and current_state[i+2][j-2] == player and current_state[i+3][j-3] == player:
                    count += 1       
        return count
    
    def __getConnected3s(self, player):
        Current_state = self.state.get_numpy_format()
        count = 0
        # check rows
        for row in range(ROWS):
            for i in range(0, COLUMNS-2):
                if(i == 0):
                    if Current_state[row][i] == player and Current_state[row][i+1] == player and Current_state[row][i+2] == player and Current_state[row][i+3] == EMPTY:
                        count += 1* ONE_END_OPEN_BIAS
                else:
                    if Current_state[row][i] == player and Current_state[row][i+1] == player and Current_state[row][i+2] == player and Current_state[row][i+3] == EMPTY and Current_state[row][i-1] == EMPTY:
                        count += 1
        # check columns
        for col in range(COLUMNS):
            for i in range(0, ROWS-2):
                if(i == 0):
                    if Current_state[i][col] == player and Current_state[i+1][col] == player and Current_state[i+2][col] == player and Current_state[i+3][col] == EMPTY:
                        count += 1* ONE_END_OPEN_BIAS
                else:
                    if Current_state[i][col] == player and Current_state[i+1][col] == player and Current_state[i+2][col] == player and Current_state[i-1][col] == EMPTY and Current_state[i+3][col] == EMPTY:
                        count += 1
        #check +ve diagonals
        for i in range(0, ROWS-2):
            for j in range(0, COLUMNS-2):
                if(i == 0):
                    if Current_state[i][j] == player and Current_state[i+1][j+1] == player and Current_state[i+2][j+2] == player and Current_state[i+3][j+3] == EMPTY:
                        count += 1* ONE_END_OPEN_BIAS
                else:
                    if Current_state[i][j] == player and Current_state[i+1][j+1] == player and Current_state[i+2][j+2] == player and Current_state[i-1][j-1] == EMPTY and Current_state[i+3][j+3] == EMPTY:
                        count += 1
        #check -ve diagonals
        for i in range(0, ROWS-2):
            for j in range(3, COLUMNS):
                if(i == 0):
                    if Current_state[i][j] == player and Current_state[i+1][j-1] == player and Current_state[i+2][j-2] == player and Current_state[i+3][j-3] == EMPTY:
                        count += 1* ONE_END_OPEN_BIAS
                else:
                    if Current_state[i][j] == player and Current_state[i+1][j-1] == player and Current_state[i+2][j-2] == player and Current_state[i-1][j+1] == EMPTY and Current_state[i+3][j-3] == EMPTY:
                        count += 1
        return count

            
    def __getCenterDistribution(self, player):
        Current_state = self.state.get_numpy_format()
        count = 0
        for row in range(ROWS):
            for col in range(COLUMNS):
                if Current_state[row][col] == player:
                    count += -abs(col - 3.5) + 3.5 
        return count
    
    def __getAdjecentEmpty(self, player):
        current_state = self.state.get_numpy_format()
        count = 0
        for row in range(ROWS):
            for col in range(COLUMNS):
                if current_state[row][col] == player:
                    if row < ROWS - 1 and current_state[row + 1][col] == EMPTY:
                        count += 1
                    if row > 0 and current_state[row - 1][col] == EMPTY:
                        count += 1
                    if col < COLUMNS - 1 and current_state[row][col + 1] == EMPTY:
                        count += 1
                    if col > 0 and current_state[row][col - 1] == EMPTY:
                        count += 1
                    if row < ROWS - 1 and col < COLUMNS - 1 and current_state[row + 1][col + 1] == EMPTY:
                        count += 1
                    if row > 0 and col > 0 and current_state[row - 1][col - 1] == EMPTY:
                        count += 1
                    if row < ROWS - 1 and col > 0 and current_state[row + 1][col - 1] == EMPTY:
                        count += 1
                    if row > 0 and col < COLUMNS - 1 and current_state[row - 1][col + 1] == EMPTY:
                        count += 1
        return count

    def get_id(self):
        return self.tree_id
    
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
