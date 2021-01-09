import pygame
import copy

fps = 60
width, height = 700, 700
rows, cols = 8, 8
square_size = width//cols

Window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")

b_king = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/kingb.png'), (90,90))
w_king = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/kingw.png'), (90,90))
b_queen = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/queenb.png'), (90,90))
w_queen = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/queenw.png'), (90,90))
b_pawn = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/pawnb.png'), (90,90))
w_pawn = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/pawnw.png'), (90,90))
b_knight = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/knightb.png'), (90,90))
w_knight = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/knightw.png'), (90,90))
b_rook = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/rookb.png'), (90,90))
w_rook = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/rookw.png'), (90,90))
b_bishop = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/bishopb.png'), (90,90))
w_bishop = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/bishopw.png'), (90,90))
valid_move = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/valid_move.png'), (90,90))
valid_move_piece = pygame.transform.scale(pygame.image.load('Python Chess/Self_Chess/Chess_pieces/valid_move_piece.png'), (90,90))

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

class Board():
	def __init__(self):
		self.board = []
		self.white_knights = self.black_knights = self.white_bishops = self.black_bishops = self.black_rooks = self.white_rooks = 2
		self.white_king = self.white_queen = self.black_king = self.white_queen = 1
		self.white_pawns = self.black_pawns = 8 
		self.white_king_moved = self.black_king_moved = False
		self.white_rook_right_moved = self.white_rook_left_moved = self.black_rook_right_moved = self.black_rook_left_moved = False 
		self.is_white_check = self.is_black_check = False
		self.create_board()

	def draw_squares(self, win):
		win.fill(board_w)
		for row in range(rows):
			for col in range(row%2, rows, 2):
				pygame.draw.rect(win, board_b, (row*square_size, col*square_size, square_size, square_size))

	def create_board(self):
		for row in range(rows):
			self.board.append([])
			for col in range(cols):
				if row == 0 and (col == 0 or col == 7):
					self.board[row].append(Piece(row, col, black, rook))
				elif row == 7 and (col == 0 or col == 7):
					self.board[row].append(Piece(row, col, white, rook))
				elif row == 0 and (col == 1 or col == 6):
					self.board[row].append(Piece(row, col, black, knight))
				elif row == 7 and (col == 1 or col == 6):
					self.board[row].append(Piece(row, col, white, knight))
				elif row == 0 and (col == 2 or col == 5):
					self.board[row].append(Piece(row, col, black, bishop))
				elif row == 7 and (col == 2 or col == 5):
					self.board[row].append(Piece(row, col, white, bishop))
				elif row == 0 and col == 3:
					self.board[row].append(Piece(row, col, black, queen))
				elif row == 7 and col == 3:
					self.board[row].append(Piece(row, col, white, queen))
				elif row == 0 and col == 4:
					self.board[row].append(Piece(row, col, black, king))
				elif row == 7 and col == 4:
					self.board[row].append(Piece(row, col, white, king))
				elif row == 1:
					self.board[row].append(Piece(row, col, black, pawn))
				elif row == 6:
					self.board[row].append(Piece(row, col, white, pawn))
				else:
					self.board[row].append(0)

	def move(self, piece, row, col):
		color, rank = piece.__repr__()
		if rank == king:
			right_moves =  self._castling_right(piece.row, piece.col, color)
			left_moves = self._castling_left(piece.row, piece.col, color)
			if (row, col) in right_moves:
				right_rook = self.get_piece(row, 7)
				self.board[right_rook.row][right_rook.col], self.board[piece.row][piece.col+1] = self.board[piece.row][piece.col+1], self.board[right_rook.row][right_rook.col]
				right_rook.move(piece.row, piece.col+1)
				if color == white:
					self.white_rook_right_moved = True
				else:
					self.black_rook_right_moved = True
			elif (row, col) in left_moves:
				left_rook = self.get_piece(row, 0)
				self.board[left_rook.row][left_rook.col], self.board[piece.row][piece.col-1] = self.board[piece.row][piece.col-1], self.board[left_rook.row][left_rook.col]
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

		self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
		piece.move(row, col)

		if rank == pawn:
			if row == 0 or row == 7:
				ans = input("What do you want to promote to?(q, b, r, k): ")
				if ans == "q":
					if color == white:
						self.board[row][col] = Piece(row, col, white, queen)
						self.board[row][col].draw_queen(Window, color)
					else:
						self.board[row][col] = Piece(row, col, black, queen)
						self.board[row][col].draw_queen(Window, color)
				elif ans == "b":
					if color == white:
						self.board[row][col] = Piece(row, col, white, bishop)
						self.board[row][col].draw_bishop(Window, color)
					else:
						self.board[row][col] = Piece(row, col, black, bishop)
						self.board[row][col].draw_bishop(Window, color)
				elif ans == "r":
					if color == white:
						self.board[row][col] = Piece(row, col, white, rook)
						self.board[row][col].draw_rook(Window, color)
					else:
						self.board[row][col] = Piece(row, col, black, rook)
						self.board[row][col].draw_rook(Window, color)
				else:
					if color == white:
						self.board[row][col] = Piece(row, col, white, knight)
						self.board[row][col].draw_knight(Window, color)
					else:
						self.board[row][col] = Piece(row, col, black, knight)
						self.board[row][col].draw_knight(Window, color)

		if color == black:
			self.is_white_check = is_check(self, white)

		if color == white:
			self.is_black_check = is_check(self, black)			

	def get_piece(self, row, col):
		return self.board[row][col]

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

	def remove(self, row, col):
		self.board[row][col] = 0

	def get_valid_moves(self, piece, condition=True):
		moves = []
		color, rank = piece.__repr__()
		col = piece.col
		row = piece.row
		if rank == pawn:
			if color == white:
				moves.extend(self._white_pawn(row, col))
			else:
				moves.extend(self._black_pawn(row, col))
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


		if color == white:
			if condition == True:
				for move in moves:
					temp_board = copy.deepcopy(self)
					temp_piece = copy.deepcopy(piece)
					new_board = simulate_move(temp_piece, temp_board, move)
					opp_moves = get_all_valid_moves(new_board, black)
					for opp_move in opp_moves:
						new_piece = new_board.get_piece(opp_move[0], opp_move[1])
						if new_piece != 0 and new_piece.rank == king:
							copy_moves.remove(move)
							
		elif color == black:
			if condition == True:
				for move in moves:
					temp_board = copy.deepcopy(self)
					temp_piece = copy.deepcopy(piece)
					new_board = simulate_move(temp_piece, temp_board, move)
					opp_moves = get_all_valid_moves(new_board, white)
					for opp_move in opp_moves:
						new_piece = new_board.get_piece(opp_move[0], opp_move[1])
						if new_piece != 0 and new_piece.rank == king:
							copy_moves.remove(move)
				
		moves = copy_moves
		return moves

	def _castling_left(self, row, col, color):
		moves = []
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

	def _castling_right(self, row, col, color):
		moves = [] 
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

	def _black_pawn(self, row, col):
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
			if right_space != 0 and right_space.color == white:
				moves.append(right_diag)
		if 8>row+1>-1 and 8>col-1>-1:
			left_space = self.get_piece(left_diag[0], left_diag[1])
			if left_space != 0 and left_space.color == white:
				moves.append(left_diag)
	
		return moves

	def _white_pawn(self, row, col):
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
			if right_space != 0 and right_space.color == black:
				moves.append(right_diag)
		if 8>row-1>-1 and 8>col-1>-1:
			left_space = self.get_piece(left_diag[0], left_diag[1])
			if left_space != 0 and left_space.color != white:
				moves.append(left_diag)

		return moves

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

