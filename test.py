from BoardState import BoardState
import numpy as np
from A_B_pruning import A_B_pruning

def test_8139(state, player):
  state = BoardState.list_to_boardstate(state)
  col, score = A_B_pruning.get_instance().run(state, depth=5, player=player)

  return col
