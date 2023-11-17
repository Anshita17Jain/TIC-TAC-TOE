import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
LINE_WIDTH = 10
BOARD_SIZE = 3
CELL_SIZE = WIDTH // BOARD_SIZE

# Colors
BG_COLOR = (248,204,249)
LINE_COLOR = (126,75,139)
TYPE_COLOR = (0 ,0 , 0)
PLAYER_X_COLOR = (255, 0, 0)
PLAYER_O_COLOR = (0, 0, 255)
FONT = pygame.font.Font(None, 36)
BOLD_FONT = pygame.font.Font(None, 48)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Create the Tic Tac Toe board
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Function to draw the Tic Tac Toe board
def draw_board():
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)

# Function to draw X or O on the board
def draw_symbol(row, col, symbol):
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2

    if symbol == 'X':
        pygame.draw.line(screen, PLAYER_X_COLOR, (x - 50, y - 50), (x + 50, y + 50), LINE_WIDTH)
        pygame.draw.line(screen, PLAYER_X_COLOR, (x + 50, y - 50), (x - 50, y + 50), LINE_WIDTH)
    elif symbol == 'O':
        pygame.draw.circle(screen, PLAYER_O_COLOR, (x, y), 50, LINE_WIDTH)

# Function to check for a win
def check_win(symbol):
    # Check rows and columns
    for i in range(BOARD_SIZE):
        if all(board[i][j] == symbol for j in range(BOARD_SIZE)) or all(board[j][i] == symbol for j in range(BOARD_SIZE)):
            return True

    # Check diagonals
    if all(board[i][i] == symbol for i in range(BOARD_SIZE)) or all(board[i][BOARD_SIZE - 1 - i] == symbol for i in range(BOARD_SIZE)):
        return True

    return False

# Function to check if the board is full
def is_board_full():
    return all(board[i][j] != ' ' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))

# Function for AI move using minimax algorithm
def minimax(board, depth, is_maximizing):
    scores = {'X': -1, 'O': 1, 'draw': 0}

    winner = None
    if check_win('X'):
        winner = 'X'
    elif check_win('O'):
        winner = 'O'

    if winner:
        return scores[winner]

    if is_board_full():
        return scores['draw']

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval

def ai_move():
    best_score = float('-inf')
    best_move = None

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_score = minimax(board, 0, False)
                board[i][j] = ' '

                if move_score > best_score:
                    best_score = move_score
                    best_move = (i, j)

    return best_move

# Function to display the winner on the screen with bold text
def display_winner(winner):
    if winner == 'draw':
        text = BOLD_FONT.render("It's a draw!", True, TYPE_COLOR)
    else:
        text = BOLD_FONT.render(f"Player {winner} wins!", True, TYPE_COLOR)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

# Main game loop
turn = 'X'
winner = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and turn == 'X' and winner is None:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // CELL_SIZE
            clicked_col = mouseX // CELL_SIZE

            if board[clicked_row][clicked_col] == ' ':
                board[clicked_row][clicked_col] = 'X'

                if check_win('X'):
                    winner = 'X'
                elif is_board_full():
                    winner = 'draw'
                else:
                    turn = 'O'

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Reset the board when the space bar is pressed
            board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
            winner = None
            turn = 'X'

    if turn == 'O' and winner is None:
        ai_row, ai_col = ai_move()
        board[ai_row][ai_col] = 'O'

        if check_win('O'):
            winner = 'O'
        elif is_board_full():
            winner = 'draw'
        else:
            turn = 'X'

    screen.fill(BG_COLOR)
    draw_board()

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != ' ':
                draw_symbol(i, j, board[i][j])

    if winner:
        display_winner(winner)

    pygame.display.flip()