import logging
import queue as queue_mod
from typing import Callable, Generator, TypeVar

from simple_queued_pipelines.single_channel.sc_pipe import SingleChannelPipe
from simple_queued_pipelines.single_channel.sc_sink import SingleChannelSink
from simple_queued_pipelines.source import GeneratorSource

logger = logging.getLogger(__name__)
T0 = TypeVar('T0')
T1 = TypeVar('T1')
T2 = TypeVar('T2')


def execute_single_channel_linear_execution_graph_with_four_stages(
        *,
        actions_0: tuple[Callable[[], Generator[T0, None, None]], ...],
        actions_1: tuple[Callable[[T0], T1], ...],
        actions_2: tuple[Callable[[T1], T2], ...],
        actions_3: tuple[Callable[[T2], None], ...],
        block_thread_timeout: float = 0.1,
        queue_0: queue_mod.Queue[T0] | None = None,
        queue_1: queue_mod.Queue[T1] | None = None,
        queue_2: queue_mod.Queue[T2] | None = None,
        report_error: Callable[[str], None],
) -> None:
    was_aborted: bool = False
    queue_0 = queue_0 or queue_mod.Queue()
    queue_1 = queue_1 or queue_mod.Queue()
    queue_2 = queue_2 or queue_mod.Queue()

    def stop(
            immediate: bool,
    ):
        queue_0.shutdown(immediate=immediate)
        queue_1.shutdown(immediate=immediate)
        queue_2.shutdown(immediate=immediate)

    def wrapped_report_error(error: str) -> None:
        nonlocal was_aborted
        was_aborted = True
        report_error(error)
        stop(immediate=True)

    with \
            GeneratorSource[T0](
                actions=actions_0,
                block_thread_timeout=block_thread_timeout,
                name="Source",
                queue_out=queue_0,
                report_error=wrapped_report_error,
            ) as source, \
            SingleChannelPipe[T0, T1](
                actions=actions_1,
                block_thread_timeout=block_thread_timeout,
                name="Pipe-1",
                queue_in=queue_0,
                queue_out=queue_1,
                report_error=wrapped_report_error,
            ) as pipe_1, \
            SingleChannelPipe[T1, T2](
                actions=actions_2,
                block_thread_timeout=block_thread_timeout,
                name="Pipe-2",
                queue_in=queue_1,
                queue_out=queue_2,
                report_error=wrapped_report_error,
            ) as pipe_2, \
            SingleChannelSink[T2](
                actions=actions_3,
                block_thread_timeout=block_thread_timeout,
                name="Sink",
                queue_in=queue_2,
                report_error=wrapped_report_error,
            ) as sink:
        source.wait_for_completion()
        pipe_1.wait_for_completion()
        pipe_2.wait_for_completion()
        sink.wait_for_completion()
    keyboard_interrupted = (
        source.keyboard_interrupted
        or pipe_1.keyboard_interrupted
        or pipe_2.keyboard_interrupted
        or sink.keyboard_interrupted
    )
    if keyboard_interrupted:
        raise KeyboardInterrupt()
    exceptions = (
        source.execution_exceptions
        + pipe_1.execution_exceptions
        + pipe_2.execution_exceptions
        + sink.execution_exceptions
    )
    if was_aborted:
        exceptions.append(Exception("Execution was aborted"))
    if len(exceptions) > 0:
        msgs = "\n".join([str(e) for e in exceptions])
        raise Exception(f"Exceptions occurred: {msgs}")
