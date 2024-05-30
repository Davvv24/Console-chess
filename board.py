import random

CHESS_BOARD = [ ['r','n','b','q','k','b','n','r'],
                ['p','p','p','p','p','p','p','p'],
                [ '', '', '', '', '', '', '', ''],
                [ '', '', '', '', '', '', '', ''],
                [ '', '', '', '', '', '', '', ''],
                [ '', '', '', '', '', '', '', ''],
                ['P','P','P','P','P','P','P','P'],
                ['R','N','B','Q','K','B','N','R']] # index 7 / row 1 in chess
# To copy an array without the Python copy module
def arr_copy(arr):
    return [[col for col in row] for row in arr]

def arr_copy(arr):
    return [[col for col in row] for row in arr]

# Board class containing a board array, methods to move pieces on the board, methods for piece coordinates, and useful conversions
class Board:
    board_position=[]
    def __init__(self, board_position=None): # construct a board object with a starting board position
        if board_position is None:
            self.board_position = arr_copy(CHESS_BOARD) # Copies default starting board 
            self.previous_position = [arr_copy(CHESS_BOARD)]
        else:
            self.board_position = arr_copy(board_position) 
            self.previous_position = [arr_copy(board_position)]
    def setboard(self,board): # set the board to a given list
        self.previous_position.append(arr_copy(self.board_position))
        self.board_position = arr_copy(board)
    
    # TODO: force changes to be logged to that undo works properly                                 
    def undo(self):
        self.board_position = self.previous_position.pop()
        
    
    # Converts a square to a coordinate on the board (eg. c1 corresponds to (6, 2))
    def sq_coord(self, square:str): 
        if len(square)==2 and square[0] in 'abcdefgh' and square[1] in '87654321':
            coord = ('87654321'.index(square[1]),'abcdefgh'.index(square[0]))
            return coord
        else: raise ValueError("Invalid square.")
 
    # Move a piece on a square to another square (with coordinates), capturing if the square is occupied 
    # Coordinates required
    def move(self, start_square, end_square): # TODO: test this function
        if isinstance(start_square,str) or isinstance(end_square, str):
            raise TypeError("'move' method requires coordinates. Use sq_coord for conversion.")
        self.previous_position.append(arr_copy(self.board_position)) # Push position onto stack
        y0, x0 = start_square  # Get coordinates
        piece = self.board_position[y0][x0] # Fetches piece
        if piece is "":
            raise ValueError("Can't move empty piece.")
        y1, x1 = end_square
        self.board_position[y0][x0] = "" # Clears previous square
        self.board_position[y1][x1] = piece # Sets the new square to the piece 
    
    # TODO: test castling 
    # This will place the king and the rook in castled positions without doing validation
    def castle(self, white=True, a_side=True): # a_side determines if the castling is happening nearer to the a-file
        self.previous_position.append(arr_copy(self.board_position)) # Push position onto stack
        if white:
            if a_side:
                self.board_position[7][2] = "K" # TODO: adjust for custom characters
                self.board_position[7][3] = "R"
                self.board_position[7][0], self.board_position[7][4] = ""
            else:
                self.board_position[7][6] = "K"
                self.board_position[7][5] = "R"
                self.board_position[7][7], self.board_position[7][4] = "",""
        else:
            if a_side:
                self.board_position[0][2] = "k"
                self.board_position[0][3] = "r"
                self.board_position[0][0], self.board_position[0][4] = ""
            else:
                self.board_position[0][6] = "k"
                self.board_position[0][5] = "r"
                self.board_position[0][7], self.board_position[0][4] = "",""
             
             
    def en_passant(self): #TODO: impement en passant
        self.previous_position.append(arr_copy(self.board_position))
        return       
        
    # Returns the x,y coordinate of the piece searched, incuding the option of searching within a file or a row
    # An error is raised if it is not found 
    # If any piece is wanted (eg. any pawn), the location of every piece of that type is returned
    def piece_coord(self, piece:str,row=None,file=None,any=False): # ! A better way to deal with multiple pieces needs to be implemented 
        if piece=="":
            raise ValueError("Can't search empty piece.")
        if row is not None and file is not None:
            raise ValueError("Can't search within file and row at the same time.")
        elif row is not None: # Type checking for row if row chosen
            if isinstance(row, int) and row>=0 and row<8:
                return (row, self.board_position[row].index(piece)) # Search within a row
            else: raise ValueError("Row must be an index.")
        elif file is not None: # Type checking for file if file chosen
            if isinstance(file, int) and file>=0 and file<8:
                for r in range(8): # Search within a file/column returning the first found
                    if self.board_position[r][file] == piece:
                        return (r, file) 
                raise ValueError("Piece: "+ piece + " not found.") # ? possibly add checking for opposite colour pieces, to indicate that it might be the wrong turn
            else: raise ValueError("File must be an index.")
        else:   # Normal search
            pos = []
            it = range(len(self.board_position))
            for i in it:
                for j in it:
                    x = self.board_position[i][j]
                    if piece == x:
                        if any:
                            pos.append((i,j))
                            return pos
                        else: return (i,j)
            return pos
        
        
    # ! not needed but can be added later  
    # def shuffle(arr): # Not needed 
    #     new_arr = []
    #     for i in range(len(arr)):
    #         new_arr.append(arr.pop(random.randint(0,len(arr)-1)))
    #     return new_arr
        

    # def randomize_board_dirty(self): also not needed 
    #     #dirty randomization (no checks for valid positions or if the king is in check)
    #     arr=self.board_position
    #     arr = arr.flatten()
    #     arr = self.shuffle(arr)
    #     arr = arr.reshape((8, 8))
    #     self.board_position=arr

    # Takes a string of fen and decodes it into an array
    def fen_to_matrix(self,fen):
        fen = fen.split(' ')[0]
        fen = fen.split('/')
        board = [['']*8 for i in range(8)]
        for i in range(8):
            j = 0
            for k in fen[i]:
                if k.isdigit():
                    j += int(k)
                else:
                    board[i][j] = k
                    j += 1
        return board

    # Converts any list to a fen string
    def matrix_to_fen(self,matrix,display=False):
        fen = ''
        for i in range(8):
            j = 0
            for k in matrix[i]:
                if k == '':
                    j += 1
                else:
                    if j > 0:
                        fen += str(j)
                        j = 0
                    fen += k
            if j > 0:
                fen += str(j)
            if i < 7:
                fen += '/'
        if display:
            print(fen)
        return fen

    # Convert a pgn into a list of string moves
    def pgn_to_moves(self,pgn): # move to utils 
        pgn = pgn.split(' ')
        moves = []
        for i in pgn:
            if '.' in i:
                continue
            moves.append(i)
        return moves

    # ! might be better to implement this in the logic
    # def pawn_move(self,board,move,turn): ## move to game/piece module	
    #     pawns=['a','b','c','d','e','f','g','h']
    #     if move[0].low() in pawns:
    #         if turn==0:
    #             board[8-int(move[1]),pawns.index(move[0])]='P'
    #         else:
    #             board[8-int(move[1]),pawns.index(move[0])]='p'    

    # def move_pawn(self,board,coordinate): ## move to game/piece module
    #     l,c=coordinate
    #     if l==1:
    #         board[l,c]=''
    #         board[l+2,c]='P'
    #     else:
    #         board[l,c]=''
    #         board[l-2,c]='p'
    #     return board

