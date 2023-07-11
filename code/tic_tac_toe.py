import numpy as np

from typing import Union, Dict, NamedTuple


class Move(NamedTuple):
    """A data struct to represent a tic-tac-toe move."""

    n_row: int
    n_col: int


class Codes:
    """A class to store game codes like markers and outcomes."""

    EMPTY = 0

    X_MARK = 1
    TIE = 0
    O_MARK = -1


class Board:
    """A Tic Tac Toe board."""

    SIDE_LENGTH = 3

    def __init__(self) -> None:
        """Initialize the empty board."""
        self.state = np.full(
            shape=(Board.SIDE_LENGTH, Board.SIDE_LENGTH), fill_value=Codes.EMPTY
        )

    def make_move(self, move: Move) -> None:
        """Make a move."""
        # Check that the square is empty.
        assert (
            self.state[move.n_row, move.n_col] == Codes.EMPTY
        ), f"{move} is not an empty square!"

        # Fill square with marker.
        marker = Board.get_marker(self.state)
        self.state[move.n_row, move.n_col] = marker

    def get_marker(state: np.ndarray) -> int:
        """Return the marker of the player whose turn it is."""
        n_move = Board.get_n_move(state)

        # X if the turn is odd, O if even.
        if n_move % 2 == 1:
            return Codes.X_MARK
        else:
            return Codes.O_MARK

    def get_n_move(state: np.ndarray) -> int:
        """Find the move number based on the # of empty squares. Starts on move 1."""
        n_move = (9 - Board.get_n_empty(state)) + 1
        return n_move

    def get_n_empty(state: np.ndarray) -> int:
        """Find the number of empty squares."""
        n_empty = np.sum(state == Codes.EMPTY)
        return n_empty

    def check_win(state: np.ndarray) -> Union[None, int]:
        """Check if there is a winner."""
        # A player has won if their marker is the mean of a slice.
        # Take row, column means.
        row_means = state.mean(axis=1)
        col_means = state.mean(axis=0)

        # Get diagonals and take means.
        diags = Board.get_diags(state)
        diag_means = diags.mean(axis=1)

        # Put slice means together.
        slice_means = [row_means, col_means, diag_means]

        # Check if either player marker is in the means.
        for means in slice_means:
            for marker in [Codes.O_MARK, Codes.X_MARK]:
                if marker in means:
                    return marker
        return None

    def get_diags(state: np.ndarray) -> np.ndarray:
        """Get board diagonals."""
        inds = np.arange(Board.SIDE_LENGTH)

        # Get diagonals.
        neg_slope_diag = state[inds, inds]
        pos_slope_diag = state[inds, inds[::-1]]

        # Put diagonals together in np array.
        diags = np.stack((neg_slope_diag, pos_slope_diag), axis=0)
        return diags

    def check_tie(state: np.ndarray) -> bool:
        """Check if the board is a tie game. Check after checking win."""
        n_empty = Board.get_n_empty(state)
        return n_empty == 0

    def get_move_state_map(state: np.ndarray) -> Dict[Move, np.ndarray]:
        """Return a list of all possible next moves."""
        move_state_map = {}
        for n_row, row in enumerate(state):
            for n_col, square in enumerate(row):
                # A move is possible if the square is empty.
                if square == Codes.EMPTY:
                    poss_move = Move(n_row, n_col)
                    poss_state = Board.simulate_move(poss_move, state)

                    move_state_map[poss_move] = poss_state

        return move_state_map

    def simulate_move(move: Move, state: np.ndarray) -> np.ndarray:
        """Get the board state after the move."""
        # Make the move.
        marker = Board.get_marker(state)

        # Create state copy.
        poss_state = state.copy()
        poss_state[move.n_row, move.n_col] = marker

        return poss_state
