import pygame

class Renderer:
    def __init__(self, size):
        pygame.init()
        pygame.display.set_caption("Minesweeper")
        icon = pygame.image.load("assets/tile_bomb.png")
        pygame.display.set_icon(icon)

        self.screen = None
        self.header = 64

        self.screen = pygame.display.set_mode((size[0], size[1] + self.header))

    def draw_board(self, board, game_state):
        self.screen.fill((192, 192, 192))
        self.draw_board_face(board, game_state)
        self.draw_board_squares(board, game_state)
        pygame.display.update()

    def draw_board_face(self, board, game_state):
        if(game_state == "continue_game"):
            face_image = pygame.image.load("assets/face_smile.png")
        elif(game_state == "lose"):
            face_image = pygame.image.load("assets/face_lose.png")
        elif(game_state == "win"):
            face_image = pygame.image.load("assets/face_win.png")
        elif(game_state == "auto_solve"):
            face_image = pygame.image.load("assets/face_smile.png")
        self.screen.blit(face_image, (board.column_count * 32 // 2 - 26, self.header - 58))

    def draw_board_squares(self, board, game_state):

        if(game_state == "continue_game"):
            for i in range(board.line_count):
                for j in range(board.column_count):

                    if board.state_matrix[i][j] == "HIDDEN":
                        tile_image = pygame.image.load("assets/tile_hidden.png")

                    elif board.state_matrix[i][j] == "VISIBLE":
                        if isinstance(board.value_matrix[i][j], int):
                            tile_image = pygame.image.load("assets/tile_" + str(board.value_matrix[i][j]) + ".png")

                    elif board.state_matrix[i][j] == "EXPLODED":
                        tile_image = pygame.image.load("assets/tile_bomb_red.png")

                    elif board.state_matrix[i][j] == "FLAG":
                        tile_image = pygame.image.load("assets/tile_flag.png")

                    self.screen.blit(tile_image, (j * 32, self.header + i * 32))

        elif(game_state == "lose"):
            for i in range(board.line_count):
                for j in range(board.column_count):

                    if isinstance(board.value_matrix[i][j], int):
                        tile_image = pygame.image.load("assets/tile_" + str(board.value_matrix[i][j]) + ".png")

                    elif board.state_matrix[i][j] == "FLAG":
                        tile_image = pygame.image.load("assets/tile_flag.png")

                    elif board.value_matrix[i][j] == "EXPLODED":
                        tile_image = pygame.image.load("assets/tile_bomb_red.png")

                    elif board.value_matrix[i][j] == "BOMB":
                        tile_image = pygame.image.load("assets/tile_bomb.png")

                    self.screen.blit(tile_image, (j * 32, self.header + i * 32))

        elif(game_state == "win"):
            for i in range(board.line_count):
                for j in range(board.column_count):

                    if isinstance(board.value_matrix[i][j], int):
                        tile_image = pygame.image.load("assets/tile_" + str(board.value_matrix[i][j]) + ".png")

                    elif board.state_matrix[i][j] == "FLAG":
                        tile_image = pygame.image.load("assets/tile_flag.png")

                    elif board.value_matrix[i][j] == "EXPLODED":
                        tile_image = pygame.image.load("assets/tile_bomb_red.png")

                    elif board.value_matrix[i][j] == "BOMB":
                        tile_image = pygame.image.load("assets/tile_hidden.png")

                    self.screen.blit(tile_image, (j * 32, self.header + i * 32))

        elif(game_state == "auto_solve"):
            for i in range(board.line_count):
                for j in range(board.column_count):

                    if board.state_matrix[i][j] == "HIDDEN":
                        tile_image = pygame.image.load("assets/tile_hidden.png")

                    elif board.state_matrix[i][j] == "VISIBLE":
                        if isinstance(board.value_matrix[i][j], int):
                            tile_image = pygame.image.load("assets/tile_" + str(board.value_matrix[i][j]) + ".png")
                        elif board.value_matrix[i][j] == "BOMB":
                            tile_image = pygame.image.load("assets/tile_bomb.png")

                    elif board.state_matrix[i][j] == "EXPLODED":
                        tile_image = pygame.image.load("assets/tile_bomb_red.png")

                    elif board.state_matrix[i][j] == "FLAG":
                        tile_image = pygame.image.load("assets/tile_flag.png")

                    self.screen.blit(tile_image, (j * 32, self.header + i * 32))

    def detect_clicked_object(self, event, board):
        if event.type == pygame.QUIT:
            return ("quit",)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            mouse_position_x = mouse_position[0]
            mouse_position_y = mouse_position[1]

            if mouse_position_x > board.column_count * 16 - 26 and mouse_position_x < board.column_count * 16 + 26 and mouse_position_y > 6 and mouse_position_y < 58:
                return("face",)

            if mouse_position_y >= self.header:
                column = int((mouse_position_x - mouse_position_x % 32) / 32)
                mouse_position_y = mouse_position_y - self.header
                line = int((mouse_position_y - mouse_position_y % 32) / 32)
                return ("square", line, column)