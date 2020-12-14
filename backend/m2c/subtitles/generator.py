from abc import ABC, abstractmethod
import enum
import sys
import time
from typing import List, Tuple
import ffmpeg
import wave
import subprocess
import contextlib
import os
import json
from pocketsphinx import AudioFile
from multiprocessing import Process
from .model import Subtitle, SubtitleStageResult
from ..worker import StageWorker
from ..model import StageResult

from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import itertools


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

        stream = stream.audio.output(audio_file, format="wav")

        success = True

        out, err = b"", b""
        try:
            out, err = stream.run(capture_stdout=True, capture_stderr=True)
        except Exception as ex:
            success = False
            out += str(ex).encode("utf-8")

        if success:
            result = self.get_subtitles(audio_file, self.session.subtitle_dir)
        else:
            result = SubtitleStageResult()

        result.log += "\n" + \
            f"stdout: {out.decode('utf-8')}\nstderr: {err.decode('utf-8')}"
        return result


class SoundSpliter:
    def __init__(self, audio_file):
        self.audio = AudioSegment.from_mp3(audio_file)

    def _split_on_silence_ranges(self, min_silence_len=1000, silence_thresh=-16, keep_silence=100,
                                 seek_step=1):
        # from the itertools documentation
        def pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            a, b = itertools.tee(iterable)
            next(b, None)
            return zip(a, b)

        if isinstance(keep_silence, bool):
            keep_silence = len(self.audio) if keep_silence else 0

        output_ranges = [
            [start - keep_silence, end + keep_silence]
            for (start, end)
            in detect_nonsilent(self.audio, min_silence_len, silence_thresh, seek_step)
        ]

        for range_i, range_ii in pairwise(output_ranges):
            last_end = range_i[1]
            next_start = range_ii[0]
            if next_start < last_end:
                range_i[1] = (last_end+next_start)//2
                range_ii[0] = range_i[1]

        return [
            (max(start, 0), min(end, len(self.audio)))
            for start, end in output_ranges
        ]

    def get_ranges(self, min_duration=1):  # [(0ms, 10ms)]
        raw = self._split_on_silence_ranges(
            min_silence_len=200, silence_thresh=-45, keep_silence=400)
        min_duration *= 1000  # to millisecconds
        result = []
        i = 0
        while i < len(raw):
            s, t = raw[i]
            j = i+1
            while j < len(raw) and t - s < min_duration:
                _, t = raw[j]
                j += 1
            result.append((s, t))
            i = j
        return result

    # return file name

    def split_ranges(self, ranges, output_dir) -> List[str]:
        result = []
        for i, (s, t) in enumerate(ranges):
            segment = self.audio[s:t]
            name = "chunk{0}.wav".format(i)
            segment.export(os.path.join(output_dir, name), format="wav")
            result.append(name)
        return result


class DefaultSubtitleGenerator(SubtitleGenerator):
    def __init__(self, is_zhcn=False):
        super().__init__()
        self.is_zhcn = is_zhcn

    def get_subtitles(self, input_file_path, output_dir) -> SubtitleStageResult:
        MIN_SEGMENT_DURATION = 5

        splitter = SoundSpliter(input_file_path)

        ranges = splitter.get_ranges(min_duration=MIN_SEGMENT_DURATION)
        names = splitter.split_ranges(ranges, output_dir)

        model_root = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "deepspeech", "models")

        from .deepspeech import DeepSpeech

        result = SubtitleStageResult()

        try:
            ds = DeepSpeech()

            if self.is_zhcn:
                ds.load_model(os.path.join(
                    model_root, "deepspeech-0.9.3-models-zh-CN.pbmm"),
                    os.path.join(model_root, "deepspeech-0.9.3-models-zh-CN.scorer"))
            else:
                ds.load_model(os.path.join(
                    model_root, "deepspeech-0.9.3-models.pbmm"),
                    os.path.join(model_root, "deepspeech-0.9.3-models.scorer"))

            for i, (s, t) in enumerate(ranges):
                name = names[i]
                text = ds.process_text(os.path.join(output_dir, name))
                text = text.strip()
                if text != "":  # remove empty subtitle
                    result.subtitles.append(
                        Subtitle(name, text, s / 1000, t / 1000))
        except Exception as ex:
            result.log = str(ex)

        result.success = True

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

            phrases.append(Subtitle("", str(phrase), start /
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
