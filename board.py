import random
from copy import deepcopy
import sys
import os

class Board:
    def __init__(self, line_count, column_count, bomb_count):
        # TEST INPUT
        if line_count < 4:
            print("ERROR: There are not enough lines!")
            line_count = 4

        if column_count < 4:
            print("ERROR: There are not enough columns!")
            column_count = 4

        if bomb_count >= line_count * column_count or bomb_count < 1:
            print("ERROR: There are too many bombs!")
            bomb_count = 1

        self.line_count = line_count
        self.column_count = column_count
        self.bomb_count = bomb_count
        self.game_state = "new_game"
        self.is_unplayed = True

    def create(self):
        self.game_state = "new_game"
        self.is_unplayed = True

        self.value_matrix = [[0 for j in range(self.column_count)] for i in range(self.line_count)]
        self.state_matrix = [["HIDDEN" for j in range(self.column_count)] for i in range(self.line_count)]

        # ADD BOMBS
        i = 0
        while i < self.bomb_count:
            random_i = random.randint(0, self.line_count - 1)
            random_j = random.randint(0, self.column_count - 1)

            if self.value_matrix[random_i][random_j] != "BOMB":
                self.value_matrix[random_i][random_j] = "BOMB"
                i = i + 1

        self.create_square_numbers()

    def create_square_numbers(self):
        for i in range(len(self.value_matrix)):
            for j in range(len(self.value_matrix[i])):

                sum = 0

                if self.value_matrix[i][j] != "BOMB":

                    for k in range(-1, 2):
                        for l in range(-1, 2):

                            if i + k >= 0 and i + k < len(self.value_matrix):
                                if j + l >= 0 and j + l < len(self.value_matrix[i]):
                                    if (k != 0 or l != 0) and self.value_matrix[i + k][j + l] == "BOMB":
                                        sum = sum + 1

                    self.value_matrix[i][j] = sum

    def print(self):
        print("")
        print("-" * (self.column_count * 2 - 1))

        for i in range(len(self.value_matrix)):
            for j in range(len(self.value_matrix[i])):
                value = self.value_matrix[i][j]
                if isinstance(value, str):
                    value = value[0]
                print(value, end=" ")
            print("")

        return None

    def print_live(self):
        if self.is_unplayed:
            os.system('cls' if os.name == 'nt' else 'clear')

        state_colors = {
            "HIDDEN": "\033[90m",
            "VISIBLE": "\033[97m",
            "FLAG": "\033[93m",
        }
        value_colors = {
            "BOMB": "\033[31m",
            "EXPLODED": "\033[91m",
        }
        reset_color = "\033[0m"
        rows = []

        for i in range(len(self.value_matrix)):
            cells = []
            for j in range(len(self.value_matrix[i])):
                value = self.value_matrix[i][j]
                color = value_colors.get(value, state_colors.get(self.state_matrix[i][j], ""))

                if isinstance(value, str):
                    value = value[0]
                cells.append(f"{color}{value}{reset_color}")
            rows.append(" ".join(cells))

        board_text = "\n".join(rows)
        sys.stdout.write(f"\033[H\033[J{board_text}")
        sys.stdout.flush()

        return None

    def uncover_empty_space(self, line, column, last_cell):
        global value_matrix, state_matrix, matrix_lines, matrix_columns

        if self.state_matrix[line][column] != "HIDDEN" or (self.value_matrix[line][column] != 0 and last_cell != 0):
            return None
        else:
            self.state_matrix[line][column] = "VISIBLE"

        last_cell = self.value_matrix[line][column]

        if column + 1 != self.column_count:
            self.uncover_empty_space(line, column + 1, last_cell)
        if line - 1 != -1:
            self.uncover_empty_space(line - 1, column, last_cell)
        if column - 1 != -1:
            self.uncover_empty_space(line, column - 1, last_cell)
        if line + 1 != self.line_count:
            self.uncover_empty_space(line + 1, column, last_cell)

        if column + 1 != self.column_count and line - 1 != -1:
            self.uncover_empty_space(line - 1, column + 1, last_cell)
        if column - 1 != -1 and line - 1 != -1:
            self.uncover_empty_space(line - 1, column - 1, last_cell)
        if column - 1 != -1 and line + 1 != self.line_count:
            self.uncover_empty_space(line + 1, column - 1, last_cell)
        if column + 1 != self.column_count and line + 1 != self.line_count:
            self.uncover_empty_space(line + 1, column + 1, last_cell)

        return None

    def is_solved(self):
        for i in range(self.line_count):
            for j in range(self.column_count):
                if isinstance(self.value_matrix[i][j], int) and self.state_matrix[i][j] != "VISIBLE":
                    return False
        return True

    # EVENT HANDLERS

    def event_click_face(self, button):
        if(self.game_state == "continue_game"):
            if(button == 1):
                self.game_state = "new_game"
            elif(button == 3):
                self.game_state = "auto_solve"
        elif(self.game_state == "lose"):
            if(button == 1):
                self.game_state = "new_game"
        elif(self.game_state == "win"):
            if(button == 1):
                self.game_state = "new_game"
        elif(self.game_state == "auto_solve"):
            if(button == 1):
                self.game_state = "new_game"
            elif(button == 3):
                self.game_state = "continue_game"

    def event_click_square(self, button, line, column):
        if(self.game_state == "continue_game" or self.game_state == "auto_solve"):
            if(button == 1):
                if self.state_matrix[line][column] == "HIDDEN":
                    if self.value_matrix[line][column] == 0:
                        self.uncover_empty_space(line, column, 0)

                    elif self.value_matrix[line][column] == "BOMB":
                        if self.is_unplayed:
                            self.state_matrix[line][column] = "VISIBLE"
                            self.value_matrix[line][column] = 0
                            self.create_square_numbers()
                        else:
                            self.value_matrix[line][column] = "EXPLODED"
                            self.game_state = "lose"

                    else:
                        self.state_matrix[line][column] = "VISIBLE"

                    self.is_unplayed = False
                    if self.is_solved():
                        self.game_state = "win"

            elif(button == 3):
                if self.state_matrix[line][column] == "HIDDEN":
                    self.state_matrix[line][column] = "FLAG"

                elif self.state_matrix[line][column] == "FLAG":
                    self.state_matrix[line][column] = "HIDDEN"
        self.print_live()

    # AUTO SOLVER

    def auto_solver_case_1(self):
        # If a tile has the same amount of hidden squares around it as unflagged bombs remaining around it then all the hidden tiles are bombs

        has_done_action = False

        for i in range(self.line_count):
            for j in range(self.column_count):

                flags = 0
                hidden = 0

                if isinstance(self.value_matrix[i][j], int) and self.state_matrix[i][j] == "VISIBLE":
                    if self.value_matrix[i][j] > 0:
                        for k in range(-1, 2):
                            for l in range(-1, 2):

                                if i + k >= 0 and i + k < self.line_count:
                                    if j + l >= 0 and j + l < self.column_count:
                                        if k != 0 or l != 0:
                                            if self.state_matrix[i + k][j + l] == "HIDDEN":
                                                hidden = hidden + 1
                                            if self.state_matrix[i + k][j + l] == "FLAG":
                                                flags = flags + 1

                        if self.value_matrix[i][j] == hidden + flags:
                            for k in range(-1, 2):
                                for l in range(-1, 2):

                                    if i + k >= 0 and i + k < self.line_count:
                                        if j + l >= 0 and j + l < self.column_count:
                                            if k != 0 or l != 0:
                                                if self.state_matrix[i + k][j + l] == "HIDDEN":
                                                    self.event_click_square(3, i + k, j + l)
                                                    has_done_action = True

        return has_done_action

    def auto_solver_case_2(self):
        # If a tile has the same amount of flags around it as the number on the square then all remaining hidden tiles around it are not bombs

        has_done_action = False

        for i in range(self.line_count):
            for j in range(self.column_count):

                flags = 0

                if isinstance(self.value_matrix[i][j], int) and self.state_matrix[i][j] == "VISIBLE":
                    if self.value_matrix[i][j] >= 0:
                        for k in range(-1, 2):
                            for l in range(-1, 2):

                                if i + k >= 0 and i + k < self.line_count:
                                    if j + l >= 0 and j + l < self.column_count:
                                        if k != 0 or l != 0:
                                            if self.state_matrix[i + k][j + l] == "FLAG":
                                                flags = flags + 1

                        if self.value_matrix[i][j] == flags:
                            for k in range(-1, 2):
                                for l in range(-1, 2):

                                    if i + k >= 0 and i + k < self.line_count:
                                        if j + l >= 0 and j + l < self.column_count:
                                            if k != 0 or l != 0:
                                                if self.state_matrix[i + k][j + l] == "HIDDEN":
                                                    self.event_click_square(1, i + k, j + l)
                                                    has_done_action = True

        return has_done_action

    def auto_solver_case_3(self):
        # In case of uncertainty, we calculate probabilities to pick the most likely safe square

        value_matrix_copy = deepcopy(self.value_matrix)
        hidden_matrix = [[0 for j in range(self.column_count)] for i in range(self.line_count)]
        probability_matrix = [[0 for j in range(self.column_count)] for i in range(self.line_count)]
        divide_for_average_matrix = [[0 for j in range(self.column_count)] for i in range(self.line_count)]

        # SCAD FLAGS SI NUMAR HIDDEN

        for i in range(self.line_count):
            for j in range(self.column_count):
                if isinstance(value_matrix_copy[i][j], int) and self.state_matrix[i][j] == "VISIBLE":
                    if value_matrix_copy[i][j] > 0:

                        for k in range(-1, 2):
                            for l in range(-1, 2):
                                if i + k >= 0 and i + k < self.line_count:
                                    if j + l >= 0 and j + l < self.column_count:
                                        if k != 0 or l != 0:
                                            if self.state_matrix[i + k][j + l] == "FLAG":
                                                value_matrix_copy[i][j] -= 1
                                            if self.state_matrix[i + k][j + l] == "HIDDEN":
                                                hidden_matrix[i][j] += 1

        # ADAUG PROBABILITATILE INTR-O MATRICE

        for i in range(self.line_count):
            for j in range(self.column_count):
                if isinstance(value_matrix_copy[i][j], int) and self.state_matrix[i][j] == "VISIBLE":
                    if value_matrix_copy[i][j] > 0:

                        for k in range(-1, 2):
                            for l in range(-1, 2):
                                if i + k >= 0 and i + k < self.line_count:
                                    if j + l >= 0 and j + l < self.column_count:
                                        if k != 0 or l != 0:
                                            if self.state_matrix[i + k][j + l] == "HIDDEN":
                                                probability_matrix[i + k][j + l] = probability_matrix[i + k][j + l] + \
                                                                                value_matrix_copy[i][j] / \
                                                                                hidden_matrix[i][j]
                                                divide_for_average_matrix[i + k][j + l] += 1

        # CALCULEZ PROBABILITATEA FINALA

        for i in range(self.line_count):
            for j in range(self.column_count):
                if divide_for_average_matrix[i][j] != 0:
                    probability_matrix[i][j] = probability_matrix[i][j] / divide_for_average_matrix[i][j]

        # PROBABILITATE MINIMA
        minimum_value = 2
        choice_column = -1
        choice_line = -1

        for i in range(self.line_count):
            for j in range(self.column_count):
                if probability_matrix[i][j] < minimum_value and probability_matrix[i][j] != 0:
                    minimum_value = probability_matrix[i][j]
                    choice_line = i
                    choice_column = j

        if choice_column == -1:
            return None

        return choice_line, choice_column

    def auto_solver(self):
        if self.is_unplayed:
            choice_line = random.randint(1, self.line_count - 2)
            choice_column = random.randint(1, self.column_count - 2)
            self.event_click_square(1, choice_line, choice_column)
            return

        did_case_1_act = self.auto_solver_case_1()
        did_case_2_act = self.auto_solver_case_2()

        if not did_case_1_act and not did_case_2_act:
            case_3_result = self.auto_solver_case_3()
            if case_3_result[0] is not None and case_3_result[1] is not None:
                self.event_click_square(1, case_3_result[0], case_3_result[1])
