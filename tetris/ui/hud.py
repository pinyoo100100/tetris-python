"""Heads-up display rendering."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import pygame

from ..config import ACCENT_COLOR, GameConfig, TEXT_COLOR, TETROMINO_COLORS
from ..utils.types import Vec2
from ..utils.constants import Tetromino
from ..core.game import Game


@dataclass
class Hud:
    """Draws score, level, and previews."""

    config: GameConfig
    font: pygame.font.Font = field(init=False)
    small_font: pygame.font.Font = field(init=False)

    def __post_init__(self) -> None:
        self.font = pygame.font.SysFont("rubik", 28)
        self.small_font = pygame.font.SysFont("rubik", 22)

    def draw(self, surface: pygame.Surface, origin: Vec2, game: Game) -> None:
        """Render the HUD elements."""

        board_width_px = self.config.board_width * self.config.cell_size
        panel_x = origin.x + board_width_px + 24
        panel_y = origin.y

        self._draw_label(surface, "Score", panel_x, panel_y)
        self._draw_value(surface, f"{game.score.score:,}", panel_x, panel_y + 32)
        self._draw_label(surface, "Level", panel_x, panel_y + 80)
        self._draw_value(surface, f"{game.score.level}", panel_x, panel_y + 112)
        self._draw_label(surface, "Lines", panel_x, panel_y + 160)
        self._draw_value(surface, f"{game.score.lines}", panel_x, panel_y + 192)

        self._draw_label(surface, "Next", panel_x, panel_y + 250)
        self._draw_preview(surface, panel_x, panel_y + 280, game.next_queue[: self.config.next_preview_count])

        self._draw_label(surface, "Hold", panel_x, panel_y + 520)
        hold = [game.hold_piece] if game.hold_piece else []
        self._draw_preview(surface, panel_x, panel_y + 550, hold)

    def _draw_label(self, surface: pygame.Surface, text: str, x: int, y: int) -> None:
        label = self.small_font.render(text.upper(), True, ACCENT_COLOR)
        surface.blit(label, (x, y))

    def _draw_value(self, surface: pygame.Surface, text: str, x: int, y: int) -> None:
        value = self.font.render(text, True, TEXT_COLOR)
        surface.blit(value, (x, y))

    def _draw_preview(self, surface: pygame.Surface, x: int, y: int, pieces: List[Tetromino]) -> None:
        for index, tetromino in enumerate(pieces):
            if tetromino is None:
                continue
            color = TETROMINO_COLORS[tetromino.value]
            offset_y = y + index * 80
            for cell in self._preview_cells(tetromino):
                rect = pygame.Rect(x + cell.x * 20, offset_y + cell.y * 20, 20, 20)
                pygame.draw.rect(surface, color, rect, border_radius=4)
                pygame.draw.rect(surface, (255, 255, 255), rect, width=1, border_radius=4)

    def _preview_cells(self, tetromino: Tetromino) -> List[Vec2]:
        return {
            Tetromino.I: [Vec2(0, 1), Vec2(1, 1), Vec2(2, 1), Vec2(3, 1)],
            Tetromino.O: [Vec2(1, 0), Vec2(2, 0), Vec2(1, 1), Vec2(2, 1)],
            Tetromino.T: [Vec2(1, 0), Vec2(0, 1), Vec2(1, 1), Vec2(2, 1)],
            Tetromino.S: [Vec2(1, 0), Vec2(2, 0), Vec2(0, 1), Vec2(1, 1)],
            Tetromino.Z: [Vec2(0, 0), Vec2(1, 0), Vec2(1, 1), Vec2(2, 1)],
            Tetromino.J: [Vec2(0, 0), Vec2(0, 1), Vec2(1, 1), Vec2(2, 1)],
            Tetromino.L: [Vec2(2, 0), Vec2(0, 1), Vec2(1, 1), Vec2(2, 1)],
        }[tetromino]
