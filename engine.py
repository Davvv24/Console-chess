import math
from board import Board, arr_copy
from logic import Logic


# TODO: implement entire engine 
# TODO: create node class from basic python 

# Evaluation points for game start, middle game, and late game
START_EVAL = {'':0,'p':-0.8,'P':0.8,'n':-3.05,'N':3.05,'b':-3.33,'B':3.33,'r':-5.63,'R':5.63,'q':-9.5,'Q':9.5,'k':-100,'K':100} # ? King eval might not be needed 
MID_EVAL = {'':0,'p':-0.8,'P':0.8,'n':-3.05,'N':3.05,'b':-3.33,'B':3.33,'r':-5.63,'R':5.63,'q':-9.5,'Q':9.5,'k':-100,'K':100} # ! don't forget to change these
END_EVAL = {'':0,'p':-0.8,'P':0.8,'n':-3.05,'N':3.05,'b':-3.33,'B':3.33,'r':-5.63,'R':5.63,'q':-9.5,'Q':9.5,'k':-100,'K':100}

class Node:
    def __init__(self,parent,board:Board,root=False) -> None:
        if root:
            self.parent = None # Orphan
        else: self.parent = parent
        self.board = board
        self.children = []
        
def add_child(parent:Node, child:Node):
    parent.children.append(child)
    
def expand_leaf_node(board:Board, node:Node, white:bool):
        board_position = board.board_position
        # Get all playable moves from the current position, creating a board position for each. Assign each position to to a new child and continue until the recursion ends
        moves = []
        it = range(len(board_position))
        for i in it:
            for j in it:
                piece = board_position[i][j]
                if piece != '':
                    logic = Logic()
                    moves += ((i,j),logic.get_piece_moves(piece.upper(), board, (i,j), white)) # append all the new moves found
        
        for move in moves:
            board.move(move[0],move[1]) # Create a new position
            new_board = Board(board_position) # Create a new board object with the position just obtained
            board.undo() # Undo to reuse previous position
            new_node = Node(parent=node,board=board)
            add_child(node, new_node)

    
class Engine:
    def __init__(self) -> None:
       self.minmax = Minmax()
       self.max_depth = 5
       pass 
    
    def board_eval(self, board_position, turn): # This is really rough and basic but it's a start 
        eval += 0
        for row in board_position:
            for piece in row:
                if turn < 15:
                    eval += START_EVAL[piece]   # ! This works under the assumption each game runs on a similar n. of moves. 
                elif turn < 30:                 # ! Better approximations should be implemented 
                    eval += MID_EVAL[piece]
                else:
                    eval += END_EVAL[piece]
                
    def best_move(self, board:Board, white:bool, turn:int): # TODO: test this thing
        board_position = board.board_position
        root_node = Node([],board,True)
        board_position = board.board_position
        # Get all playable moves from the current position, creating a board position for each. Assign each position to to a new child and continue until the recursion ends
        moves = []
        it = range(len(board_position))
        for i in it:
            for j in it:
                piece = board_position[i][j]
                if piece != '':
                    logic = Logic()
                    moves += ((i,j),logic.get_piece_moves(piece.upper(), board, (i,j), white)) # append all the new moves found
        evals = []
        for move in moves:
            board.move(move[0],move[1]) # Create a new position
            new_board = Board(board_position) # Create a new board object with the position just obtained
            board.undo() # Undo to reuse previous position
            new_node = Node(parent=root_node,board=board)
            add_child(root_node, new_node)
            eval = self.minmax(self, new_node, self.max_depth, 1000000, -1000000, white, turn)
            evals.append(eval)
        max, max_index = 0
        for i in range(len(evals)):
            if evals[i] > max:
                max = evals[i]
                max_index = i
        return move[max_index]
        

class Minmax:
    def __init__(self) -> None:
        self.loop = 0
        pass
    
    # Minmax no pruning
    def minmax_np(self, node: Node, depth: int, maximise: bool) -> int:
        self.loop+=1
        # Bottom layer condition
        if depth == 0:
            return node.name
        
        if maximise == True:
            best_eval = -100000
            for child in node.children:
                move_eval = self.minmax_np(child, depth-1, False)
                if move_eval > best_eval:
                    best_eval = move_eval
            node.name = best_eval
            return best_eval
            
        else:
            worst_eval = 100000
            for child in node.children:
                move_eval = self.minmax_np(child, depth-1, True)
                if move_eval < worst_eval:
                    worst_eval = move_eval
            node.name = worst_eval
            return worst_eval
    
    # Recursive algorithm that at depth 0 returns the node eval and on the final iteration returns the root node's eval
    def minmax(self, node: Node, depth: int, alpha: int, beta: int, maximise: bool, turn: int) -> float: # maximise is equivalent to white
        board = node.board # Get the board and position for the current node
        board_position = board.board_position
        best_eval = -100000
        worst_eval = 100000
        self.loop+=1
        if depth == 0:
            eval = self.eval(node.board_position,turn) # TODO: fix this
            return eval
        
        expand_leaf_node(board, node, maximise)
        
        if maximise == True:
            for child in node.children:
                temp = board
                eval = self.minmax(child, depth-1, alpha, beta, False, turn)
                if eval > best_eval:
                    best_eval = eval
                if eval > alpha:
                    alpha = eval
                if alpha > beta:
                    return 100000
            node.name = best_eval
            return best_eval
            
        else:
            for child in node.children:
                eval = self.minmax(child, depth-1, alpha, beta, True, turn)
                if eval < worst_eval:
                    worst_eval = eval
                if eval < beta:
                    beta = eval
                if alpha > beta:
                        return -100000
            node.name = worst_eval
            return worst_eval