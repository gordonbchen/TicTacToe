from board import Board, Markers
from q_table import QTable, Outcomes


# Create q-table and board.
q_table = QTable()
board = Board()

# Train q-table.
n_games = 10_000
for n_game in range(n_games):
    if (n_game % 100 == 0):
        print(f"Playing game: {n_game}")

    # Reset the board.
    board.reset_board()

    # Keep tracked of reached states.
    reached_states = []

    # Play a game.
    cont_game = True
    while (cont_game):
        # Get best move.
        marker = board.get_marker()
        move_state_map = board.get_move_state_map()
        best_move = q_table.get_best_move(move_state_map, marker)

        # Make the move.
        board.make_move(best_move)

        # Add state to reached states.
        state = board.get_board_state()
        reached_states.append(state)

        # Check if the game is finished.
        if (board.check_tie() is True):
            q_table.update(reached_states, Outcomes.TIE)
            cont_game = False
        else:
            winner = board.check_win()
            if (winner == Markers.O_MARKER):
                q_table.update(reached_states, Outcomes.O_WIN)
                cont_game = False
            elif (winner == Markers.X_MARKER):
                q_table.update(reached_states, Outcomes.X_WIN)
                cont_game = False

# Save q-table.
file_name = "q_table.csv"
q_table.table.to_csv(file_name)
