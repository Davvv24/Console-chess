from board import Board, arr_copy
import draw 

# TODO: implement each move checking 

# ! The coordinates are flipped for the board, as the board is stored row by row rather than file by file
# ! This means the top left corner is (0,0) and the bottom right is (7,7)
# ! So (x,y) = board_position[y][x] 

# position is the current board state in any of the available moves functions 
def rook_moves(position, coordinate, white=True, show=False)->list: # TODO: test rook moves 
    if not isinstance(white, bool):
        raise TypeError("White/black must be a boolean.")
    row = position[coordinate[0]]
    file = [row[coordinate[1]] for row in position]
    y,x = coordinate
    moves = []
    piece  = ""
    # ! I'll need to check if any rook move leads to a check, returning an empty array if so  
    for direction in [-1,1]: 
        for r in range(1*direction,8*direction,direction): # Iterate upwards or downwards depending on the direction
            k = y+r 
            if k<0 or k>7: # Prevent index errors
                break
            piece = file[k]
            if piece == "":
                if show: # To show available moves 
                    position[7-x][k] = "X"
                moves.append((k,x))
            elif white: 
                if piece.islower(): # Take black piece as white
                    moves.append((k,x))
                    break
                else: break # Stop at white piece as white
            else:
                if piece.isupper(): # Take white piece as black
                    moves.append((k,x)) 
                    break
                else: break # Stop at black piece as black
        for r in range(1*direction,8*direction,direction): # Iterate left or right depending on the direction
            k = x+r 
            if k<0 or k>7: # Prevent index errors
                break
            piece = row[k]
            if piece == "":
                if show: # To show available moves 
                    position[7-x][k] = "X"
                moves.append((y,k))
            elif white: 
                if piece.islower():
                    moves.append((y,k))
                    break
                else: break
            else:
                if piece.isupper():
                    moves.append((y,k))
                    break
                else: break
    return moves
            
# TODO: implement en passan and promotion and starting moves
def pawn_moves(position, coordinate, white=True, show=False)->list:
    moves = []
    y,x = coordinate # Row and file
    direction = 1
    if not white:
        direction = -1
    if y<1 and white or y>6 and not white: 
        raise ValueError("Pawns can't be on the first or last row without getting promoted.")
    if white and y==6 and position[5][x]=='' and position[4][x]=='': # Starting moves
        moves.append((4,x))
    elif not white and y==1 and position[2][x]=='' and position[3][x]=='':
        moves.append((3,x))
    for j in [-1,0,1]:
        k = x+j
        if k<0 or k>7: # Prevent index errors
            pass
        else:
            piece = position[y-direction][k]
            if piece == "" and j==0:
                if show: # To show available moves 
                    position[y-direction][k] = "X"
                moves.append((y-direction,k))
            elif white: 
                if piece.islower() and j!=0:
                    moves.append((y-direction,k))
            else:
                if piece.isupper() and j!=0:
                    moves.append((y-direction,k))
    return moves 

def knight_moves(position, coordinate, white=True, show=False)->list:
    if not isinstance(white, bool):
        raise TypeError("White/black must be a boolean.")
    x,y = coordinate
    moves = []
    piece  = ""
    for up in [-1,1]:
        for right in [-2,-1,1,2]:
            j = x + right
            k = y+up if abs(right)==2 else y+up*2
            if j<0 or j>7 or k<0 or k>7: # Prevent index errors
                pass
            else:
                piece = position[j][k] 
                if piece == "":
                    if show: # To show available moves 
                        position[j][k] = "X"
                    moves.append((j,k))
                elif white: 
                    if piece.islower():
                        moves.append((j,k))
                else:
                    if piece.isupper():
                        moves.append((j,k))
    return moves 

def bishop_moves(position, coordinate, white=True, show=False)->list:
    if not isinstance(white, bool):
        raise TypeError("White/black must be a boolean.")   
    y,x = coordinate
    moves = []
    piece  = ""
    for direction in [-1,1]:
        for r in range(1*direction,8*direction,direction): # Iterate upwards or downwards along the \ diagonal depending on the direction
            j = y+r
            k = x+r 
            if j<0 or j>7 or k<0 or k>7: # Prevent index errors
                break
            piece = position[j][k]
            if piece == "":
                if show: # To show available moves 
                    position[j][k] = "X"
                moves.append((j,k))
            elif white: 
                if piece.islower(): # Take black piece as white
                    moves.append((j,k))
                    break
                else: break # Stop at white piece as white
            else:
                if piece.isupper(): # Take white piece as black
                    moves.append((j,k)) 
                    break
                else: break # Stop at black piece as black
        for r in range(1*direction,8*direction,direction): # Iterate upwards or downwards along the / diagonal depending on the direction
            j = y+r
            k = x-r 
            if j<0 or j>7 or k<0 or k>7: # Prevent index errors
                break
            piece = position[j][k]
            if piece == "":
                if show: # To show available moves 
                    position[j][k] = "X"
                moves.append((j,k))
            elif white: 
                if piece.islower(): # Take black piece as white
                    moves.append((j,k))
                    break
                else: break # Stop at white piece as white
            else:
                if piece.isupper(): # Take white piece as black
                    moves.append((j,k)) 
                    break
                else: break # Stop at black piece as black
    return moves 
     
