from dataclasses import dataclass

from libage.scenario.data import ScnDataReader, ScnDataWriter


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

    def write(self, data: ScnDataWriter):
        data.uint32(self.active)
        data.uint32(self.player_type)
        data.uint32(self.civilization)
        data.uint32(self.posture)
