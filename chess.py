import pygame
import copy

depth = 2
fps = 60
width, height = 700, 700
rows, cols = 8, 8
square_size = width//cols

#creating the window
Window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")

def load_img(name):
    img = pygame.transform.scale(pygame.image.load('E:/IP/Python/Python Chess/Self_Chess/Chess_pieces/'+str(name)), (90, 90))
    return img

#loading the images
b_king = load_img('kingb.png')
w_king = load_img('kingw.png')
b_queen = load_img('queenb.png')
w_queen = load_img('queenw.png')
b_pawn = load_img('pawnb.png')
w_pawn = load_img('pawnw.png')
b_knight = load_img('knightb.png')
w_knight = load_img('knightw.png')
b_rook = load_img('rookb.png')
w_rook = load_img('rookw.png')
b_bishop = load_img('bishopb.png')
w_bishop = load_img('bishopw.png')
valid_move = load_img('valid_move.png')
valid_move_piece = load_img('valid_move_piece.png')

#some variables
black = "black"
white = "white"
rook = "rook"
bishop = "bishop"
king = "king"
queen = "queen"
pawn = "pawn"
knight = "knight"
board_b = (125, 135, 165)
board_w = (232, 235, 239)
blue = (0,0,255)

#keeps record of the internal representation of the chess board
class Board():
    def __init__(self, side):
        #board is a 2 dimentional array(list)
        self.board = []
        #keeping a record of total number of pieces on the board 
        self.white_knights = self.black_knights = self.white_bishops = self.black_bishops = self.black_rooks = self.white_rooks = 2
        self.white_king = self.white_queen = self.black_king = self.black_queen = 1
        self.white_pawns = self.black_pawns = 8 
        #checking for castling
        self.white_king_moved = self.black_king_moved = False 
        self.white_rook_right_moved = self.white_rook_left_moved = self.black_rook_right_moved = self.black_rook_left_moved = False 
        #variable to check if either side is under check
        self.is_white_check = self.is_black_check = False
        #will keep a record of the previous move(for en passant)
        self.prev_move = None
        #the side chosen by the user
        self.side = side
        #creating the board
        self.create_board()

    #evaluation function to evaluate a given position of the board
    def evaluate(self):
        return 200*(self.white_king-self.black_king)\
            +9*(self.white_queen-self.black_queen)\
            +5*(self.white_rooks-self.black_rooks)\
            +3*(self.white_knights-self.black_knights+self.white_bishops-self.black_bishops)\
            +1*(self.white_pawns-self.black_pawns)

    #creating the chess board pattern
    def draw_squares(self, win):
        win.fill(board_w)
        for row in range(rows):
            for col in range(row%2, rows, 2):
                pygame.draw.rect(win, board_b, (row*square_size, col*square_size, square_size, square_size))

    #changing the side(other than the one chosen by the user)
    def change_side(self):
        if self.side == black:
            return white
        return black 

    #creating the regular chess board
    def create_board(self):
        for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if row == 0 and (col == 0 or col == 7):
                    self.board[row].append(Piece(row, col, self.change_side(), rook))
                elif row == 7 and (col == 0 or col == 7):
                    self.board[row].append(Piece(row, col, self.side, rook))
                elif row == 0 and (col == 1 or col == 6):
                    self.board[row].append(Piece(row, col, self.change_side(), knight))
                elif row == 7 and (col == 1 or col == 6):
                    self.board[row].append(Piece(row, col, self.side, knight))
                elif row == 0 and (col == 2 or col == 5):
                    self.board[row].append(Piece(row, col, self.change_side(), bishop))
                elif row == 7 and (col == 2 or col == 5):
                    self.board[row].append(Piece(row, col, self.side, bishop))
                elif row == 0 and col == 3:
                    self.board[row].append(Piece(row, col, self.change_side(), queen))
                elif row == 7 and col == 3:
                    self.board[row].append(Piece(row, col, self.side, queen))
                elif row == 0 and col == 4:
                    self.board[row].append(Piece(row, col, self.change_side(), king))
                elif row == 7 and col == 4:
                    self.board[row].append(Piece(row, col, self.side, king))
                elif row == 1:
                    self.board[row].append(Piece(row, col, self.change_side(), pawn))
                elif row == 6:
                    self.board[row].append(Piece(row, col, self.side, pawn))
                else:
                    self.board[row].append(0)
    
    #changing the board as per the move made			
    def move(self, piece, row, col):
        en_passant = None 
        color, rank = piece.__repr__()
        if rank == king:
            right_moves =  self._castling_right(piece.row, piece.col, color)
            left_moves = self._castling_left(piece.row, piece.col, color)
            if (row, col) in right_moves:
                right_rook = self.get_piece(row, 7)
                self.board[right_rook.row][right_rook.col], self.board[piece.row][piece.col+1] = \
                    self.board[piece.row][piece.col+1], self.board[right_rook.row][right_rook.col]
                right_rook.move(piece.row, piece.col+1)
                if color == white:
                    self.white_rook_right_moved = True
                else:
                    self.black_rook_right_moved = True
            elif (row, col) in left_moves:
                left_rook = self.get_piece(row, 0)
                self.board[left_rook.row][left_rook.col], self.board[piece.row][piece.col-1] = \
                    self.board[piece.row][piece.col-1], self.board[left_rook.row][left_rook.col]
                left_rook.move(piece.row, piece.col-1)
                if color == white:
                    self.black_rook_left_moved = True
                else:
                    self.white_rook_left_moved = True
            if color == white:
                self.white_king_moved = True
            else:
                self.black_king_moved = True
        if rank == rook:
            c = piece.col
            if color == white:
                if c == 0:
                    self.white_rook_left_moved = True
                elif c == 7:
                    self.white_rook_right_moved = True
            else:
                if c == 0:
                    self.black_rook_left_moved = True
                elif c == 7:
                    self.black_rook_right_moved = True
        
        if rank == pawn:
            if (row, col) in self._en_passant(piece.row, piece.col,self.side):
                en_passant = (True, white)
            elif (row, col) in self._en_passant(piece.row, piece.col, self.change_side()):
                en_passant = (True, black)
            else:
                en_passant = None

        if rank == pawn:
            self.prev_move = ((piece.row, piece.col),(row, col))
        else:
            self.prev_move = None

        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if rank == pawn:
            if en_passant != None:
                if en_passant[1] == white:
                    self.remove(row+1, col)
                else:
                    self.remove(row-1, col)

            if row == 0 or row == 7:
                ans = input("What do you want to promote to?(q, b, r, k): ")
                if ans == "q":
                    if color == white:
                        self.board[row][col] = Piece(row, col, white, queen)
                        self.board[row][col].draw_queen(Window, color)
                        self.white_queen += 1
                    else:
                        self.board[row][col] = Piece(row, col, black, queen)
                        self.board[row][col].draw_queen(Window, color)
                        self.black_queen += 1
                elif ans == "b":
                    if color == white:
                        self.board[row][col] = Piece(row, col, white, bishop)
                        self.board[row][col].draw_bishop(Window, color)
                        self.white_bishops += 1
                    else:
                        self.board[row][col] = Piece(row, col, black, bishop)
                        self.board[row][col].draw_bishop(Window, color)
                        self.black_bishops += 1
                elif ans == "r":
                    if color == white:
                        self.board[row][col] = Piece(row, col, white, rook)
                        self.board[row][col].draw_rook(Window, color)
                        self.white_rooks += 1
                    else:
                        self.board[row][col] = Piece(row, col, black, rook)
                        self.board[row][col].draw_rook(Window, color)
                        self.black_rooks += 1
                else:
                    if color == white:
                        self.board[row][col] = Piece(row, col, white, knight)
                        self.board[row][col].draw_knight(Window, color)
                        self.white_knights += 1
                    else:
                        self.board[row][col] = Piece(row, col, black, knight)
                        self.board[row][col].draw_knight(Window, color)
                        self.black_knights += 1

            

        if color == black:
            self.is_white_check = is_check(self, white)

        if color == white:
            self.is_black_check = is_check(self, black)			

    #getting the piece on the given pos(row,col) 
    def get_piece(self, row, col):
        return self.board[row][col]

    #drawing the pieces and squares
    def  draw(self, win):
        self.draw_squares(win)
        for row in range(rows):
            for col in range(cols):
                piece = self.board[row][col]
                if piece != 0:
                    color, rank = piece.__repr__()
                    if color == black:
                        if rank == pawn:
                            piece.draw_pawn(win, color)
                        if rank == king:
                            piece.draw_king(win, color)
                        if rank == queen:
                            piece.draw_queen(win, color)
                        if rank == rook:
                            piece.draw_rook(win, color)
                        if rank == knight:
                            piece.draw_knight(win, color)
                        if rank == bishop:
                            piece.draw_bishop(win, color)
                    else:
                        if rank == pawn:
                            piece.draw_pawn(win, color)
                        if rank == king:
                            piece.draw_king(win, color)
                        if rank == queen:
                            piece.draw_queen(win, color)
                        if rank == rook:
                            piece.draw_rook(win, color)
                        if rank == knight:
                            piece.draw_knight(win, color)
                        if rank == bishop:
                            piece.draw_bishop(win, color)

    #removing the piece at a given pos(row,col)
    def remove(self, row, col):
        self.board[row][col] = 0

    #getting all the valid moves for a given piece
    def get_valid_moves(self, piece, condition=True):
        moves = []
        color, rank = piece.__repr__()
        col = piece.col
        row = piece.row
        if rank == pawn:
            if color == self.side:
                moves.extend(self._self_pawn(row, col))
                moves.extend(self._en_passant(row, col, self.side))
            else:
                moves.extend(self._opp_pawn(row, col))
                moves.extend(self._en_passant(row, col, self.change_side()))
        elif rank == knight:
            moves.extend(self._knight_traverse(row, col, color))
        elif rank == rook:
            moves.extend(self._rook_traverse_row(row, col, color))
            moves.extend(self._rook_traverse_col(row, col, color))
        elif rank == bishop:
            moves.extend(self._bishop_traverse_left(row, col, color))
            moves.extend(self._bishop_traverse_right(row, col, color))
        elif rank == queen:
            moves.extend(self._bishop_traverse_left(row, col, color))
            moves.extend(self._bishop_traverse_right(row, col, color))
            moves.extend(self._rook_traverse_row(row, col, color))
            moves.extend(self._rook_traverse_col(row, col, color))
        else:
            moves.extend(self._king_traverse(row, col, color))
            moves.extend(self._castling_right(row, col, color))
            moves.extend(self._castling_left(row, col, color)) 

        copy_moves = copy.deepcopy(moves)

        if condition:
            if color == white:
                for move in moves:
                    temp_board = copy.deepcopy(self)
                    temp_piece = copy.deepcopy(piece)
                    new_board,_ = simulate_move(temp_piece, temp_board, move)
                    opp_moves = get_all_valid_moves(new_board, black)
                    for opp_move in opp_moves:
                        new_piece = new_board.get_piece(opp_move[0], opp_move[1])
                        if new_piece != 0 and new_piece.rank == king:
                            try:
                                copy_moves.remove(move)
                            except ValueError:
                                pass
            elif color == black:
                for move in moves:
                    temp_board = copy.deepcopy(self)
                    temp_piece = copy.deepcopy(piece)
                    new_board,_ = simulate_move(temp_piece, temp_board, move)
                    opp_moves = get_all_valid_moves(new_board, white)
                    for opp_move in opp_moves:
                        new_piece = new_board.get_piece(opp_move[0], opp_move[1])
                        if new_piece != 0 and new_piece.rank == king:
                            try:
                                copy_moves.remove(move)
                            except ValueError:
                                pass
                
        moves = copy_moves

        if rank == king: 
            if ((row, col+2) in moves) and ((row, col+1) not in moves):
                moves.remove((row, col+2))
            elif ((row, col-2) in moves) and ((row, col-1) not in moves):
                moves.remove((row, col-2))

        return moves

    #returning the move for left-side-castling
    def _castling_left(self, row, col, color):
        moves = []
        if not self.is_white_check and not self.is_black_check:
            if color == white:
                if self.white_king_moved == self.white_rook_left_moved == False:
                    space = []
                    spaces = col-1
                    for c in range(1, col):
                        piece = self.get_piece(row, c)
                        if piece == 0:
                            space.append((row, c))
                        else:
                            break
                    if len(space) == spaces:
                        moves.append((row, col-2))
            else:
                if self.black_king_moved == self.black_rook_left_moved == False:
                    space = []
                    spaces = col-1
                    for c in range(1, col):
                        piece = self.get_piece(row, c)
                        if piece == 0:
                            space.append((row, c))
                        else:
                            break
                    if len(space) == spaces:
                        moves.append((row, col-2))

        return moves

    #returning the move for en passant
    def _en_passant(self, row, col, color):
        moves = []
        prev_move = self.prev_move
        if prev_move != None and abs(prev_move[0][0]-prev_move[1][0]) == 2:
            final_pos = prev_move[1]
            f_row, f_col = final_pos[0], final_pos[1]
            if (col == f_col-1 or col == f_col+1) and row == f_row:
                for r in range(rows):
                    if r == 3 and color == self.side:
                        moves.append((row-1, f_col))
                    elif r == 4 and color == self.change_side():
                        moves.append((row+1, f_col))
        return moves

    #returning the move for right-side-castling
    def _castling_right(self, row, col, color):
        moves = [] 
        if not self.is_white_check and not self.is_black_check:
            if color == white:
                if self.white_king_moved == self.white_rook_right_moved == False:
                    space = []
                    spaces = 6 - col
                    for c in range(6, col, -1):
                        piece = self.get_piece(row, c)
                        if piece == 0:
                            space.append((row, c))
                        else:
                            break
                    if len(space) == spaces:
                        moves.append((row, col+2))
            else:
                if self.black_king_moved == self.black_rook_right_moved == False:
                    space = []
                    spaces = 6 - col
                    for c in range(6, col, -1):
                        piece = self.get_piece(row, c)
                        if piece == 0:
                            space.append((row, c))
                        else:
                            break
                    if len(space) == spaces:
                        moves.append((row, col+2))

        return moves

    #getting all the valid moves for the king of a given color
    def _king_traverse(self, row, col, color):
        moves = []
        spaces = [(row+1, col+1), (row-1, col-1), (row+1, col-1), (row-1, col+1),
                    (row, col-1), (row, col+1), (row+1, col), (row-1, col)]
        for r, c in spaces:
            if 8>r>-1 and 8>c>-1:
                piece = self.get_piece(r, c)
                if piece == 0:
                    moves.append((r, c))
                elif piece.color != color:
                    moves.append((r, c))
        return moves

    #getting all the valid moves for a knight of a given color
    def _knight_traverse(self, row, col, color):
        moves = []
        spaces = [(row+2, col+1), (row+2, col-1), (row+1, col+2), (row-1, col+2),\
                    (row+1, col-2), (row-1, col-2), (row-2, col+1), (row-2, col-1)]
        for r, c in spaces:
            if 8>r>-1 and 8>c>-1:
                piece = self.get_piece(r, c)
                if piece == 0:
                    moves.append((r, c))
                elif piece.color != color:
                    moves.append((r, c))
        return moves

    #getting all the moves that the rook can make in its row
    def _rook_traverse_row(self, row, col, color):
        moves = []
        col_number = None
        for c in range(cols):
            piece = self.get_piece(row, c)
            if col>c:
                if piece == 0:
                    moves.append((row, c))
                elif piece.color == color:
                    moves.clear()
                else:
                    moves.clear()
                    moves.append((row, c))
            elif col == c:
                continue
            else:
                if col_number == None:
                    if piece == 0:
                        moves.append((row, c))
                    elif piece.color == color:
                        col_number = c
                    else:
                        moves.append((row, c))
                        col_number = c
                else:
                    break
        return moves

    #getting all the moves that the rook can make in its column
    def _rook_traverse_col(self, row, col, color):
        moves = []
        row_number = None
        for r in range(rows):
            piece = self.get_piece(r, col)
            if row>r:
                if piece == 0:
                    moves.append((r, col))
                elif piece.color == color:
                    moves.clear()
                else:
                    moves.clear()
                    moves.append((r, col))
            elif row == r:
                continue
            else:
                if row_number == None:
                    if piece == 0:
                        moves.append((r, col))
                    elif piece.color == color:
                        row_number = r
                    else:
                        moves.append((r, col))
                        row_number = r
                else:
                    break
        return moves

    #getting all the valid moves for the pawns of the opponent
    def _opp_pawn(self, row, col):
        moves = []
        if row == 1:
            for i in range(1, 3):
                if i == 2:
                    if len(moves)==0:
                        break
                r = row+i
                if 8>r>-1:
                    piece = self.get_piece(r, col)
                    if piece == 0:
                        moves.append((r, col))
        else:
            piece = self.get_piece(row+1, col)
            if piece == 0:
                moves.append((row+1, col))

        right_diag = (row+1, col+1)
        left_diag = (row+1, col-1)
        if 8>row+1>-1 and 8>col+1>-1:
            right_space = self.get_piece(right_diag[0], right_diag[1])
            if right_space != 0 and right_space.color == self.side:
                moves.append(right_diag)
        if 8>row+1>-1 and 8>col-1>-1:
            left_space = self.get_piece(left_diag[0], left_diag[1])
            if left_space != 0 and left_space.color == self.side:
                moves.append(left_diag)
    
        return moves

    #getting all the valid moves for all the pawns of self
    def _self_pawn(self, row, col):
        moves = []
        if row == 6:
            for i in range(1, 3):
                if i == 2:
                    if len(moves)==0:
                        break
                r = row-i
                if 8>r>-1:
                    piece = self.get_piece(r, col)
                    if piece == 0:
                        moves.append((r, col))
        else:
            piece = self.get_piece(row-1, col)
            if piece == 0:
                moves.append((row-1, col))

        right_diag = (row-1, col+1)
        left_diag = (row-1, col-1)
        if 8>row-1>-1 and 8>col+1>-1:
            right_space = self.get_piece(right_diag[0], right_diag[1])
            if right_space != 0 and right_space.color != self.side:
                moves.append(right_diag)
        if 8>row-1>-1 and 8>col-1>-1:
            left_space = self.get_piece(left_diag[0], left_diag[1])
            if left_space != 0 and left_space.color != self.side:
                moves.append(left_diag)

        return moves

    #getting all the moves for the bishop to the left-hand-side of the bishop
    def _bishop_traverse_left(self, row, col, color):
        moves = []
        total = row - col
        row_number = None
        for r in range(rows):
            for c in range(cols):
                if r-c == total:
                    piece = self.get_piece(r, c)
                    if row>r:
                        if piece == 0:
                            moves.append((r, c))
                        elif piece.color == color:
                            moves.clear()
                        else:
                            moves.clear()
                            moves.append((r, c))
                    elif r == row:
                        break
                    else:
                        if row_number == None:
                            if piece == 0:
                                moves.append((r, c))
                            elif piece.color == color:
                                row_number = r 
                            else:
                                moves.append((r, c))
                                row_number = r
                        else:
                            break
        return moves

    #getting all the moves for the bishop to the right-hand-side of the bishop
    def _bishop_traverse_right(self, row, col, color):
        moves = []
        total = row + col
        row_number = None
        for r in range(rows):
            for c in range(cols):
                if r+c == total:
                    piece = self.get_piece(r, c)
                    if row>r:
                        if piece == 0:
                            moves.append((r, c))
                        elif piece.color == color:
                            moves.clear()
                        else:
                            moves.clear()
                            moves.append((r, c))
                    elif r == row:
                        break
                    else:
                        if row_number == None:
                            if piece == 0:
                                moves.append((r, c))
                            elif piece.color == color:
                                row_number = r 
                            else:
                                moves.append((r, c))
                                row_number = r
                        else:
                            break	
        return moves


