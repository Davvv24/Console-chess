import random
class Board:
    start_board= [
            ['R','N','B','Q','K','B','N','R'],
            ['P','P','P','P','P','P','P','P'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['p','p','p','p','p','p','p','p'],
            ['r','n','b','q','k','b','n','r']
        ]
    def __init__(self):
        self.board_position = self.start_board
    def setboard(self,board=start_board):
        self.board_position = board
    def shuffle(arr):
        new_arr = []
        for i in range(len(arr)):
            new_arr.append(arr.pop(random.randint(0,len(arr)-1)))
        return new_arr
        

    def randomize_board_dirty(self):
        #dirty randomization (no checks for valid positions or if the king is in check)
        arr=self.board_position
        arr = arr.flatten()
        arr = self.shuffle(arr)
        arr = arr.reshape((8, 8))
        self.board_position=arr

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
                    board[i,j] = k
                    j += 1
        return board

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

    def pgn_to_moves(self,pgn): ## move to utils 
        pgn = pgn.split(' ')
        moves = []
        for i in pgn:
            if '.' in i:
                continue
            moves.append(i)
        return moves

    def pawn_move(self,board,move,turn): ## move to game/piece module	
        pawns=['a','b','c','d','e','f','g','h']
        if move[0].low() in pawns:
            if turn==0:
                board[8-int(move[1]),pawns.index(move[0])]='P'
            else:
                board[8-int(move[1]),pawns.index(move[0])]='p'    

    def move_pawn(self,board,coordinate): ## move to game/piece module
        l,c=coordinate
        if l==1:
            board[l,c]=''
            board[l+2,c]='P'
        else:
            board[l,c]=''
            board[l-2,c]='p'
        return board

if __name__=='__main__':

    board=Board()
    # fen test
    fen="q3kb1r/1p2pppp/5n2/2rp4/3Q1B2/4PN2/P1n2PPP/R3K2R w KQk - 0 14"
    newboard=board.fen_to_matrix(fen)
    
    # set board tests
    board.setboard(newboard)
    board.setboard()  
    board.randomize_board_dirty()
    board.matrix_to_fen(board.board_position,display=True)
    # pgn test
    pgn="e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 O-O c3 d5 exd5 Nxd5 Nxe5 Nxe5 Rxe5 c6 d4 Bd6 Re1 Qh4 g3 Qh3 Be3 Bg4 Qd3 Rae8 Nd2 Re6 a4 Qh5 axb5 axb5 Bxd5 cxd5 Qxb5 Rb8 Qa5 Rxb2 Qd8+ Bf8 Ra8 h6 Qxf8+ Kh7 Qh8+ Kg6 Rg8 Rxe3 Qxg7+ Kf5 Qxf7#"
    print(board.pgn_to_moves(pgn))