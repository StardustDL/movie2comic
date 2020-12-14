from typing import List, Optional
from ..serialization import PropertySerializable
from ..model import StageResult


class Subtitle(PropertySerializable):
    def __init__(self, name: str = "", text: str = "", start: float = 0.0, end: float = 0.0):
        self.name = name
        self.text = text
        self.start = start
        self.end = end

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    @property
    def start(self) -> float:
        return self._start

    @start.setter
    def start(self, value: float) -> None:
        self._start = value

    @property
    def end(self) -> float:
        return self._end

    @end.setter
    def end(self, value: float) -> None:
        self._end = value


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
        dic["subtitles"] = [{"name": fr.name, "text": fr.text, "start": fr.start, "end": fr.end}
                            for fr in self.subtitles]
        return dic
