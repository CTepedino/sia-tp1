import pygame
from pygame.locals import *
import time
import sys
import json

from sokoban.rules import SokobanRules, Directions


TILE_SIZE = 50

TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0)
WIN_TEXT = "¡Ganaste!"

GROUND_TEXTURE = "assets/Ground_Concrete.png"
WALL_TEXTURE = "assets/Wall_Black.png"
BOX_TEXTURE = "assets/Crate_Brown.png"
BOX_IN_TARGET_TEXTURE = "assets/Crate_Beige.png"
TARGET_TEXTURE = "assets/EndPoint_Red.png"

PLAYER_UP = "assets/CharacterUP.png"
PLAYER_DOWN = "assets/CharacterDOWN.png"
PLAYER_SIDE = "assets/CharacterSIDE.png"

class Sokoban:
    def __init__(self, level):
        self.level = level
        self.game = SokobanRules(level)
        self.width = len(level[0])
        self.height = len(level)
        self.screen = None
        self.font = None

        self.wall_texture = pygame.image.load(WALL_TEXTURE)
        self.box_texture = pygame.image.load(BOX_TEXTURE)
        self.box_in_target_texture = pygame.image.load(BOX_IN_TARGET_TEXTURE)
        self.target_texture = pygame.image.load(TARGET_TEXTURE)
        self.background_texture = pygame.image.load(GROUND_TEXTURE)

        self.last_move = Directions.DOWN
        self.player_textures = {
            Directions.UP: pygame.image.load(PLAYER_UP),
            Directions.DOWN: pygame.image.load(PLAYER_DOWN),
            Directions.RIGHT: pygame.image.load(PLAYER_SIDE),
            Directions.LEFT: pygame.image.load(PLAYER_SIDE)
        }

    def draw(self, solved):
        for x in range(self.width):
            for y in range(self.height):
                self.screen.blit(self.background_texture, (x * TILE_SIZE, y * TILE_SIZE))

        for x, y in self.game.walls:
            self.screen.blit(self.wall_texture, (x * TILE_SIZE, y * TILE_SIZE))
        for x, y in self.game.targets:
            self.screen.blit(self.target_texture, (x * TILE_SIZE, y * TILE_SIZE))
        for x, y in self.game.boxes:
            if (x, y) in self.game.targets:
                self.screen.blit(self.box_in_target_texture, (x * TILE_SIZE, y * TILE_SIZE))
            else:
                self.screen.blit(self.box_texture, (x * TILE_SIZE, y * TILE_SIZE))

        px, py = self.game.player
        self.screen.blit(self.player_textures[self.last_move], (px * TILE_SIZE, py * TILE_SIZE))

        if solved:
            win_text = self.font.render(WIN_TEXT, True, TEXT_COLOR)
            shadow_text = self.font.render(WIN_TEXT, True, SHADOW_COLOR)
            self.screen.blit(shadow_text, (self.screen.get_width() // 2 - win_text.get_width() // 2 + 3, self.screen.get_height() // 2 - win_text.get_height() // 2 - 20 + 3))
            self.screen.blit(win_text, (self.screen.get_width() // 2 - win_text.get_width() // 2, self.screen.get_height() // 2 - win_text.get_height() // 2 -20))

            moves_font = pygame.font.Font(None, 30)
            moves_text = moves_font.render(f"Movimientos: {len(self.game.path)}", True, TEXT_COLOR)
            moves_shadow_text = moves_font.render(f"Movimientos: {len(self.game.path)}", True, SHADOW_COLOR)
            self.screen.blit(moves_shadow_text, (self.screen.get_width() // 2 - moves_text.get_width() // 2 + 3, self.screen.get_height() // 2 - moves_text.get_height() // 2 + 40  + 3))
            self.screen.blit(moves_text, (self.screen.get_width() // 2 - moves_text.get_width() // 2, self.screen.get_height() // 2 - moves_text.get_height() // 2 + 40))

    def reset(self):
        self.game = SokobanRules(level)
        self.last_move = Directions.DOWN

    def setup(self):
        pygame.init()
        pygame.display.set_caption("Sokoban")
        self.screen = pygame.display.set_mode((self.width * TILE_SIZE, self.height * TILE_SIZE))

        self.wall_texture = pygame.transform.scale(self.wall_texture, (TILE_SIZE, TILE_SIZE))
        self.box_texture = pygame.transform.scale(self.box_texture, (TILE_SIZE, TILE_SIZE))
        self.box_in_target_texture = pygame.transform.scale(self.box_in_target_texture, (TILE_SIZE, TILE_SIZE))
        self.target_texture = pygame.transform.scale(self.target_texture, (TILE_SIZE, TILE_SIZE))
        self.background_texture = pygame.transform.scale(self.background_texture, (TILE_SIZE, TILE_SIZE))

        self.player_textures[Directions.UP] = pygame.transform.scale(self.player_textures[Directions.UP], (TILE_SIZE, TILE_SIZE))
        self.player_textures[Directions.DOWN] = pygame.transform.scale(self.player_textures[Directions.DOWN], (TILE_SIZE, TILE_SIZE))
        self.player_textures[Directions.LEFT] = pygame.transform.scale(self.player_textures[Directions.LEFT],(TILE_SIZE, TILE_SIZE))
        self.player_textures[Directions.RIGHT] = pygame.transform.scale(self.player_textures[Directions.RIGHT], (TILE_SIZE, TILE_SIZE))
        self.player_textures[Directions.RIGHT] = pygame.transform.flip(self.player_textures[Directions.RIGHT], True, False)

        self.font = pygame.font.SysFont("Arial", 48, bold=True)
    def start(self):
        self.setup()

        clock = pygame.time.Clock()
        running = True

        solved = self.game.is_solved()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and not solved:
                    if event.key == K_r:
                        self.reset()
                        break
                    if event.key in (K_UP, K_w): self.last_move = Directions.UP
                    elif event.key in (K_DOWN, K_s): self.last_move = Directions.DOWN
                    elif event.key in (K_LEFT, K_a): self.last_move = Directions.LEFT
                    elif event.key in (K_RIGHT, K_d): self.last_move = Directions.RIGHT


                    self.game.move_to(self.last_move)
                    solved = self.game.is_solved()

            self.draw(solved)
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()


    def automatic_game(self, solution):
        self.setup()

        clock = pygame.time.Clock()

        self.draw(False)
        pygame.display.flip()

        running = True
        moves_iter = iter(solution)
        has_moves = True

        while running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    break
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False
                    break

            if has_moves:
                try:
                    move = next(moves_iter)
                    time.sleep(0.225)
                    self.last_move = Directions(move)
                    self.game.move_to(self.last_move)

                except StopIteration:
                    has_moves = False

            self.draw(self.game.is_solved())
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()


                   


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        config = json.load(f)
        level = config["level"]

    game = Sokoban(level)
    game.start()