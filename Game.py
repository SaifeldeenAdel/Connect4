import pygame

ROWS = 6
COLUMNS = 7
CELL_SIZE = 120

WIDTH = COLUMNS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

RED = 1
YELLOW = 2

class Game:
  def __init__(self) -> None:
    pygame.init()
    self.playing = False
    self.player = RED
    self.current_state = None
    self.font = None
    self.font = pygame.font.Font(None, 33)

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
        

  def update_text(self):
    player_text = self.font.render(f"Player: {'RED' if self.player is RED else 'BLACK'}", True, (0, 0, 0)) 
    self.surface.blit(player_text, (WIDTH+40, 100)) 

    


  