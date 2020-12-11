from typing import List, Optional
from ..serialization import PropertySerializable


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


class FrameExtractorResult(PropertySerializable):
    def __init__(self, success: bool = False, frames: Optional[List[Frame]] = None, stdout="", stderr=""):
        self.success = success
        if frames:
            self.frames = frames
        else:
            self.frames = []
        self.stdout = stdout
        self.stderr = stderr

    @property
    def success(self) -> bool:
        return self._success

    @success.setter
    def success(self, value: bool) -> None:
        self._success = value

    @property
    def frames(self) -> List[Frame]:
        return self._frames

    @frames.setter
    def frames(self, value: List[Frame]) -> None:
        self._frames = value

    @property
    def stdout(self) -> str:
        return self._stdout

    @stdout.setter
    def stdout(self, value: str) -> None:
        self._stdout = value

    @property
    def stderr(self) -> str:
        return self._stderr

    @stderr.setter
    def stderr(self, value: str) -> None:
        self._stderr = value
