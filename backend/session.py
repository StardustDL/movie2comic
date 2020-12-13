from .comics.model import ComicStageResult
from .comics.combiner import ComicCombiner
from .styles.model import StyleStageResult
from .styles.transfer import StyleTransfer
from .subtitles.model import SubtitleStageResult
from .subtitles.generator import SubtitleGenerator
from .frames.extractor import FrameExtractor
from .frames.model import FrameStageResult
import os
from typing import Callable, Optional
import uuid
import shutil
import json
from enum import IntEnum
from . import settings
from .serialization.json import Decoder

_ALLOWED_EXTENSIONS = ["mp4", "mpeg", "mpg", "wmv", "mov", "avi", "flv"]


def _is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in _ALLOWED_EXTENSIONS


class SessionStage(IntEnum):
    Create = 0,
    Input = 1,
    Frame = 2,
    Subtitle = 3,
    Style = 4,
    Output = 5


class SessionState(IntEnum):
    AfterCreate = 0,
    AfterInitialize = 1,
    OnInput = 2,
    AfterInput = 3,
    OnFrame = 4,
    AfterFrame = 5,
    OnSubtitle = 6,
    AfterSubtitle = 7,
    OnStyle = 8,
    AfterStyle = 9,
    OnOutput = 10,
    AfterOutput = 11


def _load_result(path):
    with open(path, "r") as file:
        return json.load(file, cls=Decoder)


class Session:
    def __init__(self, sid=None, data_root=None):
        if sid is None:
            sid = str(uuid.uuid1())
        if data_root is None:
            data_root = settings.DATA_PATH
        self.id = sid
        self.data_dir = os.path.join(data_root, self.id)
        self.input_dir = os.path.join(self.data_dir, "input")
        self.video_file = os.path.join(self.input_dir, "input.dat")
        self.frame_dir = os.path.join(self.data_dir, "frames")
        self.frame_file = os.path.join(self.frame_dir, "info.json")
        self.subtitle_dir = os.path.join(self.data_dir, "subtitles")
        self.subtitle_file = os.path.join(self.subtitle_dir, "info.json")
        self.style_dir = os.path.join(self.data_dir, "styles")
        self.style_file = os.path.join(self.style_dir, "info.json")
        self.output_dir = os.path.join(self.data_dir, "output")
        self.output_file = os.path.join(self.output_dir, "output.png")

    def state(self) -> SessionState:
        if not os.path.exists(self.data_dir):
            return SessionState.AfterCreate
        if not os.path.exists(self.input_dir):
            return SessionState.AfterInitialize
        if not os.path.exists(self.video_file):
            return SessionState.OnInput
        if not os.path.exists(self.frame_dir):
            return SessionState.AfterInput
        if not os.path.exists(self.frame_file):
            return SessionState.OnFrame
        if not os.path.exists(self.subtitle_dir):
            return SessionState.AfterFrame
        if not os.path.exists(self.subtitle_file):
            return SessionState.OnSubtitle
        if not os.path.exists(self.style_dir):
            return SessionState.AfterSubtitle
        if not os.path.exists(self.style_file):
            return SessionState.OnStyle
        if not os.path.exists(self.output_dir):
            return SessionState.AfterStyle
        if not os.path.exists(self.output_file):
            return SessionState.OnOutput
        return SessionState.AfterOutput

    def stage(self) -> SessionStage:
        state = self.state()
        return SessionStage(state.value // 2)

    def initialize(self):
        os.mkdir(self.data_dir)

    def input_video(self, request_file) -> bool:
        if _is_allowed_file(request_file.filename):
            os.mkdir(self.input_dir)
            tmp = self.video_file + ".tmp"
            request_file.save(tmp)
            shutil.move(tmp, self.video_file)
            return True
        return False

    def video_path(self) -> Optional[str]:
        if self.state() >= SessionState.AfterInput:
            path = self.video_file
            if os.path.exists(path):
                return path
        return None

    # region frame

    def work_frames(self, worker: FrameExtractor = None) -> bool:
        if self.state() != SessionState.OnFrame - 1:
            return False

        if worker is None:
            from .frames.extractor import DefaultFrameExtractor
            worker = DefaultFrameExtractor()

        os.mkdir(self.frame_dir)

        worker.sid = self.id
        worker.start()

        return True

    def result_frames(self) -> Optional[FrameStageResult]:
        if self.state() >= SessionState.AfterFrame:
            return _load_result(self.frame_file)
        return None

    def frame_image_path(self, name) -> Optional[str]:
        if self.state() >= SessionState.AfterFrame:
            path = os.path.join(self.frame_dir, name)
            if os.path.exists(path):
                return path
        return None

    # endregion

    # region subtitle

    def work_subtitles(self, worker: SubtitleGenerator = None) -> bool:
        if self.state() != SessionState.OnSubtitle - 1:
            return False

        if worker is None:
            from .subtitles.generator import DefaultSubtitleGenerator
            worker = DefaultSubtitleGenerator()

        os.mkdir(self.subtitle_dir)

        worker.sid = self.id
        worker.start()

        return True

    def result_subtitles(self) -> Optional[SubtitleStageResult]:
        if self.state() >= SessionState.AfterSubtitle:
            return _load_result(self.subtitle_file)
        return None

    def subtitle_audio_path(self, name) -> Optional[str]:
        if self.state() >= SessionState.AfterSubtitle:
            path = os.path.join(self.subtitle_dir, name)
            if os.path.exists(path):
                return path
        return None

    # endregion

    # region style

    def work_styles(self, worker: StyleTransfer = None) -> bool:
        if self.state() != SessionState.OnStyle - 1:
            return False

        if worker is None:
            from .styles.transfer import WhiteBoxCartoonizationStyleTransfer
            worker = WhiteBoxCartoonizationStyleTransfer()

        os.mkdir(self.style_dir)

        worker.sid = self.id
        worker.start()

        return True

    def result_styles(self) -> Optional[StyleStageResult]:
        if self.state() >= SessionState.AfterStyle:
            return _load_result(self.style_file)
        return None

    def styled_image_path(self, name) -> Optional[str]:
        if self.state() >= SessionState.AfterStyle:
            path = os.path.join(self.style_dir, name)
            if os.path.exists(path):
                return path
        return None

    # endregion

    # region comic

    def work_comics(self, worker: ComicCombiner = None) -> bool:
        if self.state() != SessionState.OnOutput - 1:
            return False

        if worker is None:
            from .comics.combiner import DefaultComicCombiner
            worker = DefaultComicCombiner()

        os.mkdir(self.output_dir)

        worker.sid = self.id
        worker.start()

        return True

    def result_comics(self) -> Optional[ComicStageResult]:
        if self.state() >= SessionState.AfterOutput:
            return _load_result(self.output_file)
        return None

    def comic_file_path(self, file) -> Optional[str]:
        if self.state() >= SessionState.AfterOutput:
            path = os.path.join(self.output_dir, file)
            if os.path.exists(path):
                return path
        return None

    # endregion

    def clear(self):
        shutil.rmtree(self.data_dir)