# ! king moves require additional checking. This will need to be added after check checking is implemented  
def king_moves(position, coordinate, white=True, show=False)->list:
    if not isinstance(white, bool):
        raise TypeError("White/black must be a boolean.")
    moves = []
    x,y = coordinate
    for up in [-1,0,1]:
        for right in [-1,0,1]:
            if up==0 and right==0: pass
            else:
                j = x+up
                k = y+right
                if j<0 or j>7 or k<0 or k>7: # Prevent index errors
                    pass
                else:
                    piece = position[j][k] # TODO: to avoid repeated code, make this a callable function
                    if piece == "":
                        if show: # To show available moves 
                            position[j][k] = "X"
                        moves.append((j,k))
                    elif white: 
                        if piece.islower():
                            moves.append((j,k))
                    else:
                        if piece.isupper():
                            moves.append((j,k))
    return moves     
    
# Lazy solution but it works 
def queen_moves(position, coordinate, white=True, show=False)->list:
    moves = rook_moves(position, coordinate, white, show)
    moves += bishop_moves(position, coordinate, white, show)
    return moves

class Logic:
    def __init__(self):
        pass
    
    # Returns an array with coordinates of valid moves available for a given piece   
    def get_piece_moves(self,piece:str,board:Board,coordinate:tuple,white:bool,strict=True)->list: # Strict ensures that no moves that lead to checks are able to be played
        position = board.board_position
        if piece is "":
            raise ValueError("Can't get moves of empty piece.")
        piece = piece.upper()
        valid_moves = []
        # match piece:
        #     case "P":
        #         valid_moves = pawn_moves(position, coordinate, white)
        #     case "R":
        #         valid_moves = rook_moves(position, coordinate, white)
        #     case "N":
        #         valid_moves = knight_moves(position, coordinate, white) 
        #     case "B":
        #         valid_moves = bishop_moves(position, coordinate, white) 
        #     case "K":
        #         valid_moves = king_moves(position, coordinate, white) 
        #     case "Q":
        #         valid_moves = queen_moves(position, coordinate, white)
        if piece == "P":
            valid_moves = pawn_moves(position, coordinate, white)
        elif piece == "R":
            valid_moves = rook_moves(position, coordinate, white)
        elif piece == "N":
            valid_moves = knight_moves(position, coordinate, white) 
        elif piece == "B":
            valid_moves = bishop_moves(position, coordinate, white) 
        elif piece == "K":
            valid_moves = king_moves(position, coordinate, white) 
        elif piece == "Q":
            valid_moves = queen_moves(position, coordinate, white)
        else: raise ValueError("Invalid piece given.")
             
        if strict: # Remove moves leading to the king being taken
            temp = []
            for move_coord in valid_moves: # Check for checks
                temp_board = Board(board_position=position) # Create a position where the move is played
                temp_board.move(coordinate,move_coord)    
                # If it is white's turn, and a move leads to a check to the white king, it is illegal. Vice versa for black
                if (white==True and self.is_white_check(temp_board)==True) or (white!=True and self.is_black_check(temp_board)==True):
                    pass
                else: temp.append(move_coord) # If the move doesn't lead to a check, add it back into the array 
            valid_moves = temp 
        return valid_moves

    # Check if a given position has a check for either king
    def is_check(self, board:Board)->tuple:
        position = board.board_position # Get the current board position 
        wking_pos = board.piece_coord("K") # Get the positions of both kings 
        bking_pos = board.piece_coord("k")
        white_checked = False
        black_checked = False
        for i in range(8): # Iterate over the board
            for j in range(8):
                piece = position[i][j]
                if piece !="": # Skip if not a piece
                    if piece.islower(): # If the piece is black
                        valid_moves = self.get_piece_moves(piece,board,(i,j),False,strict=False)
                        if wking_pos in valid_moves:
                            white_checked = True
                    elif piece.isupper(): # If the piece is white
                        valid_moves = self.get_piece_moves(piece,board,(i,j),True,strict=False)
                        if bking_pos in valid_moves: 
                            black_checked = True# TODO: potentially break the loop to make it more efficient. This requires separate white and black check functions
        return (white_checked, black_checked) # Just a 2-bit binary value         
    def is_white_check(self, board:Board)->bool:
        check = self.is_check(board)
        if check[0]==True:
            return True
        else:
            return False
    def is_black_check(self, board:Board)->bool:
        check = self.is_check(board)
        if check[1]==True:
            return True
        else:
            return False
        
                

    
    # Checks for valid syntax in an input provided by a player, and converts it into coordinates 
    # for the validation to use 
    # ? syntax checking can be made a lot more efficient but it is not crucial
    # Returns (-1) is syntax is invalid 
    def validate_syntax(self,board:Board,move:str,white:bool) -> tuple:
        coordinates = ()
        position = board.board_position
        move=move.replace('+','').replace('#','') #remove suffixes for now
        if move in ['O-O','O-O-O']: # castling 
            if white: 
                if move is 'O-O': return ((7,4),(7,6))
                else: return ((7,4),(7,2))
            else:
                if move is 'O-O': return ((0,4),(0,6))
                else: return ((0,4),(0,2))
        def square(pos:str)->bool: # Returns true if the string given is a square. For example, e4 will return true, but Ne4 won't.
            return len(pos)==2 and pos[0] in 'abcdefgh'  and pos[1] in '12345678'
        def prefix(move:str)->bool: # Checks if a move has a prefix to represent a piece being used 
            if move[0] in 'abcdefghNBRQK': #example Nx** , dx**, if square function is called before it 
                return True
            # TODO: check that these conditions are definitely not needed 
            # elif len(move)==2 and move[0] in 'NBRQK' and move[1] in 'abcdefgh12345678': #example Ndx** , N3x**
            #     return True
            # elif len(move)==3 and move[0] in 'QKB' and square(move[1:3]): #example Qd3 , Kf7
            #     return True
            return () # not sure if the conditions above are needed
        
        move=move.split('x') # Splits a move into two components, with the piece used and the square it is taking on
        # ! Will need to be reimplemented later as pawns are not able to capture 
        # CAPTURE MOVES 
        # if len(move)==2:# If there are two components, the move was split, so a piece is being captured
        #     if prefix(move[0]) and square(move[1]): # Example Nxd4 , dxd4
        #         if move[0][0] in "abcdefgh": # Pawn move
        #             start = board.piece_coord("p", file="abcdefgh".index(move[0]))
        #         else:
        #             start = board.piece_coord(move[0][0],file="abcdefgh".index(move[0]))
        #         end = ("87654321".index(move[1][1]), "abcdefgh".index(move[1][0]))
        #         coordinates = (start, end)
        #         return coordinates
                
        #     if prefix(move[0]) and square(move[1][:2]) and move[1][2]=='=' and move[1][3] in 'NBRQK': #example  dxd4=Q
        #         return True
        if False:
            pass
        # If the move isn't split, then it is a non-capturing move
        else:
            # NORMAL MOVES
            # PAWN MOVES
            if len(move[0])==2 and square(move[0]) or len(move[0])==4 and square(move[0][:2]) and move[0][2]=="="and move[0][3] in 'NBRQK': #example e4 , e3, or promotion e1=Q
                end = board.sq_coord(move[0])
                row, file = end
                # PROMOTIONS
                if row==7: # Black promotions and invalid moves
                    if white: raise ValueError("Can't promote backwards.") 
                    else: 
                        position[7][file]=move[0][3] # Assign to chosen piece 
                elif row==0: # White promotions and invalid moves
                    if not white: raise ValueError("Can't promote backwards.") 
                    else: 
                        position[0][file]=move[0][3] # Assign to chosen piece 
                # NORMAL PAWN MOVES AND STARTING MOVES
                elif white:  
                    if position[end[0]+1][file] =='P':
                        start = (end[0]+1,file)
                    elif position[5][file]=='' and position[6][file]=='P': 
                        start = (6,file)
                    else: raise ValueError("Invalid move or syntax.")
                else:
                    if position[end[0]-1][file] =='p':
                        start = (end[0]-1,file)
                    elif position[2][file]=='' and position[1][file]=='p': 
                        start = (1,file)
                    else: raise ValueError("Invalid move or syntax.")
                return (start, end)
            # OTHER PIECES 
            elif len(move[0])==3 or len(move[0])==4:
                if move[0][0] in 'NBRQK': # Check the first character is a piece
                    piece = move[0][0]
                    if not white: # Convert to black piece if black's turn
                        piece = piece.lower()
                    if len(move[0])==3 and square(move[0][1:3]): #  piece+square. Example Nf3, Qf3, Bb2 
                        start = board.piece_coord(piece) # ! Doesn't always work with multiple knights
                        end = board.sq_coord(move[0][1:3])
                        return (start, end)
                    elif len(move[0])==4 and square(move[0][2:4]): # piece+row/column+square
                        if move[0][1] in '87654321': # Example N2f3
                            row = '87654321'.index(move[0][1])
                            try: start = board.piece_coord(piece=piece, row=row)
                            except ValueError as e:
                                return (-1)
                        elif move[0][1] in 'abcdefgh': # Example Ngf3
                            file = 'abcdefgh'.index(move[0][1])
                            try: start = board.piece_coord(piece=piece, file=file) 
                            except ValueError as e:
                                return (-1)
                        end = board.sq_coord(move[0][2:4])
                        return (start, end)
                else: raise ValueError("'"+move[0][0]+"' is not a piece.")
            else: raise ValueError("Invalid move size.")
            #elif len(move[0])==4 and square(move[0][:2]) and move[0][2]=="="and move[0][3] in 'NBRQK': #promotion move example e1=Q # ! Promotions aren't dealt with 
            #elif len(move[0])==5 and move[0][0] in "QBK" and square(move[0][1:3]) and square(move[0][-2:]): # ! I don't know what this is
                #return True
        return (-1) # If everything fails, then the move is invalid

    
