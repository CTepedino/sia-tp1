# import pygame
# from pygame.locals import *

# # Definimos constantes
# TILE_SIZE = 50
# PLAYER_COLOR = (0, 0, 255)
# BOX_COLOR = (139, 69, 19)
# TARGET_COLOR = (255, 0, 0)
# WALL_COLOR = (128, 128, 128)
# BACKGROUND_COLOR = (200, 200, 200)
# TEXT_COLOR = (255, 255, 255)

# class Sokoban:
#     def __init__(self, level,current_level):
#         self.levels = level  # Usamos el nivel pasado al constructor
#         self.width = len(self.levels[0][0])
#         self.height = len(self.levels[0])
#         self.load_level(current_level)  # Inicializamos con el primer nivel

#     def load_level(self, level_index):
#         self.player_pos = None
#         self.boxes = set()
#         self.targets = set()
#         self.walls = set()
#         level = self.levels[level_index]
#         for y, row in enumerate(level):
#             for x, cell in enumerate(row):
#                 if cell == "P":
#                     self.player_pos = (x, y)
#                 elif cell == "#":
#                     self.walls.add((x, y))
#                 elif cell == "B":
#                     self.boxes.add((x, y))
#                 elif cell == "T":
#                     self.targets.add((x, y))

#     def move(self, dx, dy):
#         px, py = self.player_pos
#         new_pos = (px + dx, py + dy)

#         if new_pos in self.walls:
#             return

#         if new_pos in self.boxes:
#             new_box_pos = (new_pos[0] + dx, new_pos[1] + dy)
#             if new_box_pos in self.walls or new_box_pos in self.boxes:
#                 return
#             self.boxes.remove(new_pos)
#             self.boxes.add(new_box_pos)

#         self.player_pos = new_pos

#     def is_solved(self):
#         return self.boxes == self.targets

#     def draw(self, screen, font, game_won):
#         screen.fill(BACKGROUND_COLOR)
#         for x, y in self.walls:
#             pygame.draw.rect(screen, WALL_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
#         for x, y in self.targets:
#             pygame.draw.rect(screen, TARGET_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
#         for x, y in self.boxes:
#             pygame.draw.rect(screen, BOX_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
#         # Dibuja al jugador con la letra "P"
#         px, py = self.player_pos
#         pygame.draw.rect(screen, PLAYER_COLOR, (px * TILE_SIZE, py * TILE_SIZE, TILE_SIZE, TILE_SIZE))
#         player_text = font.render("P", True, (0, 0, 0))
#         screen.blit(player_text, (px * TILE_SIZE + TILE_SIZE // 4, py * TILE_SIZE + TILE_SIZE // 4))

#         # Si el juego está ganado, mostramos el mensaje
#         if game_won:
#             win_text = font.render("¡Ganaste!", True, TEXT_COLOR)
#             screen.blit(win_text, (screen.get_width() // 2 - win_text.get_width() // 2, screen.get_height() // 2 - win_text.get_height() // 2))

#     def start(self, current_level):
#         pygame.init()
        
#         screen = pygame.display.set_mode((self.width * TILE_SIZE, self.height * TILE_SIZE))
#         clock = pygame.time.Clock()
#         font = pygame.font.SysFont("Arial", 24)
#         game_won = False
#         running = True
        
#         while running:
#             for event in pygame.event.get():
#                 if event.type == QUIT:
#                     running = False
#                 elif event.type == KEYDOWN:
#                     if event.key == K_UP:
#                         self.move(0, -1)
#                     elif event.key == K_DOWN:
#                         self.move(0, 1)
#                     elif event.key == K_LEFT:
#                         self.move(-1, 0)
#                     elif event.key == K_RIGHT:
#                         self.move(1, 0)
#                     elif event.key == K_n and self.is_solved():
#                         current_level = (current_level + 1) % len(self.levels)
#                         self.load_level(current_level)  # Recargar el nivel con el nuevo índice
#                         game_won = False  # Resetea el estado de "ganado"

#             if self.is_solved() and not game_won:
#                 game_won = True  # El jugador ganó el nivel
            
#             self.draw(screen, font, game_won)
#             pygame.display.flip()
#             clock.tick(30)

#         pygame.quit()

# def main():
#     levels = [
#         [
#             "######",
#             "#P   #",
#             "# B T#",
#             "######"
#         ],
#         [
#             "#######",
#             "#P    #",
#             "# B T #",
#             "#  B T#",
#             "#######"
#         ]
#     ]
#     game = Sokoban(levels,0)  # Pasamos los niveles al constructor
#     game.start(0)  # Llamamos a la función `start` pasando el nivel 0 al iniciar

# if __name__ == "__main__":
#     main()
