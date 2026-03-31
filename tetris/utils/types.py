"""Shared type definitions for the Tetris project."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple

Color = Tuple[int, int, int]


@dataclass(frozen=True)
class Vec2:
    """Simple 2D vector for grid positions."""

    x: int
    y: int

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __iter__(self) -> Iterable[int]:
        return iter((self.x, self.y))
