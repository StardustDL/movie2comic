from abc import ABC, abstractmethod
import sys
import time
from typing import List, Tuple
import ffmpeg
import wave
import contextlib
import os
import json
from pocketsphinx import AudioFile
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
        stream = ffmpeg.input(self.session.video_file)
        audio_file = os.path.join(self.session.subtitle_dir, "audio.wav")

        success = True

        out, err = b"", b""
        try:
            out, err = stream.run(capture_stdout=True, capture_stderr=True)
        except:
            success = False

        if success:
            result = self.get_subtitles(audio_file, self.session.subtitle_dir)
        else:
            result = SubtitleStageResult()

        result.log += "\n" + \
            f"stdout: {out.decode('utf-8')}\nstderr: {err.decode('utf-8')}"
        return result


class DefaultSubtitleGenerator(SubtitleGenerator):
    def __init__(self):
        super().__init__()

    def get_subtitles(self, input_file_path, output_dir) -> SubtitleStageResult:
        result = SubtitleStageResult()
        return result


class PocketSphinxSubtitleGenerator(SubtitleGenerator):
    def __init__(self):
        super().__init__()

    def get_subtitles(self, input_file_path, output_dir) -> SubtitleStageResult:
        phrases = []
        log = ""

        with contextlib.closing(wave.open(input_file_path, 'r')) as f:
            rate = f.getframerate()
            frames = f.getnframes()
            duration = frames / float(rate)
            log += f"rate: {rate}, frames: {frames}, duration: {duration}"

        for phrase in AudioFile(audio_file=input_file_path):
            start = sys.maxsize
            end = 0
            for seg in phrase.seg():
                start = min(start, seg.start_frame)
                end = max(end, seg.end_frame)

            log += f"{phrase}: {start}~{end}\n"

            phrases.append(Subtitle(str(phrase), start /
                                    float(rate), end / float(rate)))

        result = SubtitleStageResult()
        result.success = True
        result.log = log
        result.subtitles = phrases
        return result


if __name__ == "__main__":
    from ..settings import DATA_PATH

    outputPath = os.path.join(DATA_PATH, "test", "subtitles")
    os.makedirs(outputPath, exist_ok=True)

    source = sys.argv[1]

    worker = DefaultSubtitleGenerator()

    result = worker.get_subtitles(source, outputPath)

    print(json.dumps(result.as_dict(), indent=4))
