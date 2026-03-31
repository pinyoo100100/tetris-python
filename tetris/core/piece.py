"""Tetromino piece logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from ..utils.constants import KICK_TABLES, SHAPES, Tetromino
from ..utils.types import Vec2


@dataclass
class Piece:
    """Represents a falling tetromino."""

    tetromino: Tetromino
    position: Vec2
    rotation: int = 0

    def cells(self, rotation: int | None = None, offset: Vec2 | None = None) -> List[Vec2]:
        """Return occupied cells in board coordinates."""

        rotation_index = self.rotation if rotation is None else rotation % 4
        base = SHAPES[self.tetromino][rotation_index]
        origin = self.position if offset is None else self.position + offset
        return [origin + cell for cell in base]

    def rotated(self, direction: int) -> int:
        """Return the new rotation index after applying direction."""

        return (self.rotation + direction) % 4

    def kick_tests(self, to_rotation: int) -> Iterable[Vec2]:
        """Return SRS kick offsets for a rotation transition."""

        kick_table = KICK_TABLES.get(self.tetromino, {})
        return kick_table.get((self.rotation, to_rotation), [Vec2(0, 0)])

    def rotate(self, to_rotation: int, offset: Vec2) -> None:
        """Apply a rotation and offset after a successful kick."""

        self.rotation = to_rotation
        self.position = self.position + offset
