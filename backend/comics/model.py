from typing import List, Optional
from ..serialization import PropertySerializable
from ..model import StageResult


class ComicStageResult(StageResult):
    def __init__(self):
        super().__init__("Comic")

    def as_dict(self):
        dic = super().as_dict()
        return dic
