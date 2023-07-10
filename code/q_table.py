import pandas as pd
import numpy as np

from typing import List, Dict

from board import Markers, Move


class Outcomes:
    """A class to store outcome values."""
    TIE = 0

    O_WIN = Markers.O_MARKER
    X_WIN = Markers.X_MARKER


class QTable:
    """A table storing game states and evaluations."""

    def __init__(self) -> None:
        """Initialize the q-table."""
        self.table = pd.DataFrame(columns=["n_reached", "eval"])
        self.table.index.name = "state"

    def get_best_move(self, move_state_map: Dict[Move, str], marker: int) -> Move:
        """Evaluate the best move."""
        # Find the best state.
        states = move_state_map.values()
        best_state = self.get_best_state(states, marker)

        # Invert move state map to get move from state.
        state_move_map = dict(zip(move_state_map.values(), move_state_map.keys()))

        # Find the best move based on the state.
        best_move = state_move_map[best_state]
        return best_move

    def get_best_state(self, states: List[str], marker: int) -> str:
        """Evaulate the best state."""
        # Fill states without a table entry.
        state_index = pd.Index(states)
        new_states = state_index.difference(self.table.index)

        new_index = self.table.index.append(new_states)
        self.table = self.table.reindex(new_index)

        self.table.loc[new_states] = np.zeros(shape=(new_states.shape[0], 2))

        # Sort states by evals.
        state_rows = self.table.loc[states]
        sorted_states = state_rows.sort_values(by="eval", ascending=True)

        # Get best state based on which player it is.
        if (marker == Markers.O_MARKER):
            best_state = sorted_states.iloc[-1]
        else:
            best_state = sorted_states.iloc[0]

        return best_state.name

    def update(self, reached_states: List[str], outcome: int) -> None:
        """Update the q-table based on the game outcome."""
        # # Calculate linearly-increasing increments to value moves closer to the win more highly.
        # n_states = len(reached_states)
        # eval_incs = np.arange(1, n_states + 1) / n_states

        # TODO: best increment strategy.
        # BUG: q-tables.
        eval_incs = np.full(shape=len(reached_states), fill_value=1)

        if (outcome == Outcomes.X_WIN):
            # Invert increments if x won.
            eval_incs *= -1
        elif (outcome == Outcomes.TIE):
            # Make increments zero. No one should be rewarded.
            eval_incs *= 0

        # Get q-table state rows.
        table_rows = self.table.loc[reached_states]

        # Increment the number of times the state has beeen reached.
        table_rows["n_reached"] += 1

        # Update the evals with the new eval means.
        # new_mean = old_mean * (n_before / n_new) + (new_value / n_new)
        old_mean = table_rows["eval"]
        n_new = table_rows["n_reached"]
        # TODO: view vs copy problem.
        self.table.loc[reached_states, "eval"] = old_mean * (n_new / (n_new + 1)) + (eval_incs / n_new)
