from constants import AI, HUMAN
from BoardState import BoardState
import math
import random

class Minimax:
  def __init__(self, mode, maximizer) -> None:
    self.mode = mode
    self.maximizer = maximizer

    self.alpha = None
    self.beta = None 

  def run(self, state : BoardState, depth, player):
    # print(state)
    neighbors = state.get_neighbors(player) 
    cols = [neighbor[0] for neighbor in neighbors]
    # print("Running minimax")
    if state.is_terminal() or depth == 0:
      if state.is_terminal():
        return (None, state.get_score(player))
      elif depth == 0:
        return (None, state.get_heuristic(player))
    
    if player == self.maximizer: # Maximizer
      value = -math.inf
      column = random.choice(cols)
      for col, neighbor in neighbors:
        new_score = self.run(neighbor, depth-1, HUMAN)[1]
        if new_score > value:
          value  = new_score
          column = col
      return (column, value)
      
    else: ## Minimizer
      value = math.inf
      column = random.choice(cols)
      for col, neighbor in neighbors:
        new_score = self.run(neighbor, depth-1, AI)[1]
        if new_score < value:
          value  = new_score
          column = col
      return (column, value)
    