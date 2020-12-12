from abc import abstractmethod
import sys
import time
from typing import List, Tuple
import ffmpeg
import os
import json
from ..model import StageResult
from .model import ComicStageResult
from ..worker import StageWorker


class ComicCombiner(StageWorker):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def combine(self, session, output_dir) -> ComicStageResult:
        raise NotImplementedError()

    def metafile_path(self) -> str:
        return self.session.frame_file

    def work(self) -> StageResult:
        return self.combine(self.session, self.session.output_dir)


class DefaultComicCombiner(ComicCombiner):
    def __init__(self):
        super().__init__()

    def get_frames(self, session, output_dir) -> ComicStageResult:

        success = True

        res = ComicStageResult()
        res.success = success
        return res