def syntax_tests(logic:Logic):
    print("e4" ,logic.validate_syntax('e4'))
    print("O-O" ,logic.validate_syntax('O-O')) 
    print("O-O+" ,logic.validate_syntax('O-O+')) 
    print("O-O#" ,logic.validate_syntax('O-O#')) 
    print("Nf3" ,logic.validate_syntax('Nf3')) 
    print("Ngf3" ,logic.validate_syntax('Ngf3'))
    print("N2f3" ,logic.validate_syntax('N2f3'))
    print("Ngxf3" ,logic.validate_syntax('Ngxf3'))  
    print("Nxf3" ,logic.validate_syntax('Nxf3'))  
    print("R3d3" ,logic.validate_syntax('R3d3'))  
    print("e1=Q" ,logic.validate_syntax('e1=Q'))  
    print("e1=Q+" ,logic.validate_syntax('e1=Q+'))  
    print("e1=Q#" ,logic.validate_syntax('e1=Q#'))  
    print("Rdxf3" ,logic.validate_syntax('Rdxf3'))  
    print("fxe1=Q+" ,logic.validate_syntax('fxe1=Q+'))  
    print("Qe4f5+" ,logic.validate_syntax('Qe4f5+'))
    print("Qe4xf5+" ,logic.validate_syntax('Qe4xf5+'))
    print("Qwda" ,logic.validate_syntax('Qwda'))
    print("Kg2wda" ,logic.validate_syntax('Kg2wda'))
    print("e47" ,logic.validate_syntax('e47'))
    print("w2" ,logic.validate_syntax('w2'))
    
    
