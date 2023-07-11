import numpy as np

from tic_tac_toe import Board, Codes, Move


def get_eval(state: np.ndarray, use_max: bool) -> int:
    """Get the state evaluation using minimax."""
    # Base cases of win and tie.
    winner = Board.check_win(state)
    if winner is not None:
        # Marks correspond to score: x = 1, o = -1.
        return winner
    elif Board.check_tie(state):
        # Tie corresponds to 0 score.
        return Codes.TIE

    # Get possible children evals.
    move_state_map = Board.get_move_state_map(state)

    # Recursively get eval of children states.
    poss_states = move_state_map.values()
    poss_evals = [
        get_eval(poss_state, use_max=(not use_max)) for poss_state in poss_states
    ]

    # Return min or max.
    if use_max is True:
        return max(poss_evals)
    else:
        return min(poss_evals)


def get_best_move(state: np.ndarray, use_max: bool) -> Move:
    """Get the best move at the state."""
    # Get moves and corresponding states.
    move_state_map = Board.get_move_state_map(state)
    poss_moves = list(move_state_map.keys())
    poss_states = move_state_map.values()

    # Get evals of children.
    poss_evals = [
        get_eval(poss_state, use_max=(not use_max)) for poss_state in poss_states
    ]

    # Get best state index.
    if use_max is True:
        best_eval = max(poss_evals)
    else:
        best_eval = min(poss_evals)

    best_state_ind = poss_evals.index(best_eval)

    # Map best state back to best move.
    best_move = poss_moves[best_state_ind]
    return best_move


def play_game(human_first: bool) -> None:
    """Play a game against minimax."""
    # Create new board.
    board = Board()

    # Play game for 9 turns (max).
    for n_turn in range(1, 10):
        # Show the board.
        print(f"\nTurn {n_turn}:")
        print(board.state)

        if n_turn % 2 == human_first:
            # Human player turn.
            n_row = int(input("Row: "))
            n_col = int(input("Col: "))
            move = Move(n_row, n_col)

            # Make move.
            board.make_move(move)
        else:
            # Computer player turn.
            move = get_best_move(board.state, use_max=(human_first is False))

            # Make move.
            board.make_move(move)

        # Show board.
        print(board.state)

        # Check if the game is over.
        winner = Board.check_win(board.state)
        if winner == Codes.X_MARK:
            print("X won!")
            break
        elif winner == Codes.O_MARK:
            print("O won!")
            break
        elif Board.check_tie(board.state):
            print("TIE game!")
            break


if __name__ == "__main__":
    # Play the game.
    for i in range(3):
        human_first = i % 2 == 1
        play_game(human_first)
