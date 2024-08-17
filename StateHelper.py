import numpy as np
from constants import EMPTY, RED, YELLOW

class StateHelper:
  @staticmethod
  def getValidSpace(state: np.ndarray, col: int) -> int | None:
    for row in range(state.shape[0]-1, -1, -1):  # Start from the bottom row
      if state[row, col] == EMPTY:
          return row
    return None  # Column is full
  
  @staticmethod
  def insert(state: np.ndarray, col: int, value: int) -> bool:
    if value not in [1, 2]:
      raise ValueError("Invalid value. Must be 1 (RED) or 2 (YELLOW).")

    valid_row = StateHelper.getValidSpace(state, col)
    if valid_row is not None:
      state[valid_row, col] = value
    else:
      print("Invalid Move")
    return state  # No valid space in the column, move is invalid