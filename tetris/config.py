"""Global configuration for the Tetris game."""

from __future__ import annotations

from dataclasses import dataclass

from .utils.types import Color


@dataclass(frozen=True)
class GameConfig:
    """Immutable configuration values for the runtime."""

    screen_width: int = 960
    screen_height: int = 720
    fps: int = 60
    fixed_dt: float = 1 / 60
    board_width: int = 10
    board_height: int = 20
    cell_size: int = 32
    board_padding: int = 24
    side_panel_width: int = 260
    next_preview_count: int = 3
    lock_delay: float = 0.5
    das_delay: float = 0.16
    arr_interval: float = 0.05
    soft_drop_multiplier: float = 12.0
    hard_drop_score: int = 2
    soft_drop_score: int = 1


BACKGROUND_COLOR: Color = (18, 22, 28)
GRID_COLOR: Color = (38, 44, 54)
TEXT_COLOR: Color = (230, 235, 245)
PANEL_COLOR: Color = (28, 33, 41)
ACCENT_COLOR: Color = (88, 204, 255)
GHOST_ALPHA: int = 80

TETROMINO_COLORS: dict[str, Color] = {
    "I": (68, 214, 255),
    "O": (255, 221, 85),
    "T": (181, 110, 255),
    "S": (120, 220, 120),
    "Z": (255, 110, 110),
    "J": (110, 140, 255),
    "L": (255, 170, 90),
}
