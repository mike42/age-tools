from dataclasses import dataclass

from libage.scenario.data import ScnDataReader


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
    def read(data: ScnDataReader, file_version: float):
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
