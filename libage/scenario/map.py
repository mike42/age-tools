import logging

from attr import dataclass

from libage.scenario import data


@dataclass()
class ScnMap:
    width: int
    height: int
    tiles: list


@dataclass
class ScnMapTile:
    terrain: int
    elevation: int
    zone: int


def read_map(data: data):
    width = data.uint32()
    height = data.uint32()
    tiles = []
    for i in range(0, height * width):
        tiles.append(ScnMapTile(
            data.uint8(),
            data.uint8(),
            data.uint8()
        ))
    return ScnMap(width, height, tiles)
