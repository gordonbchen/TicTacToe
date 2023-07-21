import numpy as np

from hashlib import sha256

from tic_tac_toe import Move, Board, Codes


class Minimax():
    """An agent that plays tic-tac-toe using minimax."""

    def __init__(self, original_state: np.ndarray) -> None:
        """Initialize the minimax tree for tic-tac-toe."""
        self.state_eval_map = {}
        self._calc_eval(original_state)

    def _calc_eval(self, curr_state: np.ndarray) -> float:
        """
        Use minimax to recursively calculate the eval at the current state.
        Store the eval in the state eval map.
        """
        # Hash state to store in dict.
        state_hash = self._hash_state(curr_state)

        # Check if the state is already in the dict.
        if state_hash in self.state_eval_map:
            eval = self.state_eval_map[state_hash]
            return eval

        # Check if the game is won.
        winner = Board.check_win(curr_state)
        if winner is not None:
            self.state_eval_map[state_hash] = winner
            return winner

        # Check if the game is a tie.
        # NOTE: crazy bug when checking (tie is True).
        if Board.check_tie(curr_state):
            # TODO: 0 to 1 vs. -1 to 1.
            self.state_eval_map[state_hash] = Codes.TIE
            return Codes.TIE

        # Get evals of children.
        child_states = Board.get_poss_states(curr_state)
        child_evals = [self._calc_eval(child_state) for child_state in child_states]

        # Get minimax-based eval.
        if Board.get_n_move(curr_state) % 2 == 1:
            eval = np.max(child_evals)
        else:
            # BUG: empty child states and evals.
            eval = np.min(child_evals)

        # Create entry in minimax tree.
        self.state_eval_map[state_hash] = eval
        return eval

    def _hash_state(self, state: np.ndarray) -> str:
        """Return the hash of the state. Used to store np arrays in a dict."""
        state_str = str(state)
        state_hash = sha256(state_str.encode()).hexdigest()
        return state_hash

    def get_move(self, state: np.ndarray) -> Move:
        """Get the best move at the current state."""
        # Get child states, hashes, and evals.
        child_states = Board.get_poss_states(state)
        child_hashes = [self._hash_state(child_state) for child_state in child_states]
        child_evals = [self.state_eval_map[child_hash] for child_hash in child_hashes]

        # Get index of best eval.
        if Board.get_n_move(state) % 2 == 1:
            best_eval_ind = np.argmax(child_evals)
        else:
            best_eval_ind = np.argmin(child_evals)

        # Get move corresponding to the best eval.
        best_state = child_states[best_eval_ind]
        best_move = Board.get_move(state, best_state)

        return best_move
