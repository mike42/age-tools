from dataclasses import dataclass

from libage.scenario.data import ScnDataReader


@dataclass
class ScnPlayerBaseProperties:
    active: int
    player_type: int
    civilization: int
    posture: int

    @staticmethod
    def read(data: ScnDataReader):
        return ScnPlayerBaseProperties(
            data.uint32(),
            data.uint32(),
            data.uint32(),
            data.uint32()
        )

