from constants import AI, HUMAN, SCORE_BIAS
from BoardState import BoardState
import math
import random
from treelib import Tree
import pydot_ng as pd

class A_B_pruning:
    def __init__(self, mode, depth, maximizer) -> None:
        self.mode = mode
        self.maximizer = maximizer
        self.minimizer = 1 if maximizer == 2 else 2
        self.max_depth = depth
        self.nodes = []
        self.alpha = -math.inf
        self.beta = math.inf 
    
    def run(self, state : BoardState, depth, player):
        alpha = self.alpha
        beta = self.beta
        if player == self.maximizer:
            return self.max_value(state, depth, alpha, beta)
        else:   
            return self.min_value(state, depth, alpha, beta)
    
    def max_value(self, state, depth, alpha, beta):
        if state.is_terminal() or depth == 0:
            if state.is_terminal():
                score =  state.get_score(self.maximizer, self.minimizer) * SCORE_BIAS
            elif depth == 0:
                score =  state.get_heuristic(self.maximizer, self.minimizer)
            self.nodes.append((state.get_id(), score, depth))
            return (None, score)
        value = -math.inf
        column = None
        for col, neighbor in state.get_neighbors(self.maximizer):
            new_score = self.min_value(neighbor, depth-1, alpha, beta)[1]
            if new_score > value:
                value  = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        self.nodes.append((state.get_id(), value, depth))
        return (column, value)
    
    def min_value(self, state, depth, alpha, beta):
        if state.is_terminal() or depth == 0:
            if state.is_terminal():
                score =  state.get_score(self.maximizer, self.minimizer) * SCORE_BIAS
            elif depth == 0:
                score =  state.get_heuristic(self.maximizer, self.minimizer)
            self.nodes.append((state.get_id(), score, depth))
            return (None, score)
        value = math.inf
        column = None
        for col, neighbor in state.get_neighbors(self.minimizer):
            new_score = self.max_value(neighbor, depth-1, alpha, beta)[1]
            if new_score < value:
                value  = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        self.nodes.append((state.get_id(), value, depth))
        return (column, value)
