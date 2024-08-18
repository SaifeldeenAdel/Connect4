from constants import MAX_BITS_PER_STATE, COLUMNS, ROWS, NUM_BITS_PER_COLUMN
import numpy as np


class InternalState:

    def __init__(self, decimal_state: int):
        self.__decimal_state = decimal_state

    def get_binary_state(self) -> str:
        binary_state = bin(self.__decimal_state)[2:]
        binary_state = '0' * (MAX_BITS_PER_STATE - len(binary_state)) + binary_state
        return binary_state

    def get_decimal_state(self) -> int:
        return self.__decimal_state

    def get_numpy_format(self) -> np.ndarray:
        #  0 in array -> EMPTY
        #  1 in array -> player 1 -> RED
        #  2 in array -> player 2 -> YELLOW
        #  BINARY 0 -> RED
        #  BINARY 1 -> YELLOW
        binary_state = self.get_binary_state()
        nparray = np.zeros((ROWS, COLUMNS))
        # print(nparray)
        num_occupied = NUM_BITS_PER_COLUMN - ROWS

        for col in range(COLUMNS):
            print(f"column {col}")
            start = col * NUM_BITS_PER_COLUMN
            end = start + NUM_BITS_PER_COLUMN
            print(f"start {start} and end {end}")
            column_representation = binary_state[start: end]
            print(f"column representation {column_representation}")
            num_rows_occupied = int(column_representation[:num_occupied], 2)
            print(f"num_rows_occupied {num_rows_occupied}")
            disks = column_representation[num_occupied:]
            disks = column_representation[-num_rows_occupied:]
            print(f"disks {disks}")
            i = 0
            start_row = ROWS - 1
            end_row = start_row - num_rows_occupied
            for row in range(start_row, end_row, -1):  # 0,0 is top left, we start bottom left
                #                   RED                     Yellow
                nparray[row, col] = 1 if disks[i] == '1' else 2
                i += 1
        return nparray


# binary_string = '010 000000 100 000001 001 000001 100 001110 011 000001 001 000001 000 000000'
binary_string = '010 000000 100 000001 001 000001 100 001110 011 000001 001 000001 000 000000'
decimal_number = int(binary_string.replace(" ", ""), 2)

b = InternalState(decimal_number)
print(b.get_numpy_format())
