# Simple Queued Pipelines

> **Note**: This project was created as part of the [Spark Aggregation Methods](https://github.com/StevenDavisTechNotes/SparkAggregationMethods/blob/master/README.md) project.

Simple package to create thread-backed queued pipelines in Python

## Concepts

### Sink

This class abstracts a pool of threads consuming a queue.

### Pipe

This class abstracts a pool of threads consuming one queue and publishing to another queue.

### GeneratingSource

This class abstracts a pool of threads each consuming a generator (a function that yields) and publishes the iterated values to a queue.

### Execution Graphs

These are orchestrations connecting sources, pipes, and sinks to run until exhausted.
The function `execute_single_channel_linear_execution_graph_with_four_stages` has a source, 2 pipes, and a sink.  

## 🛠 Getting Started

We use `uv` for blazing-fast, unified Python dependency management.

### 1. Environment Setup

> **Note**: This directory contains a local `.python-version` file specifying `3.13t`. When you run `uv` commands in this folder, `uv` will automatically fetch and use the **free-threaded** (GIL-free) build of Python 3.13 to enable true multi-threading.

Initialize the environment and install dependencies:
```bash
uv sync
```

### 2. Code Standards (`pre-commit`)
We use `pre-commit` to automatically run formatting (`isort`, `autopep8`) and linting (`flake8`, `ty`) before you commit code.
To install the pre-commit hooks into your local git repository, run:
```bash
uv run pre-commit install
```

### 3. Handy Commands

To run the test suite:
```bash
(
        (cd common_python && uv run pytest spark_agg_methods_common_python && cd ..) -and
        (cd py_spark && uv run pytest src && cd ..) -and
        (cd python_dask && uv run pytest src && cd ..) -and
        (cd python_single_threaded && uv run pytest src && cd ..) -and
        (cd python_free_threaded && uv run pytest src && cd ..) -and
        (cd simple_queued_pipelines && uv run pytest simple_queued_pipelines && cd ..) -and
        (Write-Host "Success! All tests passed!")
    )
    (cd scala_spark && sbt test && cd ..) &&
```

To manually trigger formatting and static analysis:
```bash
uv run isort admin common_python py_spark python_dask python_single_threaded python_free_threaded simple_queued_pipelines
uv run autopep8 --in-place --recursive uv run pytest admin common_python py_spark python_dask python_single_threaded python_free_threaded simple_queued_pipelines
uv run flake8 uv run pytest admin common_python py_spark python_dask python_single_threaded python_free_threaded simple_queued_pipelines
uv run python -m ty check
```
