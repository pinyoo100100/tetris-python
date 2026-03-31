"""Animation state tracking for line clears and movement."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class LineClearAnimation:
    """Tracks line clear animation timing."""

    duration: float = 0.25
    timer: float = 0.0
    active_rows: List[int] = field(default_factory=list)

    def trigger(self, rows: List[int]) -> None:
        """Start a new line clear animation."""

        self.active_rows = rows
        self.timer = self.duration if rows else 0.0

    def update(self, dt: float) -> None:
        """Advance the animation timer."""

        if self.timer > 0.0:
            self.timer = max(0.0, self.timer - dt)

    def is_active(self) -> bool:
        """Return True while the animation is running."""

        return self.timer > 0.0

    def intensity(self) -> float:
        """Return normalized intensity for the animation."""

        if self.duration == 0:
            return 0.0
        return self.timer / self.duration
