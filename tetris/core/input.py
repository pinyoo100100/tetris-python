"""Input handling for Tetris."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

import pygame

from ..config import GameConfig


@dataclass
class InputActions:
    """Aggregated input actions per frame."""

    move: int = 0
    rotate_cw: bool = False
    rotate_ccw: bool = False
    soft_drop: bool = False
    hard_drop: bool = False
    hold: bool = False
    pause: bool = False
    confirm: bool = False


@dataclass
class InputHandler:
    """Maps pygame input into game actions with DAS/ARR."""

    config: GameConfig
    key_bindings: Dict[str, int] = field(default_factory=lambda: {
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "soft_drop": pygame.K_DOWN,
        "hard_drop": pygame.K_SPACE,
        "rotate_cw": pygame.K_UP,
        "rotate_ccw": pygame.K_z,
        "hold": pygame.K_c,
        "pause": pygame.K_ESCAPE,
        "confirm": pygame.K_RETURN,
    })
    _held_time: Dict[str, float] = field(default_factory=dict)
    _repeat_timer: Dict[str, float] = field(default_factory=dict)

    def update(self, dt: float, events: list[pygame.event.Event]) -> InputActions:
        """Return actions for the current frame."""

        actions = InputActions()
        pressed = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.key_bindings["left"]:
                    actions.move -= 1
                    self._held_time["left"] = 0.0
                    self._repeat_timer["left"] = 0.0
                if event.key == self.key_bindings["right"]:
                    actions.move += 1
                    self._held_time["right"] = 0.0
                    self._repeat_timer["right"] = 0.0
                if event.key == self.key_bindings["rotate_cw"]:
                    actions.rotate_cw = True
                if event.key == self.key_bindings["rotate_ccw"]:
                    actions.rotate_ccw = True
                if event.key == self.key_bindings["hard_drop"]:
                    actions.hard_drop = True
                if event.key == self.key_bindings["hold"]:
                    actions.hold = True
                if event.key == self.key_bindings["pause"]:
                    actions.pause = True
                if event.key == self.key_bindings["confirm"]:
                    actions.confirm = True

        actions.soft_drop = pressed[self.key_bindings["soft_drop"]]

        for direction, value in (("left", -1), ("right", 1)):
            if pressed[self.key_bindings[direction]]:
                self._held_time[direction] = self._held_time.get(direction, 0.0) + dt
                if self._held_time[direction] >= self.config.das_delay:
                    self._repeat_timer[direction] = self._repeat_timer.get(direction, 0.0) + dt
                    if self._repeat_timer[direction] >= self.config.arr_interval:
                        self._repeat_timer[direction] = 0.0
                        actions.move += value
            else:
                self._held_time[direction] = 0.0
                self._repeat_timer[direction] = 0.0

        return actions
