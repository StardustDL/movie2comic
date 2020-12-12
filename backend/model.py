from .serialization import PropertySerializable


class StageResult(PropertySerializable):
    def __init__(self, name: str = "", success: bool = False, duration: float = 0, log: str = ""):
        self.name = name
        self.duration = duration
        self.log = log
        self.success = success

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def success(self) -> bool:
        return self._success

    @success.setter
    def success(self, value: bool) -> None:
        self._success = value

    @property
    def duration(self) -> float:
        return self._duration

    @duration.setter
    def duration(self, value: float) -> None:
        self._duration = value

    @property
    def log(self) -> str:
        return self._log

    @log.setter
    def log(self, value: str) -> None:
        self._log = value

    def as_dict(self):
        return {
            "name": self.name,
            "success": self.success,
            "duration": self.duration,
            "log": self.log,
        }
