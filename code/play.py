from tic_tac_toe import Board, Codes

from agents.agent import Agent
from agents.human import Human
from agents.minimax import Minimax


def play_game(agent_1: Agent, agent_2: Agent) -> None:
    """Play a game of tic-tac-toe.."""
    # Create new board.
    board = Board()

    # Play game for 9 turns (max).
    for n_turn in range(1, 10):
        # Get the agent that will be making a move.
        is_odd_move = Board.get_n_move(board.state) % 2 == 1
        moving_agent = agent_1 if is_odd_move else agent_2

        # Show the board.
        print(f"\nTurn {n_turn}: {moving_agent}")
        print(board.state)

        # Get the agent's move and make it.
        move = moving_agent.get_move(board.state)
        board.make_move(move)

        # Show board.
        print(board.state)

        # Check if the game is over.
        winner = Board.check_win(board.state)
        if winner == Codes.X_MARK:
            print(f"{agent_1} (X) won!")
            break
        elif winner == Codes.O_MARK:
            print(f"{agent_2} (O) won!")
            break
        elif Board.check_tie(board.state):
            print("TIE game!")
            break


if __name__ == "__main__":
    # Create agents.
    human_agent = Human("Gordon")
    minimax_agent = Minimax()

    # Play tic-tac-toe.
    play_game(human_agent, minimax_agent)
