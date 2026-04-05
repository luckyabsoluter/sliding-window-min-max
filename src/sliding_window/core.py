from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import Deque, Generic, Iterable, Iterator, Optional, Protocol, TypeVar


class SupportsOrder(Protocol):
    def __lt__(self, other: object, /) -> bool: ...

    def __le__(self, other: object, /) -> bool: ...

    def __gt__(self, other: object, /) -> bool: ...

    def __ge__(self, other: object, /) -> bool: ...


T = TypeVar("T", bound=SupportsOrder)


@dataclass(frozen=True, slots=True)
class ValueIndex(Generic[T]):
    """A value paired with the index at which it entered the window."""

    value: T
    index: int


class _MonotonicQueue(Generic[T], ABC):
    """Internal queue that keeps the best candidate at the head."""

    def __init__(self) -> None:
        self._dq: Deque[ValueIndex[T]] = deque()

    def __len__(self) -> int:
        return len(self._dq)

    def __bool__(self) -> bool:
        return bool(self._dq)

    def push(self, element: ValueIndex[T]) -> None:
        while self._dq and self._should_discard(self._dq[-1].value, element.value):
            self._dq.pop()
        self._dq.append(element)

    def pop(self) -> Optional[ValueIndex[T]]:
        return self._dq.popleft() if self._dq else None

    def peek_front(self) -> Optional[ValueIndex[T]]:
        return self._dq[0] if self._dq else None

    def clear(self) -> None:
        self._dq.clear()

    @abstractmethod
    def _should_discard(self, queued_value: T, incoming_value: T) -> bool:
        """Return True when the queued value is dominated by the incoming value."""


class MonotonicMinQueue(_MonotonicQueue[T]):
    """Queue that keeps values in increasing order."""

    def _should_discard(self, queued_value: T, incoming_value: T) -> bool:
        return queued_value >= incoming_value


class MonotonicMaxQueue(_MonotonicQueue[T]):
    """Queue that keeps values in decreasing order."""

    def _should_discard(self, queued_value: T, incoming_value: T) -> bool:
        return queued_value <= incoming_value


class _SlidingWindowBase(Generic[T], ABC):
    """Shared monotonic sliding-window implementation."""

    queue_type: type[_MonotonicQueue[T]]

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

    def push(self, value: T) -> None:
        current_index = self.next_index
        self.next_index += 1

        self._evict_expired()
        self._queue.push(ValueIndex(value=value, index=current_index))

    def extend(self, values: Iterable[T]) -> list[T]:
        return list(self.iter_values(values))

    def clear(self) -> None:
        self.next_index = 0
        self._queue.clear()

    def is_full(self) -> bool:
        return self.next_index >= self.window_size

    def current(self) -> T:
        if not self._queue:
            raise IndexError("window is empty")
        return self._queue.peek_front().value

    def iter_values(self, values: Iterable[T]) -> Iterator[T]:
        for value in values:
            self.push(value)
            if self.is_full():
                yield self.current()

    def _evict_expired(self) -> None:
        window_pop_left_index = self.next_index - self.window_size
        if self._queue and self._queue.peek_front().index < window_pop_left_index:
            self._queue.pop()


class SlidingWindowMin(_SlidingWindowBase[T]):
    """Tracks the minimum value of the active window."""

    queue_type = MonotonicMinQueue

    def get_min(self) -> T:
        return self.current()


class SlidingWindowMax(_SlidingWindowBase[T]):
    """Tracks the maximum value of the active window."""

    queue_type = MonotonicMaxQueue

    def get_max(self) -> T:
        return self.current()


def sliding_window_minimums(values: Iterable[T], window_size: int) -> Iterator[T]:
    """Yield the minimum for each full window over the input values."""

    window = SlidingWindowMin[T](window_size)
    yield from window.iter_values(values)


def sliding_window_maximums(values: Iterable[T], window_size: int) -> Iterator[T]:
    """Yield the maximum for each full window over the input values."""

    window = SlidingWindowMax[T](window_size)
    yield from window.iter_values(values)
