import numpy as np

from typing import Union, List, Dict, NamedTuple


class Move(NamedTuple):
    """A data struct to represent a tic-tac-toe move."""
    n_row: int
    n_col: int


class Markers:
    """A class to store player and empty markers."""
    EMPTY_MARKER = 0

    O_MARKER = 1
    X_MARKER = -1
    PLAYER_MARKERS = [O_MARKER, X_MARKER]


class Board:
    """A Tic Tac Toe board."""
    SIDE_LENGTH = 3

    def __init__(self) -> None:
        """Initialize the board."""
        self.reset_board()

    def reset_board(self) -> None:
        """Create an empty board."""
        # Fill the board with zeros (empty).
        self.board = np.full(
            shape=(Board.SIDE_LENGTH, Board.SIDE_LENGTH),
            fill_value=Markers.EMPTY_MARKER
        )

        # Keep track of the move the board is on.
        self.n_move = 0

    def make_move(self, move: Move) -> None:
        """Make a move."""
        # Fill square with marker.
        marker = self.get_marker()
        self.board[move.n_row, move.n_col] = marker

        # Increment moves.
        self.n_move += 1

    def get_marker(self) -> int:
        """Return the marker of the player whose turn it is."""
        # O if the turn # is even, X if odd.
        if (self.n_move % 2 == 0):
            return Markers.O_MARKER
        else:
            return Markers.X_MARKER

    def check_win(self) -> Union[None, int]:
        """Check if there is a winner."""
        # A player has won if their marker is the mean of a slice.
        # Take row, column means.
        row_means = self.board.mean(axis=1)
        col_means = self.board.mean(axis=0)

        # Get diagonals and take means.
        diags = self.get_diags()
        diag_means = diags.mean(axis=1)

        # Put slice means together.
        slice_means = [row_means, col_means, diag_means]

        # Check if either player marker is in the means.
        for marker in Markers.PLAYER_MARKERS:
            for means in slice_means:
                if (marker in means):
                    return marker
        return None

    def get_diags(self) -> np.ndarray:
        """Get board diagonals."""
        inds = np.arange(Board.SIDE_LENGTH)

        # Get diagonals.
        neg_slope_diag = self.board[inds, inds]
        pos_slope_diag = self.board[inds, inds[::-1]]

        # Put diagonals together in np array.
        diags = np.stack((neg_slope_diag, pos_slope_diag), axis=0)
        return diags
    
    def check_tie(self) -> bool:
        """Check if the board is a tie game."""
        # Tie games can only happen on move 8.
        is_tie = (self.n_move == 8)
        return is_tie

    def get_move_state_map(self) -> Dict[Move, str]:
        """Find all possible next moves and corresponding board states."""
        possible_moves = self.get_possible_moves()
        possible_states = [self.simulate_move(move) for move in possible_moves]

        move_state_map = dict(zip(possible_moves, possible_states))
        return move_state_map

    def get_possible_moves(self) -> List[Move]:
        """Return a list of all possible next moves."""
        possible_moves = []
        for (n_row, row) in enumerate(self.board):
            for (n_col, square) in enumerate(row):
                # A move is possible if the square is empty.
                if (square == Markers.EMPTY_MARKER):
                    possible_move = Move(n_row, n_col)
                    possible_moves.append(possible_move)

        return possible_moves
                    
    def simulate_move(self, move: Move) -> str:
        """Get the board state after the move."""
        # Make the move.
        marker = self.get_marker()
        self.board[move.n_row, move.n_col] = marker

        # Get the board state.
        next_state = self.get_board_state()

        # Unmake the move (more efficient).
        self.board[move.n_row, move.n_col] = Markers.EMPTY_MARKER

        return next_state

    def get_board_state(self) -> str:
        """Get the str representation of the board state. Used for storing arrays in dict."""
        state = "".join([str(i) for i in np.ravel(self.board)])
        return state
