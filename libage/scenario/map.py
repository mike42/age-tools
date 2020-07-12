from dataclasses import dataclass

from libage.scenario.data import ScnDataReader

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


@dataclass
class ScnMap:
    width: int
    height: int
    tiles: list

    @staticmethod
    def read(data: ScnDataReader):
        width = data.uint32()
        height = data.uint32()
        tiles = []
        for i in range(0, height * width):
            tiles.append(ScnMapTile.read(data))
        return ScnMap(width, height, tiles)
