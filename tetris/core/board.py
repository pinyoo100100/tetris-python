"""Board logic and collision detection."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from ..utils.constants import Tetromino
from ..utils.types import Vec2


@dataclass
class Board:
    """Represents the playfield grid."""

    width: int
    height: int
    grid: List[List[Optional[Tetromino]]] = field(init=False)

    def __post_init__(self) -> None:
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

    def reset(self) -> None:
        """Clear the board grid."""

        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = None

    def is_inside(self, x: int, y: int) -> bool:
        """Return True if coordinates are inside the board."""

        return 0 <= x < self.width and y < self.height

    def is_empty(self, x: int, y: int) -> bool:
        """Check whether a cell is empty or above the board."""

        if y < 0:
            return True
        return self.is_inside(x, y) and self.grid[y][x] is None

    def collides(self, cells: Iterable[Vec2]) -> bool:
        """Return True if any cell collides with existing blocks or bounds."""

        for cell in cells:
            if cell.x < 0 or cell.x >= self.width or cell.y >= self.height:
                return True
            if cell.y >= 0 and self.grid[cell.y][cell.x] is not None:
                return True
        return False

    def lock_cells(self, cells: Iterable[Vec2], tetromino: Tetromino) -> None:
        """Lock cells onto the board grid."""

        for cell in cells:
            if cell.y >= 0:
                self.grid[cell.y][cell.x] = tetromino

    def clear_lines(self) -> List[int]:
        """Clear completed lines and return cleared row indices."""

        cleared: List[int] = []
        new_rows: List[List[Optional[Tetromino]]] = []
        for y in range(self.height - 1, -1, -1):
            if all(self.grid[y][x] is not None for x in range(self.width)):
                cleared.append(y)
            else:
                new_rows.append(self.grid[y])
        while len(new_rows) < self.height:
            new_rows.append([None for _ in range(self.width)])
        new_rows.reverse()
        self.grid = new_rows
        return cleared
