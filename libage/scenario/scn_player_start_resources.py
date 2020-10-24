from dataclasses import dataclass

from libage.scenario.data import ScnDataReader, ScnDataWriter


@dataclass
class ScnPlayerStartResources:
    wood: int
    gold: int
    food: int
    stone: int
    ore: int
    goods: int
    color: int

    @staticmethod
    def read(data: ScnDataReader, version: float):
        return ScnPlayerStartResources(
            wood=data.uint32(),
            gold=data.uint32(),
            food=data.uint32(),
            stone=data.uint32(),
            ore=data.uint32() if version >= 1.17 else 0,
            goods=data.uint32() if version >= 1.17 else 0,
            color=data.uint32() if version >= 1.24 else 0,
        )

    def write(self, data: ScnDataWriter, version: float):
        data.uint32(self.wood),
        data.uint32(self.gold),
        data.uint32(self.food),
        data.uint32(self.stone),
        if version >= 1.17:
            data.uint32(self.ore)
            data.uint32(self.goods)
        if version >= 1.24:
            data.uint32(self.color)
