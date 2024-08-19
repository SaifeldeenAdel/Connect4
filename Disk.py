import pygame
from constants import CELL_SIZE, HUMAN, AI


class Disk:
    def __init__(self, row: int, col: int, player: list = [HUMAN, AI]):
        self.row = row
        self.col = col
        self.color = (255, 0, 0) if player == HUMAN else (255, 255, 0)
        self.radius = CELL_SIZE // 2 - 5  # Adjusted to fit within a cell

    def draw(self, surface):
        center_x = self.col * CELL_SIZE + CELL_SIZE // 2
        center_y = self.row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(surface, self.color, (center_x, center_y), self.radius)

    def set_pos(self, row, col):
        self.row = row
        self.col = col

    def set_color(self, player):
        self.color = (255, 0, 0) if player == HUMAN else (255, 255, 0)

    def __repr__(self) -> str:
        return f"{'RED' if self.color == (255, 0, 0) else 'YELLOW'}:({self.row}, {self.col})"