class Piece():
	def __init__(self, row, col, color, rank):
		self.row = row
		self.col = col
		self.color = color
		self.rank = rank
		self.x = 0
		self.y = 0
		self.calc_pos()

	def calc_pos(self):
		self.x = self.col*square_size + square_size//2
		self.y = self.row*square_size + square_size//2

	def draw_king(self, win, color):
		if color == white:
			win.blit(w_king, (self.x-w_king.get_width()//2, self.y-w_king.get_height()//2))
		else:
			win.blit(b_king, (self.x-b_king.get_width()//2, self.y-b_king.get_height()//2))

	def draw_queen(self, win, color):
		if color == white:
			win.blit(w_queen, (self.x-w_queen.get_width()//2, self.y-w_queen.get_height()//2))
		else:
			win.blit(b_queen, (self.x-b_queen.get_width()//2, self.y-b_queen.get_height()//2))

	def draw_pawn(self, win, color):
		if color == white:
			win.blit(w_pawn, (self.x-w_pawn.get_width()//2, self.y-w_pawn.get_height()//2))
		else:
			win.blit(b_pawn, (self.x-b_pawn.get_width()//2, self.y-b_pawn.get_height()//2))

	def draw_knight(self, win, color):
		if color == white:
			win.blit(w_knight, (self.x-w_knight.get_width()//2, self.y-w_knight.get_height()//2))
		else:
			win.blit(b_knight, (self.x-b_knight.get_width()//2, self.y-b_knight.get_height()//2))

	def draw_rook(self, win, color):
		if color == white:
			win.blit(w_rook, (self.x-w_rook.get_width()//2, self.y-w_rook.get_height()//2))
		else:
			win.blit(b_rook, (self.x-b_rook.get_width()//2, self.y-b_rook.get_height()//2))

	def draw_bishop(self, win, color):
		if color == white:
			win.blit(w_bishop, (self.x-w_bishop.get_width()//2, self.y-w_bishop.get_height()//2))
		else:
			win.blit(b_bishop, (self.x-b_bishop.get_width()//2, self.y-b_bishop.get_height()//2))

	def move(self, row, col):
		self.row = row
		self.col = col
		self.calc_pos()

	def __repr__(self):
		return str(self.color), str(self.rank)

class Game():
	def __init__(self, win):
		self._init()
		self.win = win

	def update(self):
		self.board.draw(self.win)
		self.draw_valid_moves(self.valid_moves)
		pygame.display.update()

	def _init(self):
		self.selected = None
		self.board = Board()
		self.valid_moves = []
		self.turn = white

	def reset(self):
		self._init()

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

	def _move(self, row, col):
		piece = self.board.get_piece(row, col)
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

	def change_turn(self):
		self.valid_moves = []
		if self.turn == white:
			self.turn = black
		else:
			self.turn = white

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

def get_all_valid_moves(board, color):
		all_valid_moves = []
		pieces = get_all_pieces(board, color)
		for piece in pieces:
			valid_moves = board.get_valid_moves(piece, False)
			all_valid_moves.extend(valid_moves)

		return all_valid_moves

def get_all_pieces(board, color):
		pieces = []
		for row in board.board:
			for piece in row:
				if piece != 0 and piece.color == color:
					pieces.append(piece)
		return pieces

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

def simulate_move(piece, board, move):
	space = board.get_piece(move[0], move[1])
	if space != 0:
		board.remove(space.row, space.col)
	board.board[piece.row][piece.col], board.board[move[0]][move[1]] = board.board[move[0]][move[1]], board.board[piece.row][piece.col]
	piece.move(move[0], move[1])
	return board

def get_pos_from_mouse(pos):
	x, y = pos
	row = y//square_size
	col = x//square_size
	return row, col

def main():
	run = True
	clock = pygame.time.Clock()
	game = Game(Window)

	while run:
		clock.tick(fps)

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