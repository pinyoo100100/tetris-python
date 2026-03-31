"""Game state management and update loop."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

import pygame

from ..config import GameConfig
from ..utils.constants import GameState, Tetromino
from ..utils.types import Vec2
from .board import Board
from .input import InputHandler
from .piece import Piece
from .score import ScoreManager


# Game orchestrates pure gameplay logic; rendering and UI live elsewhere.

@dataclass
class Game:
    """Coordinates game logic and state transitions."""

    config: GameConfig
    board: Board = field(init=False)
    score: ScoreManager = field(default_factory=ScoreManager)
    input_handler: InputHandler = field(init=False)
    state: GameState = GameState.MENU
    current_piece: Optional[Piece] = None
    hold_piece: Optional[Tetromino] = None
    hold_used: bool = False
    next_queue: List[Tetromino] = field(default_factory=list)
    fall_timer: float = 0.0
    lock_timer: float = 0.0
    last_cleared: List[int] = field(default_factory=list)
    soft_drop_active: bool = False

    def __post_init__(self) -> None:
        self.board = Board(self.config.board_width, self.config.board_height)
        self.input_handler = InputHandler(self.config)
        self.refill_bag()

    def reset(self) -> None:
        """Reset the game to a fresh state."""

        self.board.reset()
        self.score.reset()
        self.state = GameState.PLAYING
        self.current_piece = None
        self.hold_piece = None
        self.hold_used = False
        self.next_queue.clear()
        self.refill_bag()
        self.spawn_piece()
        self.fall_timer = 0.0
        self.lock_timer = 0.0
        self.last_cleared = []

    def update(self, dt: float, events: list[pygame.event.Event]) -> None:
        """Advance the game simulation."""

        actions = self.input_handler.update(dt, events)

        if self.state == GameState.MENU:
            if actions.confirm:
                self.reset()
            return
        if self.state == GameState.GAME_OVER:
            if actions.confirm:
                self.reset()
            return
        if self.state == GameState.PAUSED:
            if actions.pause:
                self.state = GameState.PLAYING
            return

        if actions.pause:
            self.state = GameState.PAUSED
            return

        if self.current_piece is None:
            self.spawn_piece()

        self.last_cleared = []
        self.soft_drop_active = actions.soft_drop

        if actions.hold:
            self.hold_current()
        if actions.rotate_cw:
            self.rotate_piece(1)
        if actions.rotate_ccw:
            self.rotate_piece(-1)
        if actions.move:
            self.move_piece(actions.move)
        if actions.hard_drop:
            self.hard_drop()
            return

        self.apply_gravity(dt, actions.soft_drop)

    def refill_bag(self) -> None:
        """Ensure the next queue has enough pieces using a 7-bag shuffle."""

        import random

        while len(self.next_queue) < 7:
            bag = list(Tetromino)
            random.shuffle(bag)
            self.next_queue.extend(bag)

    def spawn_piece(self) -> None:
        """Spawn a new piece from the queue."""

        self.refill_bag()
        tetromino = self.next_queue.pop(0)
        spawn_x = (self.board.width // 2) - 2
        self.current_piece = Piece(tetromino, Vec2(spawn_x, -2))
        self.hold_used = False
        if self.board.collides(self.current_piece.cells()):
            self.state = GameState.GAME_OVER

    def move_piece(self, dx: int) -> None:
        """Attempt to move the active piece horizontally."""

        if self.current_piece is None:
            return
        offset = Vec2(dx, 0)
        if not self.board.collides(self.current_piece.cells(offset=offset)):
            self.current_piece.position = self.current_piece.position + offset
            self.lock_timer = 0.0

    def rotate_piece(self, direction: int) -> None:
        """Rotate the active piece with SRS kicks."""

        if self.current_piece is None:
            return
        to_rotation = self.current_piece.rotated(direction)
        for kick in self.current_piece.kick_tests(to_rotation):
            new_cells = self.current_piece.cells(rotation=to_rotation, offset=kick)
            if not self.board.collides(new_cells):
                self.current_piece.rotate(to_rotation, kick)
                self.lock_timer = 0.0
                return

    def apply_gravity(self, dt: float, soft_drop: bool) -> None:
        """Apply gravity and lock delay behavior."""

        if self.current_piece is None:
            return
        interval = self.drop_interval()
        if soft_drop:
            interval /= self.config.soft_drop_multiplier

        self.fall_timer += dt
        while self.fall_timer >= interval:
            self.fall_timer -= interval
            if not self.try_move_down():
                self.lock_timer += interval
                if self.lock_timer >= self.config.lock_delay:
                    self.lock_piece()
                return
            else:
                self.lock_timer = 0.0
                if soft_drop:
                    self.score.add_drop(self.config.soft_drop_score)

    def drop_interval(self) -> float:
        """Return the current gravity interval based on level."""

        level = max(1, self.score.level)
        return max(0.05, 0.8 - (level - 1) * 0.07)

    def try_move_down(self) -> bool:
        """Move the piece down by one if possible."""

        if self.current_piece is None:
            return False
        offset = Vec2(0, 1)
        if not self.board.collides(self.current_piece.cells(offset=offset)):
            self.current_piece.position = self.current_piece.position + offset
            return True
        return False

    def hard_drop(self) -> None:
        """Instantly drop the piece and lock it."""

        if self.current_piece is None:
            return
        drop_distance = 0
        while self.try_move_down():
            drop_distance += 1
        if drop_distance:
            self.score.add_drop(drop_distance * self.config.hard_drop_score)
        self.lock_piece()

    def lock_piece(self) -> None:
        """Lock the current piece and resolve line clears."""

        if self.current_piece is None:
            return
        self.board.lock_cells(self.current_piece.cells(), self.current_piece.tetromino)
        cleared = self.board.clear_lines()
        self.last_cleared = cleared
        self.score.add_clear(len(cleared))
        self.current_piece = None
        self.lock_timer = 0.0

    def hold_current(self) -> None:
        """Hold or swap the active piece."""

        if self.current_piece is None or self.hold_used:
            return
        current = self.current_piece.tetromino
        if self.hold_piece is None:
            self.hold_piece = current
            self.current_piece = None
            self.spawn_piece()
            self.hold_used = True
            self.lock_timer = 0.0
            return

        self.current_piece = Piece(self.hold_piece, Vec2((self.board.width // 2) - 2, -2))
        self.hold_piece = current
        self.hold_used = True
        self.lock_timer = 0.0
        if self.current_piece and self.board.collides(self.current_piece.cells()):
            self.state = GameState.GAME_OVER

    def fall_progress(self) -> float:
        """Return interpolation progress for the falling piece."""

        if self.current_piece is None:
            return 0.0
        interval = self.drop_interval()
        if self.soft_drop_active:
            interval /= self.config.soft_drop_multiplier
        if interval <= 0:
            return 0.0
        if self.board.collides(self.current_piece.cells(offset=Vec2(0, 1))):
            return 0.0
        return min(1.0, self.fall_timer / interval)

    def ghost_offset(self) -> int:
        """Return the downward offset for the ghost piece."""

        if self.current_piece is None:
            return 0
        offset = 0
        while True:
            test_offset = Vec2(0, offset + 1)
            if self.board.collides(self.current_piece.cells(offset=test_offset)):
                return offset
            offset += 1
