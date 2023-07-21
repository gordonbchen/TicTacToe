import numpy as np

from tic_tac_toe import Move


class Agent:
    """An interface defining a tic-tac-toe playing agent."""

    def get_move(state: np.ndarray) -> Move:
        """Get the agent's move at the given state."""
        pass
