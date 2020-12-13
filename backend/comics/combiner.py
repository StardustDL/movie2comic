from abc import abstractmethod
import shutil
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
    def combine(self, frames, subtitles, styledFrames, output_dir) -> ComicStageResult:
        raise NotImplementedError()

    def metafile_path(self) -> str:
        return self.session.output_file

    def work(self) -> StageResult:
        return self.combine(self.session.result_frames().frames, self.session.result_subtitles().subtitles, self.session.result_styles().frames, self.session.output_dir)


class DefaultComicCombiner(ComicCombiner):
    def __init__(self):
        super().__init__()

    def combine(self, frames, subtitles, styledFrames, output_dir) -> ComicStageResult:
        OUTPUT_NAME = "output.jpg"

        path = self.session.styled_image_path(styledFrames[0].name)
        if path:
            shutil.copy(path, os.path.join(output_dir, OUTPUT_NAME))

        res = ComicStageResult()
        res.success = True
        res.file = OUTPUT_NAME
        return res