# Test for move syntax checking 
if __name__ == "__main__":
    # Creating an instance of the class
    logic = Logic()
    
    board = Board()
    fen="q3kb1r/1p2pppp/5n2/2rp4/3Q1B2/4PN2/P1n2PPP/R3K2R w KQk - 0 14"
    newboard=board.fen_to_matrix(fen)
    # set board tests
    board.setboard(newboard)
    draw_tool = draw.DrawTool()
    d = lambda: draw_tool.draw_board(board.board_position) # just shorter
    d()

    
    board.setboard(board.board_position) # Save position 
    moves = rook_moves(board.board_position, (7,0), white=True, show=True)
    d()
    board.undo()
    board.setboard(board.board_position) # Save position 
    moves = bishop_moves(board.board_position, (4,5), white=True, show=True)
    d()
    board.undo()
    board.setboard(board.board_position) # Save position 
    moves = queen_moves(board.board_position, (4,3), white=True, show=True)
    d()
    board.undo()
    board.setboard(board.board_position) # Save position 
    moves = king_moves(board.board_position, (7,4), white=True, show=True)
    d()
    board.undo()
    board.setboard(board.board_position) # Save position 
    moves = king_moves(board.board_position, (0,4), white=False, show=True)
    d()
    board.undo()
    board.setboard(board.board_position) # Save position 
    moves = knight_moves(board.board_position, (5,5), white=True, show=True)
    d()
    board.undo()
    board.setboard(board.board_position) # Save position 
    moves = pawn_moves(board.board_position, (1,1), white=False, show=True)
    d()
    board.undo()
    board.setboard(board.board_position) # Save position 
    # d()
    
    
    print()
    print(moves) 