"""Rendering system for the Tetris game."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

import pygame

from ..config import ACCENT_COLOR, BACKGROUND_COLOR, GameConfig, GRID_COLOR, PANEL_COLOR, TETROMINO_COLORS, GHOST_ALPHA
from ..utils.constants import GameState, Tetromino
from ..utils.types import Vec2
from ..utils.helpers import lerp
from ..core.game import Game
from .animation import LineClearAnimation
from ..ui.hud import Hud
from ..ui.screens import ScreenManager


@dataclass
class Renderer:
    """Draws the game state to the screen."""

    config: GameConfig
    line_animation: LineClearAnimation = field(default_factory=LineClearAnimation)
    hud: Hud = field(init=False)

    def __post_init__(self) -> None:
        self.hud = Hud(self.config)

    def render(self, surface: pygame.Surface, game: Game, screens: ScreenManager) -> None:
        """Render the entire frame."""

        surface.fill(BACKGROUND_COLOR)
        board_origin = self._board_origin()
        self.line_animation.update(self.config.fixed_dt)

        if game.last_cleared and not self.line_animation.is_active():
            self.line_animation.trigger(game.last_cleared)

        self._draw_board(surface, board_origin, game)
        self.hud.draw(surface, board_origin, game)

        if game.state == GameState.MENU:
            screens.draw_menu(surface)
        elif game.state == GameState.PAUSED:
            screens.draw_pause(surface)
        elif game.state == GameState.GAME_OVER:
            screens.draw_game_over(surface, game.score.score)

    def _board_origin(self) -> Vec2:
        board_width_px = self.config.board_width * self.config.cell_size
        board_height_px = self.config.board_height * self.config.cell_size
        total_width = board_width_px + self.config.side_panel_width + self.config.board_padding * 2
        offset_x = (self.config.screen_width - total_width) // 2 + self.config.board_padding
        offset_y = (self.config.screen_height - board_height_px) // 2
        return Vec2(offset_x, offset_y)

    def _draw_board(self, surface: pygame.Surface, origin: Vec2, game: Game) -> None:
        board_width_px = self.config.board_width * self.config.cell_size
        board_height_px = self.config.board_height * self.config.cell_size
        panel_rect = pygame.Rect(
            origin.x - self.config.board_padding,
            origin.y - self.config.board_padding,
            board_width_px + self.config.side_panel_width + self.config.board_padding * 2,
            board_height_px + self.config.board_padding * 2,
        )
        pygame.draw.rect(surface, PANEL_COLOR, panel_rect, border_radius=16)

        grid_rect = pygame.Rect(origin.x, origin.y, board_width_px, board_height_px)
        pygame.draw.rect(surface, (12, 15, 20), grid_rect, border_radius=8)

        for y in range(self.config.board_height):
            for x in range(self.config.board_width):
                cell_rect = self._cell_rect(origin, x, y)
                pygame.draw.rect(surface, GRID_COLOR, cell_rect, width=1)
                cell = game.board.grid[y][x]
                if cell:
                    self._draw_cell(surface, cell_rect, TETROMINO_COLORS[cell.value])

        if game.current_piece:
            ghost_offset = game.ghost_offset()
            self._draw_piece(
                surface,
                origin,
                game.current_piece.tetromino,
                game.current_piece.cells(offset=Vec2(0, ghost_offset)),
                ghost=True,
            )
            fall_offset = game.fall_progress() * self.config.cell_size
            self._draw_piece(
                surface,
                origin,
                game.current_piece.tetromino,
                game.current_piece.cells(),
                ghost=False,
                offset_y=fall_offset,
            )

        if self.line_animation.is_active():
            intensity = self.line_animation.intensity()
            for row in self.line_animation.active_rows:
                if row < 0 or row >= self.config.board_height:
                    continue
                overlay = pygame.Surface((board_width_px, self.config.cell_size), pygame.SRCALPHA)
                alpha = int(lerp(0, 200, intensity))
                overlay.fill((*ACCENT_COLOR, alpha))
                surface.blit(overlay, (origin.x, origin.y + row * self.config.cell_size))

    def _cell_rect(self, origin: Vec2, x: int, y: int) -> pygame.Rect:
        return pygame.Rect(
            origin.x + x * self.config.cell_size,
            origin.y + y * self.config.cell_size,
            self.config.cell_size,
            self.config.cell_size,
        )

    def _draw_cell(self, surface: pygame.Surface, rect: pygame.Rect, color: Tuple[int, int, int]) -> None:
        inner = rect.inflate(-4, -4)
        pygame.draw.rect(surface, color, inner, border_radius=4)
        highlight = inner.inflate(-6, -6)
        pygame.draw.rect(surface, (255, 255, 255), highlight, width=1, border_radius=3)

    def _draw_piece(
        self,
        surface: pygame.Surface,
        origin: Vec2,
        tetromino: Tetromino,
        cells: list[Vec2],
        ghost: bool,
        offset_y: float = 0.0,
    ) -> None:
        color = TETROMINO_COLORS[tetromino.value]
        for cell in cells:
            if cell.y < 0:
                continue
            rect = pygame.Rect(
                origin.x + cell.x * self.config.cell_size,
                origin.y + cell.y * self.config.cell_size + offset_y,
                self.config.cell_size,
                self.config.cell_size,
            )
            if ghost:
                ghost_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                ghost_surface.fill((*color, GHOST_ALPHA))
                surface.blit(ghost_surface, rect.topleft)
                pygame.draw.rect(surface, color, rect, width=1, border_radius=4)
            else:
                self._draw_cell(surface, rect, color)
