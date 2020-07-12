from dataclasses import dataclass

from libage.scenario.data import ScnDataReader


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