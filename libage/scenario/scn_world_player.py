from dataclasses import dataclass

from libage.scenario.data import ScnDataReader


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
    def read(data: ScnDataReader, player_version: float):
        return WorldPlayer(
            data.float32() if player_version > 1.06 else 200.0,
            data.float32() if player_version > 1.06 else 200.0,
            data.float32() if player_version > 1.06 else 50.0,
            data.float32() if player_version > 1.06 else 100.0,
            data.float32() if player_version > 1.12 else 100.0,
            data.float32() if player_version > 1.12 else 0.0,
            data.float32() if player_version > 1.14 else 75.0,
        )