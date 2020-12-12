from abc import ABC, abstractmethod
import sys
import time
from typing import List, Tuple
import os
import json
from multiprocessing import Process
from .model import StageResult
from .serialization import PropertySerializable
from .serialization.json import Encoder


class StageWorker(Process, ABC):
    def __init__(self):
        super().__init__(daemon=True)
        self.sid: str = ""

    @abstractmethod
    def metafile_path(self) -> str:
        pass

    @abstractmethod
    def work(self) -> StageResult:
        pass

    def run(self):
        if self.sid == "":
            raise NotImplementedError()

        from .session import Session
        self.session = Session(self.sid)

        start = time.time()

        result = self.work()

        end = time.time()

        result.duration = end - start

        with open(self.metafile_path(), "w") as file:
            json.dump(result, file, ensure_ascii=False, cls=Encoder)
