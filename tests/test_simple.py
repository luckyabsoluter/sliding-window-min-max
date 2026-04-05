from __future__ import annotations

from sliding_window import (
    SimpleSlidingWindowMax,
    SimpleSlidingWindowMin,
    simple_sliding_window_maximums,
    simple_sliding_window_minimums,
)


def test_simple_min_window_tracks_expected_values() -> None:
    data = [4, 3, 5, 4, 3, 3, 6, 7]
    # Windows: [4, 3, 5], [3, 5, 4], [5, 4, 3], [4, 3, 3], [3, 3, 6], [3, 6, 7]
    expected = [3, 3, 3, 3, 3, 3]

    window = SimpleSlidingWindowMin(3)
    result = []

    for value in data:
        window.push(value)
        if window.is_full():
            result.append(window.get_min())

    assert result == expected


def test_simple_batch_helper_returns_expected_values() -> None:
    assert list(simple_sliding_window_minimums([4, 3, 5, 4, 3, 3, 6, 7], 3)) == [3, 3, 3, 3, 3, 3]


def test_simple_max_window_tracks_expected_values() -> None:
    data = [4, 3, 5, 4, 3, 3, 6, 7]
    # Windows: [4, 3, 5], [3, 5, 4], [5, 4, 3], [4, 3, 3], [3, 3, 6], [3, 6, 7]
    expected = [5, 5, 5, 4, 6, 7]

    window = SimpleSlidingWindowMax(3)
    result = []

    for value in data:
        window.push(value)
        if window.is_full():
            result.append(window.get_max())

    assert result == expected


def test_simple_max_batch_helper_returns_expected_values() -> None:
    assert list(simple_sliding_window_maximums([4, 3, 5, 4, 3, 3, 6, 7], 3)) == [5, 5, 5, 4, 6, 7]


def test_simple_batch_helper_is_lazy() -> None:
    consumed: list[int] = []

    def values():
        for value in [4, 3, 5]:
            consumed.append(value)
            yield value

    minimums = simple_sliding_window_minimums(values(), 2)

    assert consumed == []
    assert next(minimums) == 3
    assert consumed == [4, 3]


def test_simple_max_batch_helper_is_lazy() -> None:
    consumed: list[int] = []

    def values():
        for value in [4, 3, 5]:
            consumed.append(value)
            yield value

    maximums = simple_sliding_window_maximums(values(), 2)

    assert consumed == []
    assert next(maximums) == 4
    assert consumed == [4, 3]


def test_simple_extend_and_current_follow_core_style() -> None:
    window = SimpleSlidingWindowMin(3)

    assert window.extend([5.0, 1, 4, 0.5]) == [1, 0.5]
    assert window.current() == 0.5
    assert len(window) == 3


def test_simple_repr_includes_current_value() -> None:
    window = SimpleSlidingWindowMin(2)
    window.extend([5, 4.5])

    assert "current=4.5" in repr(window)


def test_simple_max_extend_and_current_follow_core_style() -> None:
    window = SimpleSlidingWindowMax(3)

    assert window.extend([1.0, 5, 4, 6.5]) == [5, 6.5]
    assert window.current() == 6.5
    assert len(window) == 3


def test_simple_max_repr_includes_current_value() -> None:
    window = SimpleSlidingWindowMax(2)
    window.extend([5, 4.5])

    assert "current=5" in repr(window)
