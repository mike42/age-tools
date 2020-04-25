from dataclasses import dataclass
from typing import List


@dataclass
class PalCol:
    r: int
    g: int
    b: int


@dataclass
class Palette:
    cols: List[PalCol]


def load(file_name: str):
    lines = open(file_name).read().split("\n")
    col_count = int(lines[2])
    cols = []
    for i in range(0, col_count):
        col_line = lines[i + 3]
        nums = col_line.split(" ")
        cols.append(PalCol(int(nums[0]), int(nums[1]), int(nums[2])))
    return Palette(cols)