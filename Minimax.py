from constants import AI, HUMAN
from BoardState import BoardState
import math

class Minimax:
  def __init__(self, mode) -> None:
    self.mode = mode
    
    self.alpha = None
    self.beta = None

  def run(self, state : BoardState, depth, player):
    neighbors = state.get_neighbors(player) 

    if state.is_terminal() or depth == 0:
      if state.is_terminal():
        return state.get_score(player)
      elif depth == 0:
        return state.get_heuristic(player)
    
    if player == AI: # Maximizer
      value = -math.inf
      for neighbor in neighbors:
        value = max(value, self.run(neighbor, depth-1, HUMAN))
        return value
      
    elif player == HUMAN: ## Minimizer
      value = math.inf
      for neighbor in neighbors:
        value = min(value, self.run(neighbor, depth-1, AI))
        return value
    