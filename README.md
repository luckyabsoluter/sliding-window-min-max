# Sliding Window Min/Max

A Python library for computing windowed minimum and maximum values in amortized $O(1)$ time using monotonic queues.

## Installation

Install the package from the project root:

```bash
pip install .
```

Install directly from a GitHub repository URL:

```bash
pip install git+https://github.com/luckyabsoluter/sliding-window-min-max.git
```

Install a specific branch, tag, or commit from GitHub:

```bash
pip install git+https://github.com/luckyabsoluter/sliding-window-min-max.git@main
pip install git+https://github.com/luckyabsoluter/sliding-window-min-max.git@v0.1.0
pip install git+https://github.com/luckyabsoluter/sliding-window-min-max.git@<commit-sha>
```

For development work:

```bash
pip install .[dev]
```

Install development dependencies from GitHub:

```bash
pip install "sliding-window-min-max[dev] @ git+https://github.com/luckyabsoluter/sliding-window-min-max.git@main"
```

## Running Tests

Run the test suite from the project root:

```bash
python -m pytest -q
```

## Usage

Track values while moving a fixed-size window across streaming data or a 1D array.

### Tracking Minimum (Min)

```python
from sliding_window import SlidingWindowMin

data = [4, 3, 5, 4, 3, 3, 6, 7]
window = SlidingWindowMin(3)

for val in data:
    window.push(val)
    if window.is_full():
        print(f"Current Minimum: {window.get_min()}")
```

### Tracking Maximum (Max)

```python
from sliding_window import SlidingWindowMax

data = [4, 3, 5, 4, 3, 3, 6, 7]
window = SlidingWindowMax(3)

for val in data:
    window.push(val)
    if window.is_full():
        print(f"Current Maximum: {window.get_max()}")
```

### Batch helpers

```python
from sliding_window import sliding_window_maximums, sliding_window_minimums

data = [4, 3, 5, 4, 3, 3, 6, 7]

mins = list(sliding_window_minimums(data, 3))
maxs = list(sliding_window_maximums(data, 3))
```

## Features

- Streaming-friendly API for incremental updates
- Batch helper functions for array-style processing
- Generic ordering support for comparable values
- Minimal dependency footprint

## Architecture

1. `MonotonicMinQueue` / `MonotonicMaxQueue`
   Internal monotonic queues that keep the best candidate at the front.
2. `SlidingWindowMin` / `SlidingWindowMax`
   Stateful wrappers for streaming workloads with `push`, `extend`, and `clear`.
3. `sliding_window_minimums` / `sliding_window_maximums`
   Convenience iterators for batch processing.
