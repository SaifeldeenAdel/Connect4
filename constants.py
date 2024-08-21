ROWS = 6
COLUMNS = 7
INITIAL_STATE = int('000 000000 000 000000 000 000000 000 000000 000 000000 000 000000 000 000000'.replace(" ", ""), 2)

ROW_BITS = len(bin(ROWS)[2:])  # row_bits are the number of bis needed to tell how many rows are occupied
COLUMN_BITS = ROW_BITS + ROWS  # column_bits are the number of bits needed to make the column_representation
STATE_BITS = COLUMN_BITS * COLUMNS  # state_bits are the number of bits needed to represent a state in binary

CELL_SIZE = 120

MINIMAX = "Minimax"
MINIMAX_PRUNE = "Pruning"
EXPECTI = "Expecti"

WIDTH = COLUMNS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
ONE_END_OPEN_BIAS = 0.5

EMPTY = 0
HUMAN = 1
AI = 2

FOURS_BIAS = 8
THREES_BIAS = 4
CENTER_BIAS = 4
ADJACENT_BIAS = 4
SCORE_BIAS = 500
