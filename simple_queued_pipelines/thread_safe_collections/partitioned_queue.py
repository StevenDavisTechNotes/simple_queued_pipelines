# cSpell: ignore Partitioner, Conflater
import queue
import time
from threading import Lock
from typing import Dict, Generic, Hashable, List, Protocol, TypeVar

TQueuedValue = TypeVar('TQueuedValue', bound=object, contravariant=False)
TPartitionKey = TypeVar('TPartitionKey', bound=Hashable, covariant=True)


class TPartitioner(Protocol[TQueuedValue, TPartitionKey]):  # pyright: ignore[reportInvalidTypeVarUse]
    def __call__(self, value: TQueuedValue) -> TPartitionKey:
        ...


class TConflater(Protocol[TQueuedValue]):
    def __call__(self, values: List[TQueuedValue]) -> TQueuedValue:
        ...


class PartitionedQueue(Generic[TQueuedValue, TPartitionKey]):
    max_size: int
    _partitioner: TPartitioner[TQueuedValue, TPartitionKey]
    _conflater: TConflater[TQueuedValue]
    is_shutdown: bool
    _queue_depth: int
    _keys: List[TPartitionKey]
    _values: Dict[TPartitionKey, List[TQueuedValue]]
    _mutex: Lock

    def __init__(
            self,
            max_size: int,
            partitioner: TPartitioner[TQueuedValue, TPartitionKey],
            conflater: TConflater[TQueuedValue],
    ):
        self.max_size = max_size
        self._partitioner = partitioner
        self._conflater = conflater
        self.is_shutdown = False
        self._queue_depth = 0
        self._keys: List[TPartitionKey] = []
        self._values: Dict[TPartitionKey, List[TQueuedValue]] = {}
        self._mutex = Lock()

    def put(self, value: TQueuedValue, timeout: float):
        start_time = time.time()
        key = self._partitioner(value)

        while True:
            elapsed_time = time.time() - start_time
            remaining_time = timeout - elapsed_time

            if self.is_shutdown:
                raise queue.ShutDown()

            if remaining_time <= 0:
                raise TimeoutError()

            acquired = self._mutex.acquire(timeout=remaining_time)
            if not acquired:
                raise TimeoutError()

            try:
                if self.is_shutdown:
                    raise queue.ShutDown()

                if self._queue_depth >= self.max_size:
                    raise queue.Full()

                if key in self._values:
                    self._values[key].append(value)
                else:
                    self._values[key] = [value]
                    self._keys.append(key)

                self._queue_depth += 1
                break
            finally:
                self._mutex.release()

    def get(self, timeout: float):
        start_time = time.time()

        while True:
            elapsed_time = time.time() - start_time
            remaining_time = timeout - elapsed_time

            if self.is_shutdown:
                raise queue.ShutDown()

            if remaining_time <= 0:
                raise TimeoutError()

            acquired = self._mutex.acquire(timeout=remaining_time)
            if not acquired:
                raise TimeoutError()

            try:
                if self.is_shutdown:
                    raise queue.ShutDown()

                if self._queue_depth == 0:
                    raise queue.Empty()

                key = self._keys.pop(0)
                values = self._values.pop(key)
                conflated_value = self._conflater(values)

                self._queue_depth -= len(values)
                return conflated_value
            finally:
                self._mutex.release()

    def shutdown(
            self,
            immediate: bool,
    ):
        self.is_shutdown = True
        if immediate:
            with self._mutex:
                self._queue_depth = 0
                self._keys.clear()
                self._values.clear()
