from abc import abstractmethod
import sys
import time
from typing import List, Tuple
import ffmpeg
import os
import json
from ..model import StageResult
from .model import StyledFrame, StyleStageResult
from ..worker import StageWorker
import shutil


class StyleTransfer(StageWorker):
    def __init__(self):
        super().__init__()

    @abstractmethod
    # [(name, path)] for input
    def transfer_frames(self, input_file_path_list: List[Tuple[str, str]], output_dir) -> StyleStageResult:
        raise NotImplementedError()

    def metafile_path(self) -> str:
        return self.session.style_file

    def work(self) -> StageResult:
        ls = []
        frames = self.session.result_frames()
        for f in frames.frames:
            ls.append((f.name, self.session.frame_image_path(f.name)))

        return self.transfer_frames(ls, self.session.style_dir)


class DefaultStyleTransfer(StyleTransfer):
    def __init__(self):
        super().__init__()

    def transfer_frames(self, input_file_path_list, output_dir) -> StyleStageResult:
        result = StyleStageResult()

        for name, path in input_file_path_list:
            shutil.copy(path, os.path.join(output_dir, name))
            result.frames.append(StyledFrame(name))

        return result


if __name__ == "__main__":
    from ..settings import DATA_PATH

    outputPath = os.path.join(DATA_PATH, "test", "frames")
    os.makedirs(outputPath, exist_ok=True)

    source = sys.argv[1]

    worker = DefaultStyleTransfer()

    result = worker.transfer_frames([], outputPath)

    print(json.dumps(result.as_dict(), indent=4))
