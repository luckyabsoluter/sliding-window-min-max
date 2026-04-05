from __future__ import annotations

import pytest

from sliding_window import (
    SlidingWindowMax,
    SlidingWindowMin,
    sliding_window_maximums,
    sliding_window_minimums,
)


def test_sliding_window_min_tracks_expected_values() -> None:
    data = [4, 3, 5, 4, 3, 3, 6, 7]
    # Windows: [4, 3, 5], [3, 5, 4], [5, 4, 3], [4, 3, 3], [3, 3, 6], [3, 6, 7]
    expected = [3, 3, 3, 3, 3, 3]

    window = SlidingWindowMin[int](3)

    result = []
    for value in data:
        window.push(value)
        if window.is_full():
            result.append(window.get_min())

    assert result == expected


def test_sliding_window_max_tracks_expected_values() -> None:
    data = [4, 3, 5, 4, 3, 3, 6, 7]
    # Windows: [4, 3, 5], [3, 5, 4], [5, 4, 3], [4, 3, 3], [3, 3, 6], [3, 6, 7]
    expected = [5, 5, 5, 4, 6, 7]

    window = SlidingWindowMax[int](3)

    result = []
    for value in data:
        window.push(value)
        if window.is_full():
            result.append(window.get_max())

    assert result == expected


@pytest.mark.parametrize("window_type", [SlidingWindowMin, SlidingWindowMax])
def test_window_size_validation(window_type: type[SlidingWindowMin[int] | SlidingWindowMax[int]]) -> None:
    with pytest.raises(ValueError, match="window_size"):
        window_type(0)


@pytest.mark.parametrize(
    ("factory", "values", "window_size", "expected"),
    [
        (sliding_window_minimums, [2, 2, 2, 1], 2, [2, 2, 1]),
        (sliding_window_maximums, [2, 2, 2, 1], 2, [2, 2, 2]),
        (sliding_window_minimums, [9, 7, 8], 1, [9, 7, 8]),
        (sliding_window_maximums, [9, 7, 8], 1, [9, 7, 8]),
    ],
)
def test_batch_helpers(factory, values, window_size, expected) -> None:
    assert list(factory(values, window_size)) == expected


def test_extend_returns_full_window_results() -> None:
    window = SlidingWindowMin[int](3)

    assert window.extend([5, 1, 4, 0]) == [1, 0]
    assert window.current() == 0
    assert len(window) == 3


def test_clear_resets_window_state() -> None:
    window = SlidingWindowMax[int](2)
    window.extend([3, 1, 4])

    window.clear()

    assert len(window) == 0
    assert not window.is_full()
    with pytest.raises(IndexError, match="empty"):
        window.current()


def test_repr_includes_current_value() -> None:
    window = SlidingWindowMin[int](2)
    window.extend([5, 4])

    assert "current=4" in repr(window)
