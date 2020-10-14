import numpy as np
import random
import pygame
import sys
import math

COLOR = (0,0,128)
BLACK = (0,0,0)
YELLOW = (240,230,140)
RED = (220,20,60)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

EMPTY = 0
WINDOW_LENGTH = 4
DEPTH = 3

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check Horizontal 
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check Vertical
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check Diagonal /
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check Diagonal \
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True


def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE

	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
				score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 10
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 5

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -=80

	return score

def score_position(board, piece):

	score = 0
	# Score Center
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count*6


	# Score Horizontal 
	
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r, :])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]

			score += evaluate_window(window, piece)


	# Score Vertical 
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:, c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]

			score += evaluate_window(window, piece)

	#Score Diagonal /
	for r in range (ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]

			score += evaluate_window(window, piece)

	#Score Diagonal \
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]

			score += evaluate_window(window, piece)


	return score

def is_terminal_node(board):

	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):

	valid_locations= get_valid_locations(board)
	terminal_node = is_terminal_node(board)

	if depth == 0 or terminal_node:
		if terminal_node:
			if winning_move(board, AI_PIECE):
				return (None, 100000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -100000000)
			else: # NO VALID MOVES
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))

	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col

			alpha = max(alpha, value)#Score Diagonal /
			if alpha >= beta:
				break
		return column, value

	else: # MINIMIZING PLAYER
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value


def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):
	
	valid_locations = get_valid_locations(board)
	best_score = 0	
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col
	

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, COLOR, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
			
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE:
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
			
	pygame.display.update()

board = create_board()
game_over = False

turn = 0
print_board(board)





pygame.init()

SQUARE_SIZE = 100	
RADIUS = int(SQUARE_SIZE/2 - 5)

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE
size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)




while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx,int(SQUARE_SIZE/2)), RADIUS)
			
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			print(event.pos)
			# #Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARE_SIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)

					if winning_move(board, PLAYER_PIECE):

						pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
						label = myfont.render("Player 1 Wins!", 1, RED)
						screen.blit(label, (40, 10))
						print("Player 1 Wins!!!")
						game_over = True
					
					turn += 1
					turn = turn % 2

					draw_board(board)
					print_board(board)



	#Ask for Player 2 Input
	if turn == AI and not game_over:
		# col = random.randint(0, COLUMN_COUNT-1)
		# col = pick_best_move(board, AI_PIECE)

		pygame.time.wait(300)
		col, minimax_score = minimax(board, DEPTH, -math.inf, math.inf, True)

		if is_valid_location(board, col):
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if winning_move(board, AI_PIECE):
				pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
				label = myfont.render("AI Wins!", 1, YELLOW)
				screen.blit(label, (40, 10))
				print("AI Wins!!!")
				game_over = True


			print_board(board)
			draw_board(board)
			
			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)


	