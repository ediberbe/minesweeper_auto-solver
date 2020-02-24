import pygame
import random
import time
from copy import deepcopy


# FUNCTIONS

def create_matrix(lines, columns, bombs):
    # TEST INPUT
    if lines < 4:
        print("ERROR: There are not enough lines!")
        lines = 4

    if columns < 4:
        print("ERROR: There are not enough columns!")
        columns = 4

    if bombs >= lines * columns or bombs < 1:
        print("ERROR: There are too many bombs!")
        bombs = 1

    matrix = [[0 for j in range(columns)] for i in range(lines)]

    # INSERT BOMBS
    i = 0
    while i < bombs:
        random_i = random.randint(0, lines - 1)
        random_j = random.randint(0, columns - 1)

        if matrix[random_i][random_j] != "B":
            matrix[random_i][random_j] = "B"
            i = i + 1

    matrix = count_neighbours(matrix)

    return matrix


def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], sep="", end=" ")
        print("")


def count_neighbours(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):

            sum = 0

            if matrix[i][j] != "B":

                for k in range(-1, 2):
                    for l in range(-1, 2):

                        if i + k >= 0 and i + k < len(matrix):
                            if j + l >= 0 and j + l < len(matrix[i]):
                                if (k != 0 or l != 0) and matrix[i + k][j + l] == "B":
                                    sum = sum + 1

                matrix[i][j] = sum

    return matrix


def flood_fill(pos_x, pos_y, last_cell):
    global value_matrix, state_matrix, matrix_lines, matrix_columns

    if state_matrix[pos_y][pos_x] != "H" or (value_matrix[pos_y][pos_x] != 0 and last_cell != 0):
        return None
    else:
        state_matrix[pos_y][pos_x] = "S"

    last_cell = value_matrix[pos_y][pos_x]

    if pos_x + 1 != matrix_columns:
        flood_fill(pos_x + 1, pos_y, last_cell)
    if pos_y - 1 != -1:
        flood_fill(pos_x, pos_y - 1, last_cell)
    if pos_x - 1 != -1:
        flood_fill(pos_x - 1, pos_y, last_cell)
    if pos_y + 1 != matrix_lines:
        flood_fill(pos_x, pos_y + 1, last_cell)

    if pos_x + 1 != matrix_columns and pos_y - 1 != -1:
        flood_fill(pos_x + 1, pos_y - 1, last_cell)
    if pos_x - 1 != -1 and pos_y - 1 != -1:
        flood_fill(pos_x - 1, pos_y - 1, last_cell)
    if pos_x - 1 != -1 and pos_y + 1 != matrix_lines:
        flood_fill(pos_x - 1, pos_y + 1, last_cell)
    if pos_x + 1 != matrix_columns and pos_y + 1 != matrix_lines:
        flood_fill(pos_x + 1, pos_y + 1, last_cell)

    return None


def win_check():
    global value_matrix, state_matrix, matrix_lines, matrix_columns
    for i in range(matrix_lines):
        for j in range(matrix_columns):
            if isinstance(value_matrix[i][j], int) and state_matrix[i][j] != "S":
                return False
    return True


# TODO SOLVE CASES

def solve_case_1():
    global value_matrix, state_matrix, matrix_lines, matrix_columns

    ok = False

    for i in range(matrix_lines):
        for j in range(matrix_columns):

            flags = 0
            hidden = 0

            if isinstance(value_matrix[i][j], int) and state_matrix[i][j] == "S":
                if value_matrix[i][j] > 0:
                    for k in range(-1, 2):
                        for l in range(-1, 2):

                            if i + k >= 0 and i + k < matrix_lines:
                                if j + l >= 0 and j + l < matrix_columns:
                                    if k != 0 or l != 0:
                                        if state_matrix[i + k][j + l] == "H":
                                            hidden = hidden + 1
                                        if state_matrix[i + k][j + l] == "F":
                                            flags = flags + 1

                    if value_matrix[i][j] == hidden + flags:
                        for k in range(-1, 2):
                            for l in range(-1, 2):

                                if i + k >= 0 and i + k < matrix_lines:
                                    if j + l >= 0 and j + l < matrix_columns:
                                        if k != 0 or l != 0:
                                            if state_matrix[i + k][j + l] == "H":
                                                state_matrix[i + k][j + l] = "F"
                                                ok = True

    return ok


