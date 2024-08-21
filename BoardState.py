import numpy as np
from constants import EMPTY, HUMAN, AI, COLUMNS, ROWS, COLUMN_BITS, ROW_BITS, ONE_END_OPEN_BIAS, THREES_BIAS, FOURS_BIAS, INITIAL_STATE, CENTER_BIAS, ADJACENT_BIAS
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
        threes = self.getConnected3s(maximizer) - self.getConnected3s(minimizer)
        fours = self.getConnected4s(maximizer) - self.getConnected4s(minimizer)
        central = self.getCenterDistribution(maximizer) - self.getCenterDistribution(minimizer)
        empty = self.getAdjecentEmpty(maximizer) - self.getAdjecentEmpty(minimizer)

        return FOURS_BIAS * fours + THREES_BIAS * threes + CENTER_BIAS * central + ADJACENT_BIAS * empty
        # return random.randint(-5,5)
    
    def get_score(self, maximizer, minimizer):
        return self.getConnected4s(maximizer) - self.getConnected4s(minimizer)

    def getConnected4s(self, player):
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
    
    def getConnected3s(self, player):
      Current_state = self.state.get_numpy_format()
      count = 0
      ROWS, COLUMNS = Current_state.shape

      # Check rows
      for row in range(ROWS):
          for col in range(COLUMNS - 2):  # Ensure there are at least 3 columns remaining
              if (Current_state[row][col] == player and
                  Current_state[row][col+1] == player and
                  Current_state[row][col+2] == player):
                  count += 1

      # Check columns
      for col in range(COLUMNS):
          for row in range(ROWS - 2):  # Ensure there are at least 3 rows remaining
              if (Current_state[row][col] == player and
                  Current_state[row+1][col] == player and
                  Current_state[row+2][col] == player):
                  count += 1

      # Check positive diagonals
      for row in range(ROWS - 2):  # Ensure there are at least 3 rows remaining
          for col in range(COLUMNS - 2):  # Ensure there are at least 3 columns remaining
              if (Current_state[row][col] == player and
                  Current_state[row+1][col+1] == player and
                  Current_state[row+2][col+2] == player):
                  count += 1

      # Check negative diagonals
      for row in range(ROWS - 2):  # Ensure there are at least 3 rows remaining
          for col in range(2, COLUMNS):  # Ensure there are at least 3 columns remaining
              if (Current_state[row][col] == player and
                  Current_state[row+1][col-1] == player and
                  Current_state[row+2][col-2] == player):
                  count += 1

      return count
            
    def getCenterDistribution(self, player):
        Current_state = self.state.get_numpy_format()
        count = 0
        for row in range(ROWS):
            for col in range(COLUMNS):
                if Current_state[row][col] == player:
                    count += abs(3 - col)
        return count
    
    def getAdjecentEmpty(self, player):
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
    
    @staticmethod
    def list_to_boardstate(ls):
      board = np.array(ls)
      state_bits = []
      for col in range(board.shape[1]):
          column = board[:, col]
          # Count the number of non-zero entries (disks) in the column
          num_disks = np.count_nonzero(column)
          # Convert the number of disks to a 3-bit binary representation
          num_disks_bits = f'{num_disks:03b}'
          # Get the disks and convert them to binary (0 for player 1, 1 for player 2)
          disks_bits = ''.join('1' if disk == 2 else '0' for disk in column)
          # Pad disks_bits to ensure it's always 6 bits long
          disks_bits = disks_bits.zfill(6)[::-1]
          # Combine the number of disks and the disks themselves
          state_bits.append(num_disks_bits + disks_bits)
          print(state_bits)
      
      # Combine all columns' binary representations into a single string
      binary_string = ''.join(state_bits)
      return BoardState(InternalState(int(binary_string, 2)))

# binary_string = '010 000000 100 000100 001 100000 100 111000 011 001000 001 100000 000 000000'
# binary_string2 = '010 000000 101 010100 001 100000 100 111000 011 001000 001 100000 000 000000'
#              '010 000000 100 000100 001 100000 100 111000 011 001000 101 010000 000 00000'
#               '010 000000 100 000100 001 100000 100 111000 011 001000 101 01000000000000'
# binary_string = 
# decimal_number = int(binary_string.replace(" ", ""), 2)
# INITIAL_STAT = int('011 000000 000 000000 000 000000 010 101000 011 000000 000 000000 000 000000'.replace(" ", ""), 2)
# b = InternalState(INITIAL_STAT)
# ls = [
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 0, 0, 1, 0, 0],
#     [1, 0, 0, 1, 1, 0, 0],
#     [1, 0, 0, 2, 1, 0, 0]
# ]
# print(BoardState.list_to_boardstate(ls).state.get_numpy_format())
# print("MAIN ")
