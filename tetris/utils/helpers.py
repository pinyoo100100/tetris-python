"""Helper utilities used across systems."""

from __future__ import annotations

from typing import Iterable


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp a number into the provided range."""

    return max(min_value, min(value, max_value))


def lerp(start: float, end: float, factor: float) -> float:
    """Linear interpolation between start and end."""

    return start + (end - start) * factor


def chunks(sequence: Iterable, size: int) -> list[list]:
    """Split a sequence into fixed-size chunks."""

    chunked: list[list] = []
    current: list = []
    for item in sequence:
        current.append(item)
        if len(current) == size:
            chunked.append(current)
            current = []
    if current:
        chunked.append(current)
    return chunked
