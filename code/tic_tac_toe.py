import numpy as np

from typing import Union, List, Dict, NamedTuple


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
            shape=(Board.SIDE_LENGTH, Board.SIDE_LENGTH),
            fill_value=Codes.EMPTY
        )

    def make_move(self, move: Move) -> None:
        """Make a move."""
        # Fill square with marker.
        marker = self.get_marker(self.board)
        self.state[move.n_row, move.n_col] = marker

        # Increment moves.
        self.n_move += 1

    def get_n_move(state: np.ndarray) -> int:
        """Find the move number based on the # of empty squares. Starts on move 1."""
        n_move = (9 - state.count(Codes.EMPTY)) + 1
        return n_move    

    def get_marker(state: np.ndarray) -> int:
        """Return the marker of the player whose turn it is."""
        # X if the turn is even, O if odd.
        if (self.n_move % 2 == 0):
            return Codes.X_MARK
        else:
            return Codes.O_MARK

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
        for marker in [Codes.O_MARK, Codes.X_MARK]:
            for means in slice_means:
                if (marker in means):
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
        n_empty = state.count(Codes.EMPTY)
        return (n_empty == 0)

    def get_move_state_map(state: np.ndarray) -> Dict[Move, np.ndarray]:
        """Find all possible next moves and corresponding board states."""
        possible_moves = Board.get_possible_moves(state)
        possible_states = [Board.simulate_move(move, state) for move in possible_moves]

        move_state_map = dict(zip(possible_moves, possible_states))
        return move_state_map

    def get_possible_moves(state: np.ndarray) -> List[Move]:
        """Return a list of all possible next moves."""
        possible_moves = []
        for (n_row, row) in enumerate(state):
            for (n_col, square) in enumerate(row):
                # A move is possible if the square is empty.
                if (square == Codes.EMPTY):
                    possible_move = Move(n_row, n_col)
                    possible_moves.append(possible_move)

        return possible_moves

    def simulate_move(move: Move, state: np.ndarray) -> np.ndarray:
        """Get the board state after the move."""
        # Make the move.
        marker = self.get_marker()
        self.board[move.n_row, move.n_col] = marker

        # Get the board state.
        next_state = self.get_board_state()

        # Unmake the move (more efficient).
        self.board[move.n_row, move.n_col] = Codes.EMPTY

        return next_state
