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
        return self.get_subtitles(self.session.video_file, self.session.subtitle_dir)


class DefaultSubtitleGenerator(SubtitleGenerator):
    def __init__(self):
        super().__init__()

    def get_subtitles(self, input_file_path, output_dir) -> SubtitleStageResult:
        stream = ffmpeg.input(input_file_path)
        audio_file = os.path.join(output_dir, "audio.wav")

        # info = ffmpeg.probe(input_file_path, v="quiet", select_streams="v")
        # fps_str = info["streams"][0]["r_frame_rate"]

        fps = 100

        stream = stream.audio.output(audio_file, format="wav")

        success = True

        out, err = b"", b""
        try:
            out, err = stream.run(capture_stdout=True, capture_stderr=True)
        except:
            success = False

        phrases = []
        log = ""

        if success:
            with contextlib.closing(wave.open(audio_file, 'r')) as f:
                rate = f.getframerate()
                frames = f.getnframes()
                duration = frames / float(rate)
                log += f"rate: {rate}, frames: {frames}, duration: {duration}"
            
            for phrase in AudioFile(audio_file=audio_file):
                start = sys.maxsize
                end = 0
                for seg in phrase.seg():
                    start = min(start, seg.start_frame)
                    end = max(end, seg.end_frame)

                log += f"{phrase}: {start}~{end}\n"

                phrases.append(Subtitle(str(phrase), start /
                                        float(rate), end / float(rate)))

        result = SubtitleStageResult()
        result.success = success
        result.log = log + "\n" + f"stdout: {out}\nstderr: {err}"
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
