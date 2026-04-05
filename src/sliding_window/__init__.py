"""Sliding-window min/max primitives backed by monotonic queues."""

from .core import (
    MonotonicMinQueue,
    MonotonicMaxQueue,
    SlidingWindowMin,
    SlidingWindowMax,
    ValueIndex,
    sliding_window_maximums,
    sliding_window_minimums,
)
from .simple import (
    MonotonicMaxQueue as SimpleMonotonicMaxQueue,
    MonotonicMinQueue as SimpleMonotonicMinQueue,
    SlidingWindowMax as SimpleSlidingWindowMax,
    SlidingWindowMin as SimpleSlidingWindowMin,
    ValueIndex as SimpleValueIndex,
    sliding_window_maximums as simple_sliding_window_maximums,
    sliding_window_minimums as simple_sliding_window_minimums,
)

__all__ = [
    "MonotonicMinQueue",
    "MonotonicMaxQueue",
    "SlidingWindowMin",
    "SlidingWindowMax",
    "ValueIndex",
    "sliding_window_minimums",
    "sliding_window_maximums",
    "SimpleMonotonicMaxQueue",
    "SimpleMonotonicMinQueue",
    "SimpleSlidingWindowMax",
    "SimpleSlidingWindowMin",
    "SimpleValueIndex",
    "simple_sliding_window_maximums",
    "simple_sliding_window_minimums",
]
