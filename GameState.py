import numpy as np
from constants import EMPTY, RED, YELLOW, COLUMNS, ROWS

class GameState:
  def __init__(self, state: np.ndarray, id : int = None):
    self.state = state
    self.score = self.get_heuristic()
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
            return GameState(new_state)
      
    raise ValueError("Invalid Move")

  def get_neighbors(self, player: int):
    neighbors = []
    possible_moves = self.get_possible_moves()

    for col in possible_moves:
        next_state = self.insert(col, player)
        neighbors.append(next_state)

    return neighbors
  
  def get_heuristic(self):
    pass

  def __getConnected4s(state):
    pass 
  
  def __getConnected3s(state):
    pass 
  
  def __getCenterDistribution(state):
    pass

  def __repr__(self) -> str:
    return str(self.state)