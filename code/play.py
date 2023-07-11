from __future__ import annotations

import numpy as np

from typing import Union, List

from tic_tac_toe import Board, Codes, Move


class Node:
    """A minimax node storing an eval and children nodes."""

    def __init__(
        self,
        state: np.ndarray,
        eval: int,
        children: Union[None, List[Node]],
        use_max: bool,
    ) -> None:
        """Create the node."""
        self.state = state
        self.eval = eval
        self.children = children
        self.use_max = use_max

    def get_best_move(self) -> Move:
        """Get the best move at the current state."""
        # Find best eval.
        poss_evals = [child.eval for child in self.children]
        best_eval = max(poss_evals) if self.use_max is True else min(poss_evals)
        best_eval_ind = poss_evals.index(best_eval)

        # Find state with best eval.
        poss_states = [child.state for child in self.children]
        best_state = poss_states[best_eval_ind]

        # Find move getting best state.
        best_move = Board.get_move(self.state, best_state)
        return best_move

    def get_child(self, state) -> Node:
        """Get the child with the given state."""
        for child in self.children:
            if np.all(child.state == state):
                return child


def create_minimax_tree(state: np.ndarray, use_max: bool) -> Node:
    """Create a minmax tree."""
    # Base cases of win and tie.
    winner = Board.check_win(state)
    if winner is not None:
        # Marks correspond to score: x = 1, o = -1.
        node = Node(state, eval=winner, children=None, use_max=(not use_max))
        return node
    elif Board.check_tie(state):
        # Tie corresponds to 0 score.
        node = Node(state, 0, children=None, use_max=(not use_max))
        return node

    # Recursively get eval of children nodes.
    poss_states = Board.get_poss_states(state)
    children = [
        create_minimax_tree(poss_state, use_max=(not use_max))
        for poss_state in poss_states
    ]

    # Get eval from children.
    poss_evals = [child.eval for child in children]
    best_eval = max(poss_evals) if use_max is True else min(poss_evals)

    # Create node.
    node = Node(state, best_eval, children, use_max=(use_max))
    return node


def play_game() -> None:
    """Play a game against minimax."""
    # Create new board.
    board = Board()

    # Create minimax tree.
    node = create_minimax_tree(board.state, use_max=True)

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
            move = node.get_best_move()

            board.make_move(move)

        # Update node.
        node = node.get_child(board.state)

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
