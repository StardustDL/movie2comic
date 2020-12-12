from typing import List, Optional
from ..serialization import PropertySerializable
from ..model import StageResult


class Subtitle(PropertySerializable):
    def __init__(self, text: str = "", time: float = 0.0):
        self.text = text
        self.time = time

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    @property
    def time(self) -> float:
        return self._time

    @time.setter
    def time(self, value: float) -> None:
        self._time = value


class SubtitleStageResult(StageResult):
    def __init__(self):
        super().__init__("Subtitle")
        self.subtitles = []

    @property
    def subtitles(self) -> List[Subtitle]:
        return self._subtitles

    @subtitles.setter
    def subtitles(self, value: List[Subtitle]) -> None:
        self._subtitles = value

    def as_dict(self):
        dic = super().as_dict()
        dic["subtitles"] = [{"text": fr.text, "time": fr.time}
                            for fr in self.subtitles]
        return dic