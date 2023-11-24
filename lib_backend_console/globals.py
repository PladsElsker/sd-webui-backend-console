from asyncio import Queue
from typing import Sequence, Dict


class BackendConsoleGlobals:
    queue: Queue = Queue()
    console_content: Sequence[Dict] = []
