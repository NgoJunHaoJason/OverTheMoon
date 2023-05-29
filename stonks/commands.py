from enum import Enum


class Command(Enum):
    CHECK = "/check"
    LIST = "/list"
    WATCH = "/watch"
    UNWATCH = "/unwatch"

    def __eq__(self, __value: object) -> bool:
        return self.value == str(__value)

    def __str__(self) -> str:
        return self.value
