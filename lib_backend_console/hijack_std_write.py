import functools
import sys
from typing import Callable, AnyStr
from asyncio import Queue

from lib_backend_console.globals import BackendConsoleGlobals
from lib_backend_console.one_time_callable import one_time_callable


def on_print(message: str, event: Queue, is_error: bool) -> None:
    message = message.replace('\r', '\n').replace('\n\n', '\n')

    console_content = dict(message=message, is_error=is_error)
    BackendConsoleGlobals.console_content.append(console_content)
    event.put_nowait(console_content)


def hijack_stdout_write(message: AnyStr, original_write: Callable[[AnyStr], int], queue: Queue, is_error: bool = False) -> int:
    code = original_write(message)
    on_print(str(message), queue, is_error)
    return code


@one_time_callable
def apply_hijack():
    sys.stdout.write = functools.partial(hijack_stdout_write, original_write=sys.stdout.write, queue=BackendConsoleGlobals.queue)
    sys.stderr.write = functools.partial(hijack_stdout_write, original_write=sys.stderr.write, queue=BackendConsoleGlobals.queue, is_error=True)
