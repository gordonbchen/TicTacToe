import numpy as np

from tic_tac_toe import Move


class Human():
    """A human agent that plays tic-tac-toe."""

    def __init__(self) -> None:
        """initialize the human player."""
        pass

    def get_move(self, state: np.ndarray) -> Move:
        """Get the human's move."""
        n_row, n_col = (int(char) for char in input("Row, Col: ").split(", "))
        move = Move(n_row, n_col)
        return move
