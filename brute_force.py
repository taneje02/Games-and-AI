import itertools

def check_winner(board):
    """Checks if there is a winner in the given board state."""
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
                      (0, 4, 8), (2, 4, 6)]  # Diagonals

    for condition in win_conditions:
        a, b, c = condition
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]  # Return winner ('X' or 'O')
    return None  # No winner

def get_available_moves(board):
    """Returns available moves on the board."""
    return [i for i, v in enumerate(board) if v == " "]

def brute_force_best_move(board, player):
    """Finds the best move using brute force by simulating all possible outcomes."""
    best_move = None
    best_score = -float('inf')

    for move in get_available_moves(board):
        new_board = board[:]
        new_board[move] = player
        if check_winner(new_board) == player:
            return move  # Immediate winning move
        opponent = "O" if player == "X" else "X"

        # Simulate all opponent moves
        opponent_moves = get_available_moves(new_board)
        if not opponent_moves:  # If no moves left, it's a draw
            score = 0
        else:
            worst_score = float('inf')
            for opp_move in opponent_moves:
                temp_board = new_board[:]
                temp_board[opp_move] = opponent
                if check_winner(temp_board) == opponent:
                    worst_score = -1  # Losing move
                    break
                worst_score = min(worst_score, 0)

            score = -worst_score  # Maximize the worst possible outcome

        if score > best_score:
            best_score = score
            best_move = move

    return best_move

# Example usage
board = ["X", "O", "X",
         " ", "O", " ",
         " ", " ", "X"]

best_move = brute_force_best_move(board, "O")
print(f"Best move for 'O': {best_move}")
