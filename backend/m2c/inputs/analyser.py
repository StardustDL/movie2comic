from abc import abstractmethod
from ..subtitles.model import Subtitle
from ..styles.model import StyledFrame
from ..frames.model import Frame
import shutil
import sys
import time
from typing import List, Tuple
import ffmpeg
import os
import json
from ..model import StageResult
from .model import InputStageResult, VideoInfo
from ..worker import StageWorker
from PIL import Image, ImageDraw, ImageFont


class InputAnalyser(StageWorker):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def analysis(self, video_file) -> InputStageResult:
        raise NotImplementedError()

    def metafile_path(self) -> str:
        return self.session.input_file

    def work(self) -> StageResult:
        try:
            result = self.analysis(self.session.video_file)
            return result
        except Exception as ex:
            result = InputStageResult()
            result.log = str(ex)
            return result


class DefaultInputAnalyser(InputAnalyser):
    def __init__(self):
        super().__init__()

    def analysis(self, video_file) -> InputStageResult:
        info = ffmpeg.probe(video_file)
        video = [s for s in info["streams"] if s["codec_type"] == "video"][0]
        formats = info["format"]

        result = InputStageResult()
        result.info = VideoInfo(
            os.path.split(formats["filename"])[1], 
            formats["format_long_name"], 
            float(formats["duration"]))
        result.info.width = float(video["width"])
        result.info.height = float(video["height"])
        result.success = True
        return result