def solve_case_2():
    global value_matrix, state_matrix, matrix_lines, matrix_columns

    ok = False

    for i in range(matrix_lines):
        for j in range(matrix_columns):

            flags = 0

            if isinstance(value_matrix[i][j], int) and state_matrix[i][j] == "S":
                if value_matrix[i][j] >= 0:
                    for k in range(-1, 2):
                        for l in range(-1, 2):

                            if i + k >= 0 and i + k < matrix_lines:
                                if j + l >= 0 and j + l < matrix_columns:
                                    if k != 0 or l != 0:
                                        if state_matrix[i + k][j + l] == "F":
                                            flags = flags + 1

                    if value_matrix[i][j] == flags:
                        for k in range(-1, 2):
                            for l in range(-1, 2):

                                if i + k >= 0 and i + k < matrix_lines:
                                    if j + l >= 0 and j + l < matrix_columns:
                                        if k != 0 or l != 0:
                                            if state_matrix[i + k][j + l] == "H" and value_matrix[i + k][j + l] == 0:
                                                flood_fill(j + l, i + k, 0)
                                                ok = True
                                            elif state_matrix[i + k][j + l] == "H":
                                                state_matrix[i + k][j + l] = "S"
                                                ok = True

    return ok


def solve_case_3():
    global value_matrix, state_matrix, matrix_lines, matrix_columns, choice_x, choice_y

    value_matrix_copy = deepcopy(value_matrix)
    hidden_matrix = [[0 for j in range(matrix_columns)] for i in range(matrix_lines)]
    probability_matrix = [[0 for j in range(matrix_columns)] for i in range(matrix_lines)]
    divide_for_average_matrix = [[0 for j in range(matrix_columns)] for i in range(matrix_lines)]

    # SCAD FLAGS SI NUMAR HIDDEN

    for i in range(matrix_lines):
        for j in range(matrix_columns):
            if isinstance(value_matrix_copy[i][j], int) and state_matrix[i][j] == "S":
                if value_matrix_copy[i][j] > 0:

                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            if i + k >= 0 and i + k < matrix_lines:
                                if j + l >= 0 and j + l < matrix_columns:
                                    if k != 0 or l != 0:
                                        if state_matrix[i + k][j + l] == "F":
                                            value_matrix_copy[i][j] -= 1
                                        if state_matrix[i + k][j + l] == "H":
                                            hidden_matrix[i][j] += 1

    # ADAUG PROBABILITATILE INTR-O MATRICE

    for i in range(matrix_lines):
        for j in range(matrix_columns):
            if isinstance(value_matrix_copy[i][j], int) and state_matrix[i][j] == "S":
                if value_matrix_copy[i][j] > 0:

                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            if i + k >= 0 and i + k < matrix_lines:
                                if j + l >= 0 and j + l < matrix_columns:
                                    if k != 0 or l != 0:
                                        if state_matrix[i + k][j + l] == "H":
                                            probability_matrix[i + k][j + l] = probability_matrix[i + k][j + l] + \
                                                                               value_matrix_copy[i][j] / \
                                                                               hidden_matrix[i][j]
                                            divide_for_average_matrix[i + k][j + l] += 1

    # CALCULEZ PROBABILITATEA FINALA

    for i in range(matrix_lines):
        for j in range(matrix_columns):
            if divide_for_average_matrix[i][j] != 0:
                probability_matrix[i][j] = probability_matrix[i][j] / divide_for_average_matrix[i][j]

    # PROBABILITATE MINIMA
    minimum_value = 2
    choice_x = -1
    choice_y = -1

    for i in range(matrix_lines):
        for j in range(matrix_columns):
            if probability_matrix[i][j] < minimum_value and probability_matrix[i][j] != 0:
                minimum_value = probability_matrix[i][j]
                choice_y = i
                choice_x = j

    return True


# WINDOW

pygame.init()
pygame.display.set_caption("Minesweeper")
icon = pygame.image.load("tile_bomb.png")
pygame.display.set_icon(icon)

# MAIN GAME LOOP

solve_count = 0
solve_win_count = 0

begginer_difficulty = [8 ,8 ,10]
intermediate_difficulty = [16, 16, 40]
expert_difficulty = [16, 30, 99]

