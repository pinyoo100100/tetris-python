"""Tetris entry point."""

from __future__ import annotations

import os
import sys

if __package__ is None or __package__ == "":
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pygame

from tetris.config import GameConfig
from tetris.core.game import Game
from tetris.systems.renderer import Renderer
from tetris.ui.screens import ScreenManager


def main() -> None:
    """Boot the Tetris game."""

    pygame.init()
    pygame.display.set_caption("Tetris")
    config = GameConfig()
    screen = pygame.display.set_mode((config.screen_width, config.screen_height))
    clock = pygame.time.Clock()

    game = Game(config)
    renderer = Renderer(config)
    screens = ScreenManager(config)

    # Fixed timestep updates keep gameplay deterministic across frame rates.

    accumulator = 0.0
    running = True
    while running:
        dt = clock.tick(config.fps) / 1000.0
        accumulator += dt

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        first_step = True
        while accumulator >= config.fixed_dt:
            game.update(config.fixed_dt, events if first_step else [])
            accumulator -= config.fixed_dt
            first_step = False

        renderer.render(screen, game, screens)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
