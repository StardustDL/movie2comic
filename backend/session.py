import os
from typing import Optional
import uuid
import shutil
import json
from enum import IntEnum
from . import settings
from .frames import FrameExtractorResult
from .serialization.json import Decoder

_ALLOWED_EXTENSIONS = ["mp4", "mpeg", "mpg", "wmv", "mov", "avi"]


def _is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in _ALLOWED_EXTENSIONS


class SessionStage(IntEnum):
    Created = 0
    Initialized = 1
    Inputted = 2
    KeyframeExtracting = 3
    KeyframeExtracted = 4
    SubtitleGenerating = 5
    SubtitleGenerated = 6
    StyleTranferring = 7
    StyleTranferred = 8
    Finished = 9


class Session:
    def __init__(self, sid=None, data_root=None):
        if sid is None:
            sid = str(uuid.uuid1())
        if data_root is None:
            data_root = settings.DATA_PATH
        self.id = sid
        self.data_dir = os.path.join(data_root, self.id)
        self.input_file = os.path.join(self.data_dir, "input.dat")
        self.keyframe_dir = os.path.join(self.data_dir, "keyframes")
        self.keyframe_file = os.path.join(self.keyframe_dir, "info.json")
        self.subtitle_dir = os.path.join(self.data_dir, "subtitles")
        self.subtitle_file = os.path.join(self.subtitle_dir, "info.json")
        self.styletransfer_dir = os.path.join(self.data_dir, "styletransfer")
        self.styletransfer_file = os.path.join(
            self.styletransfer_dir, "info.json")
        self.output_file = os.path.join(self.data_dir, "output.png")

    def stage(self) -> SessionStage:
        if not os.path.exists(self.data_dir):
            return SessionStage.Created
        if not os.path.exists(self.input_file):
            return SessionStage.Initialized
        if not os.path.exists(self.keyframe_dir):
            return SessionStage.Inputted
        if not os.path.exists(self.keyframe_file):
            return SessionStage.KeyframeExtracting
        if not os.path.exists(self.subtitle_dir):
            return SessionStage.KeyframeExtracted
        if not os.path.exists(self.subtitle_file):
            return SessionStage.SubtitleGenerating
        if not os.path.exists(self.styletransfer_dir):
            return SessionStage.SubtitleGenerated
        if not os.path.exists(self.styletransfer_file):
            return SessionStage.StyleTranferring
        if not os.path.exists(self.output_file):
            return SessionStage.StyleTranferred
        return SessionStage.Finished

    def initialize(self):
        os.mkdir(self.data_dir)

    def prepare_keyframe_extract(self):
        os.mkdir(self.keyframe_dir)

    def prepare_subtitle_generate(self):
        os.mkdir(self.subtitle_dir)

    def prepare_style_transfer(self):
        os.mkdir(self.styletransfer_dir)

    def input(self, request_file) -> bool:
        if _is_allowed_file(request_file.filename):
            request_file.save(self.input_file)
            return True
        return False

    def work_keyframes(self) -> bool:
        if self.stage() != SessionStage.Inputted:
            return False
        from .frames.extractor import KeyframeExtractor

        self.prepare_keyframe_extract()
        worker = KeyframeExtractor(self.id)
        worker.start()

        return True

    def keyframes(self) -> Optional[FrameExtractorResult]:
        if self.stage() >= SessionStage.KeyframeExtracted:
            with open(self.keyframe_file, "r") as file:
                return json.load(file, cls=Decoder)
        return None

    def keyframe_path(self, name) -> Optional[str]:
        if self.stage() >= SessionStage.KeyframeExtracted:
            path = os.path.join(self.keyframe_dir, name)
            if os.path.exists(path):
                return path
        return None

    def clear(self):
        shutil.rmtree(self.data_dir)
