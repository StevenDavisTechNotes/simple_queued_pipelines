# cSpell: ignore partitioner, conflater
import queue
from typing import List

import pytest

from simple_queued_pipelines.thread_safe_collections.partitioned_queue import (
    PartitionedQueue,
)


@pytest.fixture
def partitioned_queue():
    max_size = 10

    def partitioner(value: int) -> int:
        return value % 2

    def conflater(values: List[int]) -> int:
        return sum(values)

    return PartitionedQueue(max_size, partitioner, conflater)


def test_put_and_get(partitioned_queue):
    partitioned_queue.put(1, timeout=1)
    partitioned_queue.put(2, timeout=1)
    partitioned_queue.put(3, timeout=1)

    result = partitioned_queue.get(timeout=1)
    assert result == 4  # 1 + 3

    result = partitioned_queue.get(timeout=1)
    assert result == 2  # 2

    with pytest.raises(queue.Empty):
        partitioned_queue.get(timeout=1)


def test_put_timeout(partitioned_queue):
    for i in range(partitioned_queue.max_size):
        partitioned_queue.put(i, timeout=1)

    with pytest.raises(queue.Full):
        partitioned_queue.put(partitioned_queue.max_size, timeout=1)


def test_get_timeout(partitioned_queue):
    with pytest.raises(queue.Empty):
        partitioned_queue.get(timeout=1)


def test_put_and_get_with_timeout(partitioned_queue):
    partitioned_queue.put(1, timeout=1)
    partitioned_queue.put(2, timeout=1)

    result = partitioned_queue.get(timeout=1)
    assert result == 1

    result = partitioned_queue.get(timeout=1)
    assert result == 2

    with pytest.raises(queue.Empty):
        partitioned_queue.get(timeout=1)