if __name__=='__main__':
    board=Board()
    # fen test
    fen="q3kb1r/1p2pppp/5n2/2rp4/3Q1B2/4PN2/P1n2PPP/R3K2R w KQk - 0 14"
    newboard=board.fen_to_matrix(fen)
    # set board tests
    board.setboard(newboard)
    board.matrix_to_fen(board.board_position,display=True)
    # pgn test
    pgn="e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 O-O c3 d5 exd5 Nxd5 Nxe5 Nxe5 Rxe5 c6 d4 Bd6 Re1 Qh4 g3 Qh3 Be3 Bg4 Qd3 Rae8 Nd2 Re6 a4 Qh5 axb5 axb5 Bxd5 cxd5 Qxb5 Rb8 Qa5 Rxb2 Qd8+ Bf8 Ra8 h6 Qxf8+ Kh7 Qh8+ Kg6 Rg8 Rxe3 Qxg7+ Kf5 Qxf7#"
    print(board.pgn_to_moves(pgn))
    import draw
    draw_tool = draw.DrawTool(board.board_position)
    d = lambda: draw_tool.draw_board(board.board_position) # just shorter
    d()
    board.move((0,0), (0,1))
    d()
    board.move((0,1), (0,5))
    d()
    board.castle(a_side=False)
    d()
    # Get piece coordinates by row, file or generic search 
    coords = {"p":board.piece_coord("p"),"K":board.piece_coord("K"),"n":board.piece_coord("n",row=6),"P":board.piece_coord("P",file=5)}
    print()
    print(coords)