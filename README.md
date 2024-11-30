# Simple Queued Pipelines
Simple package to create thread-backed queued pipelines in Python

## Concepts

### Sink

This class abstracts a pool of threads consuming a queue.

### Pipe

This class abstracts a pool of threads consuming one queue and publishing to another queue.

### GeneratingSource

This class abstracts a pool of threads each consuming a generator (a function that yields) and publishes the iterated values to a queue.

### Execution Graphs

These acyclic connected directed graphs of sources, pipes, and sinks which run until exhausted.

## Example

Checkout the function `simple_queued_pipelines\single_channel\sc_execution_graph_test.py` which exercises these concepts.  

