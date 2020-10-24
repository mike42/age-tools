from dataclasses import dataclass

from libage.scenario.data import ScnDataReader, ScnDataWriter


@dataclass
class ScenarioObject:
    position: tuple
    id: int
    type_id: int
    state: int
    angle: float
    frame: int
    garrisoned_in:  int

    @staticmethod
    def read_classic(data: ScnDataReader, file_version: float):
        return ScenarioObject(
            (data.float32(), data.float32(), data.float32()),
            data.uint32(),
            data.uint16(),
            data.uint8(),
            data.float32(),
            # Not used in AOE1
            -1 if file_version < 1.15 else data.uint16(),
            -1 if file_version < 1.13 else data.uint32()
        )

    @staticmethod
    def read_de(data: ScnDataReader):
        return ScenarioObject(
            (data.float32(), data.float32(), data.float32()),
            data.uint32(),
            data.uint16(),
            data.uint8(),
            data.float32(),
            -1,
            -1
        )

    def write_classic(self, data: ScnDataWriter, file_version: float):
        data.float32(self.position[0])
        data.float32(self.position[1])
        data.float32(self.position[2])
        data.uint32(self.id),
        data.uint16(self.type_id),
        data.uint8(self.state),
        data.float32(self.angle),
        if file_version >= 1.15:
            data.uint16(self.frame)
        if file_version > 1.13:
            data.uint32(self.garrisoned_in)
