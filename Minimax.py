from constants import AI, HUMAN, SCORE_BIAS
from BoardState import BoardState
import math
import random

class Minimax:
  def __init__(self, mode, maximizer) -> None:
    self.mode = mode
    self.maximizer = maximizer
    self.minimizer = 1 if maximizer == 2 else 2

    self.alpha = None
    self.beta = None 

  def run(self, state : BoardState, depth, player):
    # print(state)
    neighbors = state.get_neighbors(player) 
    cols = [neighbor[0] for neighbor in neighbors]
    # print("Running minimax")
    if state.is_terminal() or depth == 0:
      if state.is_terminal():
        return (None, state.get_score(self.maximizer, self.minimizer) * SCORE_BIAS)
      elif depth == 0:
        return (None, state.get_heuristic(self.maximizer, self.minimizer))
    
    if player == self.maximizer: # Maximizer
      value = -math.inf
      column = random.choice(cols)
      for col, neighbor in neighbors:
        new_score = self.run(neighbor, depth-1, self.minimizer)[1]
        if new_score > value:
          value  = new_score
          column = col
      return (column, value)
      
    else: ## Minimizer
      value = math.inf
      column = random.choice(cols)
      for col, neighbor in neighbors:
        new_score = self.run(neighbor, depth-1, self.maximizer)[1]
        if new_score < value:
          value  = new_score
          column = col
      return (column, value)
    