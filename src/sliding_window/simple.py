from __future__ import annotations

"""Simple reference implementation for learning, understanding,
and hands-on work such as coding interviews.

This version keeps only the abstractions that matter for the algorithm and removes
heavier general-purpose abstractions from the main implementation.
"""

from collections import deque
from dataclasses import dataclass
from typing import Iterable, Iterator


@dataclass(frozen=True, slots=True)
class ValueIndex:
    """Simple value/index pair for the demo implementation."""

    value: int | float
    index: int


class _MonotonicQueue:
    """Simple monotonic queue that stores the current best value at the front."""

    def __init__(self) -> None:
        self._dq: deque[ValueIndex] = deque()

    def __len__(self) -> int:
        return len(self._dq)

    def __bool__(self) -> bool:
        return bool(self._dq)

    def peek_front(self) -> ValueIndex | None:
        return self._dq[0] if self._dq else None

    def push(self, value: int | float, index: int) -> None:
        while self._dq and self._should_discard(self._dq[-1].value, value):
            self._dq.pop()
        self._dq.append(ValueIndex(value=value, index=index))

    def pop(self) -> ValueIndex | None:
        return self._dq.popleft() if self._dq else None

    def clear(self) -> None:
        self._dq.clear()

    def _should_discard(self, queued_value: int | float, incoming_value: int | float) -> bool:
        raise NotImplementedError


class MonotonicMinQueue(_MonotonicQueue):
    """Queue that keeps the current minimum at the front."""

    def _should_discard(self, queued_value: int | float, incoming_value: int | float) -> bool:
        return queued_value >= incoming_value


class MonotonicMaxQueue(_MonotonicQueue):
    """Queue that keeps the current maximum at the front."""

    def _should_discard(self, queued_value: int | float, incoming_value: int | float) -> bool:
        return queued_value <= incoming_value


class _SlidingWindowBase:
    queue_type: type[MonotonicMinQueue] | type[MonotonicMaxQueue] = MonotonicMinQueue

    def __init__(self, window_size: int) -> None:
        if window_size <= 0:
            raise ValueError("window_size must be greater than 0")

        self.window_size = window_size
        self.next_index = 0
        self._queue = self.queue_type()

    def __len__(self) -> int:
        return min(self.next_index, self.window_size)

    def __bool__(self) -> bool:
        return bool(self._queue)

    def __repr__(self) -> str:
        name = self.__class__.__name__
        current = self.current()
        return (
            f"{name}(window_size={self.window_size}, size={len(self)}, "
            f"current={current!r})"
        )

    def is_full(self) -> bool:
        return self.next_index >= self.window_size

    def current(self) -> int | float:
        if not self._queue:
            raise IndexError("window is empty")
        return self._queue.peek_front().value

    def push(self, value: int | float) -> None:
        current_index = self.next_index
        self.next_index += 1

        self._evict_expired()
        self._queue.push(value, current_index)

    def extend(self, values: Iterable[int | float]) -> list[int | float]:
        return list(self.iter_values(values))

    def iter_values(self, values: Iterable[int | float]) -> Iterator[int | float]:
        for value in values:
            self.push(value)
            if self.is_full():
                yield self.current()

    def clear(self) -> None:
        self.next_index = 0
        self._queue.clear()

    def _evict_expired(self) -> None:
        window_pop_left_index = self.next_index - self.window_size
        if self._queue and self._queue.peek_front().index < window_pop_left_index:
            self._queue.pop()


class SlidingWindowMin(_SlidingWindowBase):
    """Plain sliding-window minimum implementation for ints and floats."""

    queue_type = MonotonicMinQueue

    def get_min(self) -> int | float:
        return self.current()


class SlidingWindowMax(_SlidingWindowBase):
    """Plain sliding-window maximum implementation for ints and floats."""

    queue_type = MonotonicMaxQueue

    def get_max(self) -> int | float:
        return self.current()


def sliding_window_minimums(
    values: Iterable[int | float], window_size: int
) -> Iterator[int | float]:
    """Yield the minimum for each full window over the input values."""

    window = SlidingWindowMin(window_size)
    yield from window.iter_values(values)


def sliding_window_maximums(
    values: Iterable[int | float], window_size: int
) -> Iterator[int | float]:
    """Yield the maximum for each full window over the input values."""

    window = SlidingWindowMax(window_size)
    yield from window.iter_values(values)
