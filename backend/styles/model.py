from typing import List, Optional
from ..serialization import PropertySerializable
from ..model import StageResult


class StyledFrame(PropertySerializable):
    def __init__(self, name: str = ""):
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value


class StyleStageResult(StageResult):
    def __init__(self):
        super().__init__("Style")
        self.frames = []

    @property
    def frames(self) -> List[StyledFrame]:
        return self._frames

    @frames.setter
    def frames(self, value: List[StyledFrame]) -> None:
        self._frames = value

    def as_dict(self):
        dic = super().as_dict()
        dic["frames"] = [{"name": fr.name}
                         for fr in self.frames]
        return dic
