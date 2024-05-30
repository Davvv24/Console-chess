# Main file to run to start chess
from board import Board
from draw import DrawTool
# from engine import Engine
from logic import *


class ChessGame:
    # Game variables 
    def __init__(self):
        self.board = Board()
        self.draw = DrawTool(self.board.board_position)
        self.logic = Logic()
        # self.engine = Engine()
        self.turn = 1 
        self.moves = []
        self.game_end = False
        self.white_castled = False
        self.black_castled = False # TODO: Use these later 
        

    # TODO: check this code still holds after changes are made 
    # ! promotions not implemented
    # ! castling not implemented
    # ! en passant not implemented
    # ! check not implemented
    def validate_move(self): # potentially add checking for infinite loops to prevent errors
        white = bool(self.turn%2)
        validated = False
        move = ""
        # Creating validate a move
        while not validated: # Validate input until correct
            move=input('Enter valid move: ')
            try:
                coords = self.logic.validate_syntax(self.board,move,white=white) # Get start and end coordinates of move
            except ValueError as e: # TODO: this solution is slightly brute forced, improvements could be made
                coord = (-1)
            if coords != (-1):
                piece = self.board.board_position[coords[0][0]][coords[0][1]] # Fetch piece
                moves = self.logic.get_piece_moves(piece,self.board,coords[0],white) # Pass coordinates of piece to get its moves 
                if coords[1] in moves:
                    validated = True
                else: 
                    print("\nInvalid move.") # TODO: add more descriptive messages 
            else: 
                print("\nInvalid syntax.")
        self.moves.append(move) # Save the move played 
        return coords   
        

    def update_game(self, move_coords):
        white = bool(self.turn%2)
        ## Update the game state here
        # ? check if the game is over
        # ? check if the king is in check
        # ? check if the move puts the king in check
        self.board.move(move_coords[0], move_coords[1])
        self.turn+=1
        if self.logic.is_black_check(self.board):
            print("Black king in check.")
        if self.logic.is_white_check(self.board):
            print("White king in check.")

    # Method to render board at the end of each turn  
    def render_game(self):
        self.draw.draw_board(self.board.board_position)
        print()

    # TODO: fix game loop
    # Primary game loop. Everything is handled here
    def game_loop(self):
        while not self.game_end:
            white = bool(self.turn%2)
            if white: 
                move_coords = self.validate_move() # Get a move from the player, check the syntax is correct and validate it 
            else: 
                move_coords = self.engine.best_move(self.board, white)
            self.update_game(move_coords) # handle updates such as game end, check, turn increment
            self.render_game() # Update the game
        print("Game ended.")

# Start game
# if __name__ == "__main__":
#     game = ChessGame()
#     game.game_loop()


game = ChessGame()
game.game_loop()