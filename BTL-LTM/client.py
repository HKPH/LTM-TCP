import pygame
import sys
import socket
import threading

from utils import *
from entity import *
from tilemap import *


class ClientGame:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("ninja game")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            "decor": load_images("data/images/tiles/decor"),
            "grass": load_images("data/images/tiles/grass"),
            "large_decor": load_images("data/images/tiles/large_decor"),
            "stone": load_images("data/images/tiles/stone"),
            "player": load_img("data/images/entities/player.png"),
            "background": load_img("data/images/background.png"),
            "player/idle": Animations(
                load_images("data/images/entities/player/idle"), img_dur=6
            ),
            "player/run": Animations(
                load_images("data/images/entities/player/run"), img_dur=4
            ),
            "player/jump": Animations(load_images("data/images/entities/player/jump")),
            "player/slide": Animations(
                load_images("data/images/entities/player/slide")
            ),
            "player/wall_slide": Animations(
                load_images("data/images/entities/player/wall_slide")
            ),
        }

        self.player = Player(self, (50, 50), (8, 15))
        self.player_id = None

        self.tilemap = Tilemap(self, tile_size=16)

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.display.blit(self.assets["background"], (0, 0))

            self.scroll[0] += (
                self.player.rect().centerx
                - self.display.get_width() / 2
                - self.scroll[0]
            ) / 30
            self.scroll[1] += (
                self.player.rect().centery
                - self.display.get_height() / 2
                - self.scroll[1]
            ) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                        self.send_data(f"move:left:{self.player_id}")
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                        self.send_data(f"move:right:{self.player_id}")
                    if event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -3
                        self.send_data(f"jump:{self.player_id}")
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                        self.send_data(f"stop:left:{self.player_id}")
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                        self.send_data(f"stop:right:{self.player_id}")

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    client_game = ClientGame()
    client_game.run()
