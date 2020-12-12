from abc import ABC, abstractmethod
import sys
import time
from typing import List, Tuple
import ffmpeg
import os
import json
from multiprocessing import Process
from .model import Subtitle, SubtitleStageResult
from ..worker import StageWorker
from ..model import StageResult


class SubtitleGenerator(StageWorker):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_subtitles(self, input_file_path, output_dir) -> SubtitleStageResult:
        pass

    def metafile_path(self) -> str:
        return self.session.subtitle_file

    def work(self) -> StageResult:
        return self.get_subtitles(self.session.video_file, self.session.subtitle_dir)


class DefaultSubtitleGenerator(SubtitleGenerator):
    def __init__(self):
        super().__init__()

    def get_subtitles(self, input_file_path, output_dir) -> SubtitleStageResult:
        return SubtitleStageResult()


if __name__ == "__main__":
    from ..settings import DATA_PATH

    outputPath = os.path.join(DATA_PATH, "test", "subtitles")
    os.makedirs(outputPath, exist_ok=True)

    source = sys.argv[1]

    worker = DefaultSubtitleGenerator()

    result = worker.get_subtitles(source, outputPath)

    print(json.dumps(result.as_dict(), indent=4))
