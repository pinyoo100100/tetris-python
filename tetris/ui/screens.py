"""Screen overlays for menu and pause states."""

from __future__ import annotations

from dataclasses import dataclass, field

import pygame

from ..config import ACCENT_COLOR, GameConfig, TEXT_COLOR


@dataclass
class ScreenManager:
    """Render high-level game screens."""

    config: GameConfig
    title_font: pygame.font.Font = field(init=False)
    subtitle_font: pygame.font.Font = field(init=False)

    def __post_init__(self) -> None:
        self.title_font = pygame.font.SysFont("rubik", 56)
        self.subtitle_font = pygame.font.SysFont("rubik", 28)

    def draw_menu(self, surface: pygame.Surface) -> None:
        """Draw the main menu overlay."""

        self._draw_overlay(surface, "TETRIS", "Press Enter to start")

    def draw_pause(self, surface: pygame.Surface) -> None:
        """Draw the paused overlay."""

        self._draw_overlay(surface, "PAUSED", "Press Esc to resume")

    def draw_game_over(self, surface: pygame.Surface, score: int) -> None:
        """Draw the game over overlay."""

        self._draw_overlay(surface, "GAME OVER", f"Score: {score:,} • Press Enter")

    def _draw_overlay(self, surface: pygame.Surface, title: str, subtitle: str) -> None:
        overlay = pygame.Surface((self.config.screen_width, self.config.screen_height), pygame.SRCALPHA)
        overlay.fill((10, 12, 16, 180))
        surface.blit(overlay, (0, 0))

        title_surf = self.title_font.render(title, True, TEXT_COLOR)
        subtitle_surf = self.subtitle_font.render(subtitle, True, ACCENT_COLOR)
        title_rect = title_surf.get_rect(center=(self.config.screen_width // 2, self.config.screen_height // 2 - 40))
        subtitle_rect = subtitle_surf.get_rect(center=(self.config.screen_width // 2, self.config.screen_height // 2 + 20))
        surface.blit(title_surf, title_rect)
        surface.blit(subtitle_surf, subtitle_rect)