#represents the piece as a separate object and keeps records of the row,col,color and rank of the piece
class Piece():
    def __init__(self, row, col, color, rank):
        self.row = row
        self.col = col
        self.color = color
        self.rank = rank
        self.x = 0
        self.y = 0
        self.calc_pos()

    #calculating the position of piece
    def calc_pos(self):
        self.x = self.col*square_size + square_size//2
        self.y = self.row*square_size + square_size//2

    #drawing king from the image on the board
    def draw_king(self, win, color):
        if color == white:
            win.blit(w_king, (self.x-w_king.get_width()//2, self.y-w_king.get_height()//2))
        else:
            win.blit(b_king, (self.x-b_king.get_width()//2, self.y-b_king.get_height()//2))

    #drawing queen from the image on the board
    def draw_queen(self, win, color):
        if color == white:
            win.blit(w_queen, (self.x-w_queen.get_width()//2, self.y-w_queen.get_height()//2))
        else:
            win.blit(b_queen, (self.x-b_queen.get_width()//2, self.y-b_queen.get_height()//2))

    #drawing pawn from the image on the board
    def draw_pawn(self, win, color):
        if color == white:
            win.blit(w_pawn, (self.x-w_pawn.get_width()//2, self.y-w_pawn.get_height()//2))
        else:
            win.blit(b_pawn, (self.x-b_pawn.get_width()//2, self.y-b_pawn.get_height()//2))

    #drawing knight from the image on the board
    def draw_knight(self, win, color):
        if color == white:
            win.blit(w_knight, (self.x-w_knight.get_width()//2, self.y-w_knight.get_height()//2))
        else:
            win.blit(b_knight, (self.x-b_knight.get_width()//2, self.y-b_knight.get_height()//2))

    #drawing rook from the image on the board
    def draw_rook(self, win, color):
        if color == white:
            win.blit(w_rook, (self.x-w_rook.get_width()//2, self.y-w_rook.get_height()//2))
        else:
            win.blit(b_rook, (self.x-b_rook.get_width()//2, self.y-b_rook.get_height()//2))

    #drawing bishop from the image on the board
    def draw_bishop(self, win, color):
        if color == white:
            win.blit(w_bishop, (self.x-w_bishop.get_width()//2, self.y-w_bishop.get_height()//2))
        else:
            win.blit(b_bishop, (self.x-b_bishop.get_width()//2, self.y-b_bishop.get_height()//2))

    #changes the row and col and updates the position
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    #special representation method returning the color and rank of the piece as strings
    def __repr__(self):
        return str(self.color), str(self.rank)


#a very basic api which coordinates the working of the two classes board and piece
class Game():
    def __init__(self, win, side):
        self.side = side
        self._init()
        self.win = win

    #draws and keeps the board updated
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    #initialisation method
    def _init(self):
        self.selected = None
        self.board = Board(self.side)
        self.valid_moves = []
        self.turn = white

    #resets everything
    def reset(self):
        self._init()

    #checks if there's a winner or not
    def winner(self):
        if self.board.is_white_check and self.turn == white:
            all_valid_moves = get_all_valid_moves(self.board, white, True)
            if all_valid_moves == []:
                return "BLACK", "WHITE"
        elif self.board.is_black_check and self.turn == black:
            all_valid_moves = get_all_valid_moves(self.board, black, True)
            if all_valid_moves == []:
                return "WHITE", "BLACK"
        elif self.turn == black or self.turn == white:
            all_valid_moves = get_all_valid_moves(self.board, self.turn, True)
            if all_valid_moves == []:
                return "STALEMATE", "STALEMATE"
        return None

    #it checks if the selected piece is valid or not
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    #moving the selected piece and keeping the record of the pieces left on the board (for evaluation function)
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)

        if piece != 0:
            if piece.color != self.turn:
                if piece.color == white:
                    if piece.rank == queen:
                        self.board.white_queen -= 1
                    elif piece.rank == rook:
                        self.board.white_rooks -= 1
                    elif piece.rank == knight:
                        self.board.white_knights -= 1
                    elif piece.rank == bishop:
                        self.board.white_bishops -= 1
                    elif piece.rank == pawn:
                        self.board.white_pawns -= 1
                else:
                    if piece.rank == queen:
                        self.board.black_queen -= 1
                    elif piece.rank == rook:
                        self.board.black_rooks -= 1
                    elif piece.rank == knight:
                        self.board.black_knights -= 1
                    elif piece.rank == bishop:
                        self.board.black_bishops -= 1
                    elif piece.rank == pawn:
                        self.board.black_pawns -= 1

        if self.selected and (row, col) in self.valid_moves:
            if piece == 0:
                self.board.move(self.selected, row, col)
                self.change_turn()
            elif piece != 0:
                if piece.color == self.turn:
                    return False
                else:
                    self.board.remove(row, col)
                    self.board.move(self.selected, row, col)
                    self.change_turn()
            else:
                return False
        return True

    #changing the side
    def change_side(self):
        return self.board.change_side()

    #returns the board
    def get_board(self):
        return self.board

    #changing the turn
    def change_turn(self):
        self.valid_moves = []
        if self.turn == white:
            self.turn = black
        else:
            self.turn = white

    #given the previous board, current board and color it returns the previous move made by that color's side
    def get_previous_move(self, prev_board, color):
        prev_move = None
        condition = False
        prev_pieces = get_all_pieces(prev_board, color)
        curr_pieces = get_all_pieces(self.board, color)
        for piece in prev_pieces:
            if piece.rank == pawn:
                new_piece = self.board.get_piece(piece.row, piece.col)
                if new_piece == 0:
                    initial_pos = (piece.row, piece.col)
                    break    
        for piece in curr_pieces:
            if piece.rank == pawn:
                new_piece = prev_board.get_piece(piece.row, piece.col)
                if new_piece == 0 or piece.color == change_color(color):
                    final_pos = (piece.row, piece.col)
                    condition = True    

        if condition:
            prev_move = (initial_pos, final_pos)
        return prev_move     

    #drawing the valid moves for a given piece on the board
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            piece = self.board.get_piece(row, col)
            if piece == 0:
                self.win.blit(valid_move, 
                    (col*square_size-valid_move.get_width()//2+square_size//2, row*square_size-valid_move.get_height()//2+square_size//2))
            else:
                self.win.blit(valid_move_piece, 
                    (col*square_size-valid_move_piece.get_width()//2+square_size//2, row*square_size-valid_move_piece.get_height()//2+square_size//2))

#changing the color
def change_color(color):
    if color==white:
        return black
    return white

#getting all the valid moves for all the pieces of a given color 
def get_all_valid_moves(board, color, con=False):
        all_valid_moves = []
        pieces = get_all_pieces(board, color)
        for piece in pieces:
            valid_moves = board.get_valid_moves(piece, con)
            all_valid_moves.extend(valid_moves)

        return all_valid_moves

#getting all the pieces of a given color
def get_all_pieces(board, color):
        pieces = []
        for row in board.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

#drawing the moves on the board
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves)
    pygame.display.update()
    pygame.time.delay(100)

#checkig if a side is checked or not
def is_check(board, color):
    if color == white:
        color = black
    else:
        color = white
    moves = get_all_valid_moves(board, color)
    for row, col in moves:
        piece = board.get_piece(row, col)
        if piece != 0 and piece.rank == king:
            return True
    return False

#getting all the valid boards, after making each valid move on the move on the board for a color
def get_all_valid_boards(board, color, game):
    moves = []
    for piece in get_all_pieces(board, color):
        valid_moves = board.get_valid_moves(piece, True)
        for move in valid_moves:
            #draw_moves(game, board, piece)
            temp_board = copy.deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board, new_move = simulate_move(temp_piece, temp_board, move)
            moves.append((new_board, new_move, piece))
    return moves

#simulating the move on the board
def simulate_move(piece, board, move):
    en_passant = None
    row,col = move[0], move[1]
    space = board.get_piece(move[0], move[1])
    if space != 0:
        board.remove(space.row, space.col)
    if piece.rank == pawn:
        if (row, col) in board._en_passant(piece.row, piece.col,board.side):
            en_passant = (True, white)
        elif (row, col) in board._en_passant(piece.row, piece.col, board.change_side()):
            en_passant = (True, black)
    if piece.rank == pawn:
        board.prev_move = ((piece.row, piece.col),(row, col))
    else:
        board.prev_move = None
    board.board[piece.row][piece.col], board.board[move[0]][move[1]] = board.board[move[0]][move[1]], board.board[piece.row][piece.col]
    piece.move(move[0], move[1])
    if piece.rank == pawn:
        if en_passant != None:
            if en_passant[1] == white:
                board.remove(row+1, col)
            else:
                board.remove(row-1, col)
    return board, move

#getting position from the mouse
def get_pos_from_mouse(pos):
    x, y = pos
    row = y//square_size
    col = x//square_size
    return row, col

#the minimax algorithm
def minimax(board, depth, max_player, game):
    #max_player = white
    if depth == 0 or game.winner() != None:
        return board.evaluate(), board, None
    if max_player:
        maxEval = float('-inf')
        best_board = None
        for nboard, move, piece in get_all_valid_boards(board, white, game):
            evaluation = minimax(nboard, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_board = nboard
        return maxEval, best_board, piece	
    else:
        minEval = float('inf')
        best_board = None
        for nboard, move, piece in get_all_valid_boards(board, black, game):
            evaluation = minimax(nboard, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_board = nboard
        return minEval, best_board, piece


#the main function that is actually executed
def main():
    valid = False
    while not valid:
        side = input("Which side do you want: ")
        if side.lower() == black:
            side = black
            valid = True
        elif side.lower() == white:
            side = white
            valid = True
        else:
            print("Please enter a valid answer(white/black)!!")

    valid_difficulty = False
    while not valid_difficulty:
        print("The higher the difficulty level the longer will the A.I. take to make the move.")
        difficulty = input("Enter a difficulty level(integer): ")
        try:
            depth = int(difficulty)
            valid_difficulty = True
        except ValueError:
            print("Please enter a valid integer!!")

    run = True
    clock = pygame.time.Clock()
    game = Game(Window, side)

    while run:
        clock.tick(fps)

        if game.winner() != None and game.winner()[0] != "STALEMATE":
            print(f"{game.winner()[1]} is checkmated, {game.winner()[0]} has won!")
            run = False
            pygame.time.delay(1000)
            break
        elif  game.winner() != None and game.winner()[0] == "STALEMATE":
            print(f"It's a {game.winner()[0]}!")
            run = False
            break
        
        if game.turn == game.change_side() == white:
            prev_board = copy.deepcopy(game.board)
            value, game.board, piece = minimax(game.get_board(), depth, True, game)
            game.board.prev_move = game.get_previous_move(prev_board, white)
            game.change_turn()
        elif game.turn == game.change_side() == black:
            prev_board = copy.deepcopy(game.board)
            value, game.board, piece = minimax(game.get_board(), depth, False, game)
            game.board.prev_move = game.get_previous_move(prev_board, black)
            game.change_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_pos_from_mouse(pos)
                game.select(row, col)

        game.update()	

    pygame.time.wait(800)
    pygame.quit()

main() 
#THE END
