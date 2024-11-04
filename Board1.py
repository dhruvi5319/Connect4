import time
import numpy as np
import pygame
import sys
import math
import random

GRAY = (128, 128, 128)  # Background color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def draw_board(board, board_color):
   
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, board_color, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, GRAY, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, player_color, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, ai_color, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def ai_move(board):
    valid_moves = [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]
    for col in valid_moves:
        row = get_next_open_row(board, col)
        # Try placing the AI's piece and check if it wins
        drop_piece(board, row, col, 2)
        if winning_move(board, 2):
            return col  # AI wins, so play in this column
        # Undo the move
        board[row][col] = 0

    for col in valid_moves:
        row = get_next_open_row(board, col)
        # Try placing the player's piece and check if they win
        drop_piece(board, row, col, 1)
        if winning_move(board, 1):
            board[row][col] = 0  # Undo the move
            return col  # Block player's winning move by playing in this column
        # Undo the move
        board[row][col] = 0

    # If no winning/losing move, choose randomly
    return random.choice(valid_moves) if valid_moves else None


board = create_board()
print_board(board)
game_over = False
turn = 0

# Initialize pygame
pygame.init()

# Define our screen size
SQUARESIZE = 100

# Define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
# # Calling function draw_board again
# draw_board(board, GRAY)
# pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

# Get player's name and coin color
player_name = input("Enter your name: ")

# Get the board color from the provided palette
print("Select the board color from the palette: Mustard, Lemon, Golden Yellow, Amber, Yellow Orange, Marigold, Saffron, Butter, Golden Beige, Beige, Tan, Khaki, Olive Yellow, Goldenrod, Golden Brown, Golden Oak")
board_color = input("Enter the board color name (e.g., Mustard): ").strip().lower()

color_codes = {
    "mustard": (255, 255, 153),
    "lemon": (255, 255, 102),
    "golden yellow": (255, 204, 0),
    "amber": (255, 191, 0),
    "yellow orange": (255, 153, 0),
    "marigold": (255, 153, 51),
    "saffron": (255, 153, 102),
    "butter": (255, 204, 153),
    "golden beige": (255, 204, 102),
    "beige": (255, 204, 153),
    "tan": (230, 184, 115),
    "khaki": (204, 187, 153),
    "olive yellow": (204, 170, 51),
    "goldenrod": (218, 165, 32),
    "golden brown": (153, 101, 21),
    "golden oak": (115, 76, 0)
}

# Set the BOARD_COLOR based on the user's choice
BOARD_COLOR = color_codes.get(board_color, GRAY)
# Calling function draw_board again
draw_board(board, BOARD_COLOR)
pygame.display.update()

if BOARD_COLOR == GRAY:
    print("Invalid color name. Using default gray color.")

player_coin_color = input("Choose your coin color (White or Black): ").strip().lower()
if player_coin_color == "white":
    player_color = WHITE
    ai_color = BLACK
elif player_coin_color == "black":
    player_color = BLACK
    ai_color = WHITE
else:
    print("Invalid color choice. Using default colors.")
    player_color = BLACK
    ai_color = WHITE

# Select the first player
first_player = input(f"Who should go first? ({player_name} or AI): ").lower()
if first_player == "ai":
    turn = 1
else:
    turn = 0

# Get the search depth for the minimax algorithm
search_depth = int(input("How deep is the search for the Minimax [1-5]? "))
if search_depth < 1 or search_depth > 5:
    print("Invalid search depth. Using default value of 3.")
    search_depth = 3

start_time = time.time()  # Record the start time of the game

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, GRAY, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, player_color, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, ai_color, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
            pygame.draw.rect(screen, GRAY, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    label = myfont.render(f"{player_name} wins!!", 1, player_color)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn += 1
                turn = turn % 2

                print_board(board)
                draw_board(board, BOARD_COLOR)

        # AI's move
        if turn == 1 and not game_over:
            col = ai_move(board)
            if col is not None:
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    label = myfont.render("AI wins!!", 1, ai_color)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn += 1
                turn = turn % 2

                print_board(board)
                draw_board(board, BOARD_COLOR)

    if game_over:
        pygame.time.wait(3000)

        # Calculate game duration
        end_time = time.time()
        game_duration = end_time - start_time
        game_duration_str = f"Game Duration: {game_duration:.2f} seconds"
        label = myfont.render(game_duration_str, 1, BLACK)
        screen.blit(label, (50, height + 20))
        pygame.display.update()

        # Show the winner and game duration
        winner_name = "AI" if turn == 0 else player_name
        print(f"The winner is {winner_name}!")
        print(f"Game Duration: {game_duration:.2f} seconds")
        # Code to calculate and display the number of moves

pygame.quit()
