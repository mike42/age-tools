from dataclasses import dataclass

from libage.scenario.data import ScnDataReader, ScnDataWriter


@dataclass
class WorldPlayer:
    food: float
    wood: float
    gold: float
    stone: float
    ore: float
    goods: float
    population: float

    @staticmethod
    def read_classic(data: ScnDataReader, player_version: float):
        return WorldPlayer(
            data.float32() if player_version > 1.06 else 200.0,
            data.float32() if player_version > 1.06 else 200.0,
            data.float32() if player_version > 1.06 else 50.0,
            data.float32() if player_version > 1.06 else 100.0,
            data.float32() if player_version > 1.12 else 100.0,
            data.float32() if player_version > 1.12 else 0.0,
            data.float32() if player_version > 1.14 else 75.0,
        )

    @staticmethod
    def read_de(data: ScnDataReader, player_version: float):
        return WorldPlayer(
            data.float32(debug='food'),
            data.float32(debug='wood'),
            data.float32(debug='gold'),
            data.float32(debug='stone'),
            0,
            0,
            data.float32(debug='population') if player_version >= 3.13 else 75.0
        )

    def write_classic(self, data: ScnDataWriter, player_version: float):
        if player_version > 1.06:
            data.float32(self.food)
            data.float32(self.wood)
            data.float32(self.gold)
            data.float32(self.stone)
        if player_version > 1.12:
            data.float32(self.ore)
            data.float32(self.goods)
            data.float32(self.population)

    def write_de(self, data: ScnDataWriter):
        data.float32(self.food)
        data.float32(self.wood)
        data.float32(self.gold)
        data.float32(self.stone)
        data.float32(self.population)
