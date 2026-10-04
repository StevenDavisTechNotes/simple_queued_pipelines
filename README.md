# Simple Queued Pipelines

> **Note**: This project was created as part of the [Spark Aggregation Methods](https://github.com/StevenDavisTechNotes/SparkAggregationMethods/blob/master/README.md) project.

Simple components to create thread-backed queued pipelines in Python.

## Installation

Requires Python 3.13 or newer.

```bash
pip install simple-queued-pipelines
```

Or, in a `uv` project:

```bash
uv add simple-queued-pipelines
```

## Concepts

### Sink

This class abstracts a pool of threads consuming a queue.

### Pipe

This class abstracts a pool of threads consuming one queue and publishing to another queue.

### GeneratorSource

This class abstracts a pool of threads each consuming a generator (a function that yields) and publishes the iterated values to a queue.

### Execution Graphs

These are orchestrations connecting sources, pipes, and sinks to run until exhausted.
The function `execute_single_channel_linear_execution_graph_with_four_stages` has a source, 2 pipes, and a sink.

## Quick Start

Each stage takes a tuple of actions, and each action runs in its own thread.
Repeat an action to give a stage more threads.

```python
from simple_queued_pipelines.single_channel.sc_execution_graph import (
    execute_single_channel_linear_execution_graph_with_four_stages,
)


def numbers():
    yield from range(10)


results: list[int] = []

execute_single_channel_linear_execution_graph_with_four_stages(
    actions_0=(numbers,),                 # one source thread
    actions_1=(lambda n: n * 2,) * 4,     # four threads in the first pipe
    actions_2=(lambda n: n + 1,) * 2,     # two threads in the second pipe
    actions_3=(results.append,),          # one sink thread
    report_error=lambda message: print(f"error: {message}"),
)

print(sorted(results))  # [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
```

The call returns once the source is exhausted and every item has reached the sink.
Items can pass through a stage's threads in any order, so sort the results if order matters.

If a stage fails, `report_error` is called with a message, the queues are shut down, and the function raises an `Exception` after all threads have stopped.

Optional arguments:

- `queue_0`, `queue_1`, `queue_2`: your own `queue.Queue` instances, for example with a `maxsize` to bound how far a stage can run ahead.
- `block_thread_timeout`: the timeout, in seconds, for each blocking queue operation and thread join. A thread that times out retries. The default is `0.1`.

## Free-threaded Python

The components run on any Python 3.13 or newer. To get true parallelism for CPU-bound work, you need a free-threaded (GIL-free) build of Python, such as `3.13t`.
On a standard build the GIL lets only one thread run Python code at a time, so the pipelines only overlap work that blocks or waits, such as I/O.

## License

Licensed under the GNU Lesser General Public License v2.1 or later. See [LICENSE](LICENSE).

## Development

This project uses [`uv`](https://docs.astral.sh/uv/) to manage dependencies.

> **Note**: This directory contains a local `.python-version` file specifying `3.13t`. When you run `uv` commands in this folder, `uv` will automatically fetch and use the free-threaded build of Python 3.13.

Create the environment and install the dev tools:

```bash
uv sync
```

Run the tests:

```bash
uv run pytest
```

We use `pre-commit` to run formatting (`isort`, `autopep8`) and linting (`flake8`, `ty`) before each commit.
To install the hooks into your local git repository, run:

```bash
uv run pre-commit install
```
