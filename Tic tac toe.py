import random

def initialize_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("---------")

def check_win(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):  
            return True
        if all(board[j][i] == player for j in range(3)):  
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):  
        return True
    return False

def check_draw(board):
    return all(spot in ['X', 'O'] for row in board for spot in row)

def get_empty_positions(board):
    return [(row, col) for row in range(3) for col in range(3) if board[row][col] == ' ']

def computer_move(board):
    empty_positions = get_empty_positions(board)
    return random.choice(empty_positions)

def valid_input(row, col, board):
    return 0 <= row < 3 and 0 <= col < 3 and board[row][col] == ' '

def player_move(board, current_player):
    while True:
        try:
            row = int(input(f"Player {current_player}, enter the row (0, 1, or 2): "))
            col = int(input(f"Player {current_player}, enter the column (0, 1, or 2): "))
            if valid_input(row, col, board):
                board[row][col] = current_player
                break
            else:
                print("Invalid move! Try again.")
        except ValueError:
            print("Invalid input! Please enter numbers between 0 and 2.")

def play_again():
    while True:
        play_again_input = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again_input in ['yes', 'no']:
            return play_again_input == 'yes'
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

def tic_tac_toe():
    while True:
        board = initialize_board()
        current_player = "X"

        game_mode = input("Choose game mode: 1 for Player vs Player, 2 for Player vs Computer: ").strip()
        while game_mode not in ['1', '2']:
            game_mode = input("Invalid choice. Choose game mode: 1 for Player vs Player, 2 for Player vs Computer: ").strip()

        while True:
            print_board(board)

            if game_mode == '1':
                player_move(board, current_player)
            else:
                if current_player == "X":
                    player_move(board, current_player)
                else:
                    row, col = computer_move(board)
                    print(f"Computer chose: {row}, {col}")
                    board[row][col] = current_player

            if check_win(board, current_player):
                print_board(board)
                print(f"{'Player 1' if current_player == 'X' else 'Player 2' if game_mode == '1' else 'Computer'} wins!")
                break

            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break

            current_player = "O" if current_player == "X" else "X"
        if not play_again():
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    tic_tac_toe()
