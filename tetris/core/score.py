"""Scoring and level progression."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScoreManager:
    """Tracks score, lines, and level progression."""

    score: int = 0
    level: int = 1
    lines: int = 0
    combo: int = -1

    def reset(self) -> None:
        """Reset score-related values."""

        self.score = 0
        self.level = 1
        self.lines = 0
        self.combo = -1

    def add_clear(self, cleared: int) -> int:
        """Apply scoring for cleared lines and return added score."""

        if cleared == 0:
            self.combo = -1
            return 0

        self.combo += 1
        line_scores = {1: 100, 2: 300, 3: 500, 4: 800}
        base = line_scores.get(cleared, 0)
        combo_bonus = max(0, self.combo) * 50
        added = (base + combo_bonus) * self.level
        self.score += added
        self.lines += cleared
        if self.lines // 10 + 1 > self.level:
            self.level = self.lines // 10 + 1
        return added

    def add_drop(self, amount: int) -> None:
        """Add score from soft/hard drops."""

        self.score += amount
