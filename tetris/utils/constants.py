"""Core constants and enums for the Tetris ruleset."""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Tuple

from .types import Vec2


class GameState(Enum):
    """High-level game states."""

    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class Tetromino(Enum):
    """Enumerates the available tetromino types."""

    I = "I"
    O = "O"
    T = "T"
    S = "S"
    Z = "Z"
    J = "J"
    L = "L"


Rotation = int


SHAPES: Dict[Tetromino, List[List[Vec2]]] = {
    Tetromino.I: [
        [Vec2(0, 1), Vec2(1, 1), Vec2(2, 1), Vec2(3, 1)],
        [Vec2(2, 0), Vec2(2, 1), Vec2(2, 2), Vec2(2, 3)],
        [Vec2(0, 2), Vec2(1, 2), Vec2(2, 2), Vec2(3, 2)],
        [Vec2(1, 0), Vec2(1, 1), Vec2(1, 2), Vec2(1, 3)],
    ],
    Tetromino.O: [
        [Vec2(1, 0), Vec2(2, 0), Vec2(1, 1), Vec2(2, 1)],
        [Vec2(1, 0), Vec2(2, 0), Vec2(1, 1), Vec2(2, 1)],
        [Vec2(1, 0), Vec2(2, 0), Vec2(1, 1), Vec2(2, 1)],
        [Vec2(1, 0), Vec2(2, 0), Vec2(1, 1), Vec2(2, 1)],
    ],
    Tetromino.T: [
        [Vec2(1, 0), Vec2(0, 1), Vec2(1, 1), Vec2(2, 1)],
        [Vec2(1, 0), Vec2(1, 1), Vec2(2, 1), Vec2(1, 2)],
        [Vec2(0, 1), Vec2(1, 1), Vec2(2, 1), Vec2(1, 2)],
        [Vec2(1, 0), Vec2(0, 1), Vec2(1, 1), Vec2(1, 2)],
    ],
    Tetromino.S: [
        [Vec2(1, 0), Vec2(2, 0), Vec2(0, 1), Vec2(1, 1)],
        [Vec2(1, 0), Vec2(1, 1), Vec2(2, 1), Vec2(2, 2)],
        [Vec2(1, 1), Vec2(2, 1), Vec2(0, 2), Vec2(1, 2)],
        [Vec2(0, 0), Vec2(0, 1), Vec2(1, 1), Vec2(1, 2)],
    ],
    Tetromino.Z: [
        [Vec2(0, 0), Vec2(1, 0), Vec2(1, 1), Vec2(2, 1)],
        [Vec2(2, 0), Vec2(1, 1), Vec2(2, 1), Vec2(1, 2)],
        [Vec2(0, 1), Vec2(1, 1), Vec2(1, 2), Vec2(2, 2)],
        [Vec2(1, 0), Vec2(0, 1), Vec2(1, 1), Vec2(0, 2)],
    ],
    Tetromino.J: [
        [Vec2(0, 0), Vec2(0, 1), Vec2(1, 1), Vec2(2, 1)],
        [Vec2(1, 0), Vec2(2, 0), Vec2(1, 1), Vec2(1, 2)],
        [Vec2(0, 1), Vec2(1, 1), Vec2(2, 1), Vec2(2, 2)],
        [Vec2(1, 0), Vec2(1, 1), Vec2(0, 2), Vec2(1, 2)],
    ],
    Tetromino.L: [
        [Vec2(2, 0), Vec2(0, 1), Vec2(1, 1), Vec2(2, 1)],
        [Vec2(1, 0), Vec2(1, 1), Vec2(1, 2), Vec2(2, 2)],
        [Vec2(0, 1), Vec2(1, 1), Vec2(2, 1), Vec2(0, 2)],
        [Vec2(0, 0), Vec2(1, 0), Vec2(1, 1), Vec2(1, 2)],
    ],
}


KickTable = Dict[Tuple[Rotation, Rotation], List[Vec2]]

JLSTZ_KICKS: KickTable = {
    (0, 1): [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, 1), Vec2(0, -2), Vec2(-1, -2)],
    (1, 0): [Vec2(0, 0), Vec2(1, 0), Vec2(1, -1), Vec2(0, 2), Vec2(1, 2)],
    (1, 2): [Vec2(0, 0), Vec2(1, 0), Vec2(1, -1), Vec2(0, 2), Vec2(1, 2)],
    (2, 1): [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, 1), Vec2(0, -2), Vec2(-1, -2)],
    (2, 3): [Vec2(0, 0), Vec2(1, 0), Vec2(1, 1), Vec2(0, -2), Vec2(1, -2)],
    (3, 2): [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, -1), Vec2(0, 2), Vec2(-1, 2)],
    (3, 0): [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, -1), Vec2(0, 2), Vec2(-1, 2)],
    (0, 3): [Vec2(0, 0), Vec2(1, 0), Vec2(1, 1), Vec2(0, -2), Vec2(1, -2)],
}

I_KICKS: KickTable = {
    (0, 1): [Vec2(0, 0), Vec2(-2, 0), Vec2(1, 0), Vec2(-2, -1), Vec2(1, 2)],
    (1, 0): [Vec2(0, 0), Vec2(2, 0), Vec2(-1, 0), Vec2(2, 1), Vec2(-1, -2)],
    (1, 2): [Vec2(0, 0), Vec2(-1, 0), Vec2(2, 0), Vec2(-1, 2), Vec2(2, -1)],
    (2, 1): [Vec2(0, 0), Vec2(1, 0), Vec2(-2, 0), Vec2(1, -2), Vec2(-2, 1)],
    (2, 3): [Vec2(0, 0), Vec2(2, 0), Vec2(-1, 0), Vec2(2, 1), Vec2(-1, -2)],
    (3, 2): [Vec2(0, 0), Vec2(-2, 0), Vec2(1, 0), Vec2(-2, -1), Vec2(1, 2)],
    (3, 0): [Vec2(0, 0), Vec2(1, 0), Vec2(-2, 0), Vec2(1, -2), Vec2(-2, 1)],
    (0, 3): [Vec2(0, 0), Vec2(-1, 0), Vec2(2, 0), Vec2(-1, 2), Vec2(2, -1)],
}


KICK_TABLES: Dict[Tetromino, KickTable] = {
    Tetromino.I: I_KICKS,
    Tetromino.O: {},
    Tetromino.T: JLSTZ_KICKS,
    Tetromino.S: JLSTZ_KICKS,
    Tetromino.Z: JLSTZ_KICKS,
    Tetromino.J: JLSTZ_KICKS,
    Tetromino.L: JLSTZ_KICKS,
}
