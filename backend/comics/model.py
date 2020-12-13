from typing import List, Optional
from ..serialization import PropertySerializable
from ..model import StageResult


class ComicStageResult(StageResult):
    def __init__(self, file: str = ""):
        super().__init__("Comic")
        self.file = file

    @property
    def file(self) -> str:
        return self._file

    @file.setter
    def file(self, value: str) -> None:
        self._file = value

    def as_dict(self):
        dic = super().as_dict()
        dic["file"] = self.file
        return dic
