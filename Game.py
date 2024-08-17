import pygame
import numpy as np
from StateHelper import StateHelper

from constants import EMPTY, RED, YELLOW
from constants import WIDTH, HEIGHT, COLUMNS, ROWS, CELL_SIZE
from constants import MINIMAX, MINIMAX_PRUNE, EXPECTI

class Game:
  def __init__(self) -> None:
    pygame.init()
    self.playing = False
    self.player = RED
    self.mode = None
    self.current_state = np.zeros((8,8), dtype=np.int8)
    self.current_state = StateHelper.insert(self.current_state,7,1)
    self.current_state = StateHelper.insert(self.current_state,2,1)
    self.current_state = StateHelper.insert(self.current_state,7,1)
    self.current_state = StateHelper.insert(self.current_state,7,1)

    print(self.current_state)
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
            self.player = YELLOW

        if self.pruning_btn.collidepoint(event.pos):
            self.mode = MINIMAX_PRUNE

        if self.expecti_btn.collidepoint(event.pos):
            self.mode = EXPECTI


  def update(self):
    self.surface.fill((202, 228, 241))
    self.make_grid_and_buttons()
    self.update_text()
    
    pygame.display.update()

    
  def make_grid_and_buttons(self):
    for i in range(ROWS+1):
        pygame.draw.line(self.surface, (0, 0, 0), (0, (i) * CELL_SIZE),
                          (WIDTH, (i) * CELL_SIZE), 2)
    for i in range(COLUMNS+1):
        pygame.draw.line(self.surface, (0, 0, 0), (i * CELL_SIZE, 0),
                          (i * CELL_SIZE, HEIGHT), 2)
    
    self.minimax_btn = self.make_button("Minimax", WIDTH+40, 200, 120, 40 )
    self.pruning_btn = self.make_button("Minimax a-B", WIDTH+20, 260, 160, 40 )
    self.expecti_btn = self.make_button("Expecti", WIDTH+40, 320, 120, 40 )

  def update_text(self):
    self.font = pygame.font.Font(None, 33)
    color = (255,0,0) if self.player == RED else (180,140,0)
    player_text = self.font.render(f"Player: {'RED' if self.player is RED else 'YELLOW'}", True, color) 
    self.surface.blit(player_text, (WIDTH+20, 100)) 

  def make_button(self, text, x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    font = pygame.font.Font(None, 33)
    text = font.render(text, True, (0, 0, 0))

    pygame.draw.rect(self.surface, (255, 255, 255), rect)
    self.surface.blit(text, text.get_rect(center=rect.center))
    return rect
    


  