from dataclasses import dataclass
from typing import List

from libage.scenario.data import ScnDataReader, ScnDataWriter


@dataclass
class ScnMapTile:
    terrain: int
    elevation: int
    zone: int

    @staticmethod
    def read(data: ScnDataReader):
        return ScnMapTile(
            data.uint8(),
            data.uint8(),
            data.uint8()
        )

    def write(self, data: ScnDataWriter):
        data.uint8(self.terrain)
        data.uint8(self.elevation)
        data.uint8(self.zone)


@dataclass
class ScnMap:
    width: int
    height: int
    tiles: List[ScnMapTile]

    @staticmethod
    def read(data: ScnDataReader):
        width = data.uint32()
        height = data.uint32()
        tiles = []
        for i in range(0, height * width):
            tiles.append(ScnMapTile.read(data))
        return ScnMap(width, height, tiles)

    def write(self, data: ScnDataWriter):
        data.uint32(self.width)
        data.uint32(self.height)
        for tile in self.tiles:
            tile.write(data)
