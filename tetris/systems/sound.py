"""Sound effects loader (optional)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pygame


@dataclass
class SoundSystem:
    """Lazy-loading sound effects to keep gameplay optional."""

    enabled: bool = True
    rotate: Optional[pygame.mixer.Sound] = None
    clear: Optional[pygame.mixer.Sound] = None
    drop: Optional[pygame.mixer.Sound] = None

    def load(self, base_path: str) -> None:
        """Load audio files if available."""

        if not self.enabled:
            return
        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False
            return
        self.rotate = self._safe_load(base_path, "rotate.wav")
        self.clear = self._safe_load(base_path, "clear.wav")
        self.drop = self._safe_load(base_path, "drop.wav")

    def _safe_load(self, base_path: str, name: str) -> Optional[pygame.mixer.Sound]:
        try:
            return pygame.mixer.Sound(f"{base_path}/{name}")
        except pygame.error:
            return None

    def play(self, sound: Optional[pygame.mixer.Sound]) -> None:
        """Play a sound if available."""

        if self.enabled and sound:
            sound.play()
