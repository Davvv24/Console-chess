class DrawTool:
    def __init__(self,board_position=None):
        if board_position is None: # default board
            self.board_position = [[col for col in row] for row in CHESS_BOARD] # copies default starting board
        else:
            try:
                if len(board_position)==8 and len(board_position[0])==8:
                    self.board_position = board_position
            except:
                IndexError("Invalid board passed. ,m")
        self.symbol_map = self.piece_to_symbol() #dictionary to convert pieces to symbols

    # ! Don't use this because a lot of move checking requires the normal characters
    # Only needed to fetch custom symbols 
    def piece_to_symbol(self): 
        # symbols=['♔','♕','♖','♗','♘','♙','♚','♛','♜','♝','♞','♟']
        pieces=['K','Q','R','B','N','P','k','q','r','b','n','p','X']
        symbols = pieces
        d=dict()
        for i in range(12):
            d[pieces[i]]=symbols[i]+' '
        return d
    
    # Takes in a board as a list and draws it in the console 
    # symbol_mapping is an optional array containing custom symbols to use instead of letters
    def draw_board(self,board_position,symbol_mapping=None):
        # default paramter is attribute
        if symbol_mapping is None: # Fetch stored symbols 
            symbol_mapping = self.symbol_map
        # Actual rendering 
        if len(board_position)==8 and len(board_position[0])==8:
            print("\n"*6)
            row_length=len(board_position[0])
            col_length=len(board_position)
            for i in 'abcdefgh':
                print(' ',i,end='')
            print('')
            print('',' __'*(col_length))
            for i in range(row_length):
                print(8-i,end='')
                print('|',end='')
                for j in range(col_length):
                    if board_position[i][j]=='':
                        print('  ',end='|')
                    else:
                        print(board_position[i][j],'',end='|')
                print()
            print('',' --'*(col_length))
            for i in 'abcdefgh':
                print(' ',i,end='')
        else:
            print("Invalid board size.")
        
        
CHESS_BOARD=[   ['r','n','b','q','k','b','n','r'],
                ['p','p','p','p','p','p','p','p'],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['P','P','P','P','P','P','P','P'],
                ['R','N','B','Q','K','B','N','R']]    


if __name__ == "__main__":
    board_position=[   
                ['r','n','b','q','k','b','n','r'],
                ['p','p','p','p','p','p','p','p'],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['P','P','P','P','P','P','P','P'],
                ['R','N','B','Q','K','B','N','R']]    
    chess = DrawTool(board_position)
    chess.draw_board()
