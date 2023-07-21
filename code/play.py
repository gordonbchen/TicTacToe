from tic_tac_toe import Board, Codes, Move
from agents.minimax import Minimax


def play_game() -> None:
    """Play a game of tic-tac-toe.."""
    # Create new board.
    board = Board()

    # Create minimax agent.
    minimax_agent = Minimax(board.state)

    # Play game for 9 turns (max).
    for n_turn in range(1, 10):
        # Show the board.
        print(f"\nTurn {n_turn}:")
        print(board.state)

        if n_turn % 2 == 1:
            # Human player turn.
            n_row, n_col = (int(char) for char in input("Row, Col: ").split(", "))
            move = Move(n_row, n_col)

            board.make_move(move)
        else:
            # Computer player turn.
            move = minimax_agent.get_move(board.state)

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
    # Play tic-tac-toe.
    play_game()
