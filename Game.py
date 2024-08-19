import pygame
import numpy as np
import random
from treelib import Tree
from BoardState import BoardState
from InternalState import InternalState
from Disk import Disk
from Minimax import Minimax

from constants import EMPTY, HUMAN, AI
from constants import WIDTH, HEIGHT, COLUMNS, ROWS, CELL_SIZE, INITIAL_STATE
from constants import MINIMAX, MINIMAX_PRUNE, EXPECTI


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.playing = False
        self.player = HUMAN  # if random.random() >= 0.5 else AI

        self.human = 1 if self.player == HUMAN else 2
        self.ai = 1 if self.player == AI else 2

        self.mode = None
        self.tree = Tree()

        self.disks = [0 for _ in range(42)]  # Pool of disks to use

        self.current_state = BoardState(InternalState(INITIAL_STATE))

        # self.current_state = self.current_state.insert(1, self.human)
        # self.current_state = self.current_state.insert(1, self.human)
        # self.current_state = self.current_state.insert(1, self.human)
        # self.current_state = self.current_state.insert(1, self.human)
        # self.current_state = self.current_state.insert(1, self.human)
        # self.current_state = self.current_state.insert(1, self.human)
        # self.current_state = self.current_state.insert(1, self.human)
        print(self.current_state.state.get_numpy_format())

        # self.K = input("Enter K (max depth of tree): ")

        self.initialiseBoard()

    def initialiseBoard(self):
        self.surface = pygame.display.set_mode((WIDTH + 200, HEIGHT))
        self.surface.fill((202, 228, 241))

    def new_game(self):
        self.playing = True

    def play(self):
        while self.playing:
            self.check_events()
            self.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.minimax_btn.collidepoint(event.pos):
                    self.mode = MINIMAX
                    # self.player = HUMAN if self.player == AI else AI

                elif self.pruning_btn.collidepoint(event.pos):
                    self.mode = MINIMAX_PRUNE

                elif self.expecti_btn.collidepoint(event.pos):
                    self.mode = EXPECTI
                else:
                    # Handle human move
                    if self.player == HUMAN:
                        col = event.pos[0] // CELL_SIZE  # Determine the clicked column
                        self.handle_human_move(col)

    def update(self):
        self.surface.fill((202, 228, 241))
        self.make_grid_and_buttons()
        self.update_text()

        # Update pool of disks based on state and draw them
        self.set_disks()
        for disk in self.disks:
            if disk:
                disk.draw(self.surface)

        if self.player == AI and self.mode:
            Minimax.get_instance().run(self.K)
            print("Running algo")

        pygame.display.update()

    # Creates new disk objects if need or updates existing objects
    def set_disks(self):
        for i, row in enumerate(self.current_state.state.get_numpy_format()):
            for j, player in enumerate(row):
                if player:
                    index = i * COLUMNS + j
                    if not self.disks[index]:
                        self.disks[index] = Disk(i, j, player)
                    else:
                        self.disks[index].set_pos(i, j)
                        self.disks[index].set_color(player)

    def make_grid_and_buttons(self):
        for i in range(ROWS + 1):
            pygame.draw.line(self.surface, (0, 0, 0), (0, (i) * CELL_SIZE),
                             (WIDTH, (i) * CELL_SIZE), 2)
        for i in range(COLUMNS + 1):
            pygame.draw.line(self.surface, (0, 0, 0), (i * CELL_SIZE, 0),
                             (i * CELL_SIZE, HEIGHT), 2)

        self.minimax_btn = self.make_button("Minimax", WIDTH + 40, 200, 120, 40)
        self.pruning_btn = self.make_button("Minimax a-B", WIDTH + 20, 260, 160, 40)
        self.expecti_btn = self.make_button("Expecti", WIDTH + 40, 320, 120, 40)

    def update_text(self):
        self.font = pygame.font.Font(None, 33)
        color = (255, 0, 0) if self.player == HUMAN else (180, 140, 0)
        player_text = self.font.render(f"Player: {'HUMAN' if self.player is HUMAN else 'AI'}", True, color)
        mode = self.font.render(f"Mode: {self.mode}", True, (0, 0, 0))
        self.surface.blit(player_text, (WIDTH + 20, 100))
        self.surface.blit(mode, (WIDTH + 20, 600))

    def make_button(self, text, x, y, width, height):
        rect = pygame.Rect(x, y, width, height)
        font = pygame.font.Font(None, 33)
        text = font.render(text, True, (0, 0, 0))

        pygame.draw.rect(self.surface, (255, 255, 255), rect)
        self.surface.blit(text, text.get_rect(center=rect.center))
        return rect

    def handle_human_move(self, col):
        print(f"col: {col} || human: {self.human}")
        self.current_state = self.current_state.insert(col, self.human)
        print(self.current_state.state.get_numpy_format())
        print(self.current_state.state.get_binary_state())
        # self.player = AI  # Switch to AI after the human move

    def game_end(self):
        return not np.any(self.current_state == 0)
