#probability that disc falls in chosen position is 0.6 and 0.2 each for left and right

from constants import AI, HUMAN, SCORE_BIAS
from BoardState import BoardState
import math
import random
from treelib import Tree
import pydot_ng as pd

class Expecti:
    def __init__(self, mode, depth, maximizer) -> None:
        self.mode = mode
        self.maximizer = maximizer
        self.minimizer = 1 if maximizer == 2 else 2
        self.max_depth = depth
        self.nodes = []
        
    def run(self, state : BoardState, depth, player):
        if player == self.maximizer:
            return self.max_value(state, depth)
        else:   
            return self.min_value(state, depth)
    
    def max_value(self, state, depth):
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
            new_score = self.expecti_value(neighbor, depth-1)[1]
            if new_score > value:
                value  = new_score
                column = col
        self.nodes.append((state.get_id(), value, depth))
        return (column, value)
    
    def min_value(self, state, depth):
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
            new_score = self.expecti_value(neighbor, depth-1)[1]
            if new_score < value:
                value  = new_score
                column = col
        self.nodes.append((state.get_id(), value, depth))
        return (column, value)
    
    def expecti_value(self, state, depth):
        if state.is_terminal() or depth == 0:
            if state.is_terminal():
                score =  state.get_score(self.maximizer, self.minimizer) * SCORE_BIAS
            elif depth == 0:
                score =  state.get_heuristic(self.maximizer, self.minimizer)
            self.nodes.append((state.get_id(), score, depth))
            return (None, score)
        value = 0
        column = None
        for col, neighbor in state.get_neighbors(self.maximizer):
            new_score = self.min_value(neighbor, depth-1)[1]
            value += 0.6 * new_score
        for col, neighbor in state.get_neighbors(self.minimizer):
            new_score = self.max_value(neighbor, depth-1)[1]
            value += 0.2 * new_score
        self.nodes.append((state.get_id(), value, depth))
        return (column, value)
    
    def draw_tree(self):
        nodes = list(reversed(self.nodes))
        tree = Tree(   )

        parent_ids = [(nodes[0][0],nodes[0][2])]
        tree.create_node(nodes[0][1], nodes[0][0]   )

        for id, value, depth in nodes[1:]:
          if depth < parent_ids[-1][1]:
            tree.create_node(value, id, parent=parent_ids[-1][0])
            parent_ids.append((id, depth))
          elif depth == parent_ids[-1][1]   :

            tree.create_node(value, id, parent=parent_ids[-2][0])
          elif depth > parent_ids[-1][1]:
            while parent_ids and parent_ids[-1][1] <= depth:
              parent_ids.pop(   )

            tree.create_node(value, id, parent=parent_ids[-1][0])
            parent_ids.append((id, depth))

        print(tree.show(stdout=False))
        self.tree = tree

    def get_number_nodes(self):
        return len(self.nodes)

    def reset_nodes(self):
        self.nodes = [   ]
  
    def tree_svg(self):
        self.tree.to_graphviz("minimax.dot")
        dot = pd.graph_from_dot_file("minimax.dot")
        filename = "minimax.svg"
        dot.write_svg(filename)   
  

