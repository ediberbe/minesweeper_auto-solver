import pygame
import time
from board import Board
from renderer import Renderer

def handle_events(board, renderer, allow_square_clicks=False):
    for event in pygame.event.get():
        clicked_object = renderer.detect_clicked_object(event, board)
        if not clicked_object:
            continue

        object_type = clicked_object[0]
        if object_type == "quit":
            board.game_state = "quit"
        elif object_type == "face":
            board.event_click_face(event.button)
        elif allow_square_clicks and object_type == "square":
            board.event_click_square(event.button, clicked_object[1], clicked_object[2])


def run_game(board, renderer):
    while board.game_state == "continue_game":
        renderer.draw_board(board, board.game_state)
        handle_events(board, renderer, allow_square_clicks=True)


def run_finished_game(board, renderer):
    while board.game_state in ("lose", "win"):
        renderer.draw_board(board, board.game_state)
        handle_events(board, renderer)


def run_auto_solver(board, renderer):
    for row in range(board.line_count):
        for column in range(board.column_count):
            if board.state_matrix[row][column] == "FLAG":
                board.state_matrix[row][column] = "HIDDEN"

    while board.game_state == "auto_solve":
        renderer.draw_board(board, board.game_state)
        handle_events(board, renderer)
        board.auto_solver()
        time.sleep(0.1)


def main():
    board = Board(16, 16, 40)
    renderer = Renderer((board.column_count * 32, board.line_count * 32))

    while board.game_state != "quit":
        if board.game_state == "new_game":
            board.create()
            board.print_live()
            board.game_state = "continue_game"
        elif board.game_state == "continue_game":
            run_game(board, renderer)
        elif board.game_state in ("lose", "win"):
            run_finished_game(board, renderer)
        elif board.game_state == "auto_solve":
            run_auto_solver(board, renderer)


if __name__ == "__main__":
    main()