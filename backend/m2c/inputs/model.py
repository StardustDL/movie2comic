from typing import List, Optional
from ..serialization import PropertySerializable
from ..model import StageResult


class VideoInfo(PropertySerializable):
    def __init__(self, name="", format="", duration=0.0):
        self.name = name
        self.duration = duration
        self.format = format
        self.width = 0
        self.height = 0

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def format(self) -> str:
        return self._format

    @format.setter
    def format(self, value: str) -> None:
        self._format = value

    @property
    def duration(self) -> float:
        return self._duration

    @duration.setter
    def duration(self, value: float) -> None:
        self._duration = value

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value


class InputStageResult(StageResult):
    def __init__(self):
        super().__init__("Input")
        self.info = VideoInfo()

    @property
    def info(self) -> VideoInfo:
        return self._info

    @info.setter
    def info(self, value: VideoInfo) -> None:
        self._info = value

    def as_dict(self):
        dic = super().as_dict()
        dic["info"] = {
            "name": self.info.name,
            "format": self.info.format,
            "duration": self.info.duration,
            "width": self.info.width,
            "height": self.info.height
        }
        return dic
