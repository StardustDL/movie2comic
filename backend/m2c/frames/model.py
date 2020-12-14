from typing import List, Optional
from ..serialization import PropertySerializable
from ..model import StageResult


class Frame(PropertySerializable):
    def __init__(self, name: str = "", time: float = 0.0):
        self.name = name
        self.time = time

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def time(self) -> float:
        return self._time

    @time.setter
    def time(self, value: float) -> None:
        self._time = value


class FrameStageResult(StageResult):
    def __init__(self):
        super().__init__("Frame")
        self.frames = []

    @property
    def frames(self) -> List[Frame]:
        return self._frames

    @frames.setter
    def frames(self, value: List[Frame]) -> None:
        self._frames = value

    def as_dict(self):
        dic = super().as_dict()
        dic["frames"] = [{"name": fr.name, "time": fr.time}
                         for fr in self.frames]
        return dic