game_state = "new_game"
while game_state != "quit":

    if game_state == "new_game":
        value_matrix = create_matrix(expert_difficulty[0], expert_difficulty[1], expert_difficulty[2])
        state_matrix = [["H" for j in range(len(value_matrix[i]))] for i in range(len(value_matrix))]

        matrix_lines = len(value_matrix)
        matrix_columns = len(value_matrix[0])

        print("")
        print("-" * (matrix_columns * 2 - 1))
        print_matrix(value_matrix)

        header = 64
        first_click = True
        screen = pygame.display.set_mode((matrix_columns * 32, matrix_lines * 32 + header))

        game_state = "continue_game"

    while game_state == "continue_game":

        screen.fill((192, 192, 192))
        face_image = pygame.image.load("face_smile.png")
        screen.blit(face_image, (matrix_columns * 32 // 2 - 26, header - 58))

        # EVENT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                mouse_position_x = mouse_position[0]
                mouse_position_y = mouse_position[1]

                if event.button == 1:

                    if mouse_position_x > matrix_columns * 16 - 26 and mouse_position_x < matrix_columns * 16 + 26 and mouse_position_y > 6 and mouse_position_y < 58:
                        game_state = "new_game"

                    if mouse_position_y >= header:
                        column = int((mouse_position_x - mouse_position_x % 32) / 32)
                        mouse_position_y = mouse_position_y - header
                        line = int((mouse_position_y - mouse_position_y % 32) / 32)

                        if state_matrix[line][column] == "H":
                            if value_matrix[line][column] == 0:
                                flood_fill(column, line, 0)

                            if value_matrix[line][column] == "B":
                                value_matrix[line][column] = "X"
                                game_state = "lose"

                        if state_matrix[line][column] != "F":
                            state_matrix[line][column] = "S"
                        first_click = False

                elif event.button == 3:
                    if mouse_position_x > matrix_columns * 16 - 26 and mouse_position_x < matrix_columns * 16 + 26 and mouse_position_y > 6 and mouse_position_y < 58:
                        game_state = "solve"

                    if mouse_position_y >= header:
                        column = int((mouse_position_x - mouse_position_x % 32) / 32)
                        mouse_position_y = mouse_position_y - header
                        line = int((mouse_position_y - mouse_position_y % 32) / 32)

                        if state_matrix[line][column] == "H":
                            state_matrix[line][column] = "F"

                        elif state_matrix[line][column] == "F":
                            state_matrix[line][column] = "H"

                if win_check():
                    game_state = "win"

        # DRAW BOARD

        for i in range(matrix_lines):
            for j in range(matrix_columns):

                if state_matrix[i][j] == "H":
                    tile_image = pygame.image.load("tile_hidden.png")

                elif state_matrix[i][j] == "S":
                    if isinstance(value_matrix[i][j], int):
                        tile_image = pygame.image.load("tile_" + str(value_matrix[i][j]) + ".png")

                elif state_matrix[i][j] == "X":
                    tile_image = pygame.image.load("tile_bomb_red.png")

                elif state_matrix[i][j] == "F":
                    tile_image = pygame.image.load("tile_flag.png")

                screen.blit(tile_image, (j * 32, header + i * 32))

        pygame.display.update()

    while game_state == "lose":

        screen.fill((192, 192, 192))
        face_image = pygame.image.load("face_lose.png")
        screen.blit(face_image, (matrix_columns * 32 // 2 - 26, header - 58))

        # EVENT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                mouse_position_x = mouse_position[0]
                mouse_position_y = mouse_position[1]

                if event.button == 1:
                    if mouse_position_x > matrix_columns * 16 - 26 and mouse_position_x < matrix_columns * 16 + 26 and mouse_position_y > 6 and mouse_position_y < 58:
                        game_state = "new_game"

        # DRAW BOARD

        for i in range(matrix_lines):
            for j in range(matrix_columns):

                if isinstance(value_matrix[i][j], int):
                    tile_image = pygame.image.load("tile_" + str(value_matrix[i][j]) + ".png")

                elif state_matrix[i][j] == "F":
                    tile_image = pygame.image.load("tile_flag.png")

                elif value_matrix[i][j] == "X":
                    tile_image = pygame.image.load("tile_bomb_red.png")

                elif value_matrix[i][j] == "B":
                    tile_image = pygame.image.load("tile_bomb.png")

                screen.blit(tile_image, (j * 32, header + i * 32))

        pygame.display.update()

    while game_state == "win":

        screen.fill((192, 192, 192))
        face_image = pygame.image.load("face_win.png")
        screen.blit(face_image, (matrix_columns * 32 // 2 - 26, header - 58))

        # EVENT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                mouse_position_x = mouse_position[0]
                mouse_position_y = mouse_position[1]

                if event.button == 1:
                    if mouse_position_x > matrix_columns * 16 - 26 and mouse_position_x < matrix_columns * 16 + 26 and mouse_position_y > 6 and mouse_position_y < 58:
                        game_state = "new_game"

        # DRAW BOARD

        for i in range(matrix_lines):
            for j in range(matrix_columns):

                if isinstance(value_matrix[i][j], int):
                    tile_image = pygame.image.load("tile_" + str(value_matrix[i][j]) + ".png")

                elif state_matrix[i][j] == "F":
                    tile_image = pygame.image.load("tile_flag.png")

                elif value_matrix[i][j] == "X":
                    tile_image = pygame.image.load("tile_bomb_red.png")

                elif value_matrix[i][j] == "B":
                    tile_image = pygame.image.load("tile_hidden.png")

                screen.blit(tile_image, (j * 32, header + i * 32))

        pygame.display.update()

    if game_state == "solve":

        solve_count += 1
        print("Solve steps: ", end="")

        for i in range(matrix_lines):
            for j in range(matrix_columns):
                if state_matrix[i][j] == "F":
                    state_matrix[i][j] = "H"

        while game_state == "solve":

            screen.fill((192, 192, 192))
            face_image = pygame.image.load("face_solve.png")
            screen.blit(face_image, (matrix_columns * 32 // 2 - 26, header - 58))

            # EVENT

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = "quit"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    mouse_position_x = mouse_position[0]
                    mouse_position_y = mouse_position[1]

                    if event.button == 1:
                        if mouse_position_x > matrix_columns * 16 - 26 and mouse_position_x < matrix_columns * 16 + 26 and mouse_position_y > 6 and mouse_position_y < 58:
                            game_state = "new_game"

                    if event.button == 3:
                        if mouse_position_x > matrix_columns * 16 - 26 and mouse_position_x < matrix_columns * 16 + 26 and mouse_position_y > 6 and mouse_position_y < 58:
                            running = True
                            while running:

                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        game_state = "quit"
                                        running = False

                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                        mouse_position = pygame.mouse.get_pos()
                                        mouse_position_x = mouse_position[0]
                                        mouse_position_y = mouse_position[1]

                                        if event.button == 1:
                                            if mouse_position_x > matrix_columns * 16 - 26 and mouse_position_x < matrix_columns * 16 + 26 and mouse_position_y > 6 and mouse_position_y < 58:
                                                game_state = "new_game"
                                                running = False

                                        if event.button == 3:
                                            if mouse_position_x > matrix_columns * 16 - 26 and mouse_position_x < matrix_columns * 16 + 26 and mouse_position_y > 6 and mouse_position_y < 58:
                                                running = False

            # TODO ALGORITHM
            # CHOICE

            if first_click:
                print("F", end=" ")
                choice_x = random.randint(1, matrix_columns - 2)
                choice_y = random.randint(1, matrix_lines - 2)

            result_1 = solve_case_1()
            result_2 = solve_case_2()

            if result_1:
                print("1", end=" ")
            if result_2:
                print("2", end=" ")

            result_3 = False
            if result_1 == False and result_2 == False and first_click == False:
                print("3", end=" ")
                result_3 = solve_case_3()

            # REPERCURSION

            if first_click or result_3:
                if state_matrix[choice_y][choice_x] == "H":
                    if value_matrix[choice_y][choice_x] == 0:
                        flood_fill(choice_x, choice_y, 0)
                    elif isinstance(value_matrix[choice_y][choice_x], int):
                        state_matrix[choice_y][choice_x] = "S"
                    elif value_matrix[choice_y][choice_x] == "B":
                        value_matrix[choice_y][choice_x] = "X"
                        game_state = "lose"

            first_click = False
            if win_check():
                game_state = "win"

            # DRAW BOARD

            for i in range(matrix_lines):
                for j in range(matrix_columns):

                    if state_matrix[i][j] == "H":
                        tile_image = pygame.image.load("tile_hidden.png")

                    elif state_matrix[i][j] == "S":
                        if isinstance(value_matrix[i][j], int):
                            tile_image = pygame.image.load("tile_" + str(value_matrix[i][j]) + ".png")
                        elif value_matrix[i][j] == "B":
                            tile_image = pygame.image.load("tile_bomb.png")

                    elif state_matrix[i][j] == "X":
                        tile_image = pygame.image.load("tile_bomb_red.png")

                    elif state_matrix[i][j] == "F":
                        tile_image = pygame.image.load("tile_flag.png")

                    screen.blit(tile_image, (j * 32, header + i * 32))

            # AFISARE STATISTICA
            if game_state == "win":
                solve_win_count += 1
                print("\nAlgoritmul a castigat! Rata de succes este ", solve_win_count, " din ", solve_count, ".",sep="")

            elif game_state == "lose":
                print("\nAlgoritmul a pierdut! Rata de succes este ", solve_win_count, " din ", solve_count, ".",sep="")

            time.sleep(0.2)
            pygame.display.update()
