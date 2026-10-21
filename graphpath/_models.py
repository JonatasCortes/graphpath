from ._constants import ORIGIN_X, ORIGIN_Y, STEP_SIZE
from dataclasses import dataclass
from datetime import date


@dataclass
class Day:
    when: date
    count: int
    column: int
    row: int

    @property
    def x(self) -> float:
        return ORIGIN_X + self.column * STEP_SIZE

    @property
    def y(self) -> float:
        return ORIGIN_Y + self.row * STEP_SIZE