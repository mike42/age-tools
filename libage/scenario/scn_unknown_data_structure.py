from dataclasses import dataclass
from typing import List

from libage.scenario.data import ScnDataReader, ScnDataWriter


@dataclass
class UnknownPlayerDataStructure:
    field1: str
    field2: float
    field3: float
    field4: int
    field5: int
    field6: int
    field7: int
    field8: List[int]
    field9: List[int]
    field10: float
    field11: float
    field12: List[int]

    @staticmethod
    def read(data: ScnDataReader):
        field1 = data.string16(debug='player_name_repeated')
        field2 = data.float32(debug='unknown field 1')
        field3 = data.float32(debug='unknown field 2')
        field4 = data.uint16(debug='unknown field 3')
        field5 = data.uint16(debug='unknown field 4')
        field6 = data.uint8(debug='unknown field 5')
        field7 = data.uint16(debug='unknown field 6')
        field8 = []
        for j in range(0, 9):
            something = data.uint8(debug='unknown field {}'.format(j))
            field8.append(something)
        field9 = []
        for j in range(0, 9):
            something = data.uint32(debug='unknown field {}'.format(j))
            field9.append(something)
        field10 = data.float32(debug="unknown field")  # 1.00
        field11 = data.float32(debug="unknown field")  # only seen 0. guess this could be float as well ?
        field12 = []
        for j in range(0, 9):  # all 0's. guessing it could hold another list of 9 values?
            something = data.uint8(debug='unknown field {}'.format(j))
            field12.append(something)
        return UnknownPlayerDataStructure(
            field1,
            field2,
            field3,
            field4,
            field5,
            field6,
            field7,
            field8,
            field9,
            field10,
            field11,
            field12
        )

    def write(self, data: ScnDataWriter):
        data.string16(self.field1)
        data.float32(self.field2)
        data.float32(self.field3)
        data.uint16(self.field4)
        data.uint16(self.field5)
        data.uint8(self.field6)
        data.uint16(self.field7)
        for j in range(0, 9):
            data.uint8(self.field8[j])
        for j in range(0, 9):
            data.uint32(self.field9[j])
        data.float32(self.field10)  # 1.00
        data.float32(self.field11)
        for j in range(0, 9):
            data.uint8(self.field12[j])


@dataclass
class UnknownDataStructure:
    player_count: int
    unknown_player_data_structure: List[UnknownPlayerDataStructure]

    @staticmethod
    def read(data: ScnDataReader):
        # Not sure how to walk through this trailing data yet.
        # Fails on both of the Multiplayer Border Patrol maps bundled with ROR and DE.
        # This data seems to be either 1320 or 708 bytes long.

        # Some kind of per-player data structure here
        player_count = data.uint32(debug="unknown field")  # Only seen 9.
        player_unknown_structure_list = []
        for i in range(1, 9):
            player_unknown_structure = UnknownPlayerDataStructure.read(data)
            player_unknown_structure_list.append(player_unknown_structure)
        data.done()
        return UnknownDataStructure(
            player_count,
            player_unknown_structure_list
        )

    def write(self, data: ScnDataWriter):
        data.uint32(self.player_count)
        for i in range(1, 9):
            self.unknown_player_data_structure[i - 1].write(data)


def default() -> UnknownDataStructure:
    return UnknownDataStructure(9, [
        UnknownPlayerDataStructure(field1='Player 1',
                                   field2=85.0,
                                   field3=59.0,
                                   field4=72,
                                   field5=72,
                                   field6=0,
                                   field7=9,
                                   field8=[1, 1, 3, 3, 3, 3, 3, 3, 3],
                                   field9=[0, 1, 4, 4, 4, 4, 4, 4, 4],
                                   field10=1.0,
                                   field11=0.0,
                                   field12=[0, 0, 0, 0, 0, 0, 0, 0, 0]),
        UnknownPlayerDataStructure(field1='Player 2',
                                   field2=72.0,
                                   field3=72.0,
                                   field4=72,
                                   field5=72,
                                   field6=0,
                                   field7=9,
                                   field8=[1, 3, 1, 3, 3, 3, 3, 3, 3],
                                   field9=[0, 4, 1, 4, 4, 4, 4, 4, 4],
                                   field10=1.0,
                                   field11=0.0,
                                   field12=[0, 0, 0, 0, 0, 0, 0, 0, 0]),
        UnknownPlayerDataStructure(field1='Player 3',
                                   field2=72.0,
                                   field3=72.0,
                                   field4=72,
                                   field5=72,
                                   field6=0,
                                   field7=9,
                                   field8=[1, 3, 3, 1, 3, 3, 3, 3, 3],
                                   field9=[0, 4, 4, 1, 4, 4, 4, 4, 4],
                                   field10=1.0,
                                   field11=0.0,
                                   field12=[0, 0, 0, 0, 0, 0, 0, 0, 0]),
        UnknownPlayerDataStructure(field1='Player 4',
                                   field2=72.0,
                                   field3=72.0,
                                   field4=72,
                                   field5=72,
                                   field6=0,
                                   field7=9,
                                   field8=[1, 3, 3, 3, 1, 3, 3, 3, 3],
                                   field9=[0, 4, 4, 4, 1, 4, 4, 4, 4],
                                   field10=1.0,
                                   field11=0.0,
                                   field12=[0, 0, 0, 0, 0, 0, 0, 0, 0]),
        UnknownPlayerDataStructure(field1='Player 5',
                                   field2=72.0,
                                   field3=72.0,
                                   field4=72,
                                   field5=72,
                                   field6=0,
                                   field7=9,
                                   field8=[1, 3, 3, 3, 3, 1, 3, 3, 3],
                                   field9=[0, 4, 4, 4, 4, 1, 4, 4, 4],
                                   field10=1.0,
                                   field11=0.0,
                                   field12=[0, 0, 0, 0, 0, 0, 0, 0, 0]),
        UnknownPlayerDataStructure(field1='Player 6',
                                   field2=72.0,
                                   field3=72.0,
                                   field4=72,
                                   field5=72,
                                   field6=0,
                                   field7=9,
                                   field8=[1, 3, 3, 3, 3, 3, 1, 3, 3],
                                   field9=[0, 4, 4, 4, 4, 4, 1, 4, 4],
                                   field10=1.0,
                                   field11=0.0,
                                   field12=[0, 0, 0, 0, 0, 0, 0, 0, 0]),
        UnknownPlayerDataStructure(field1='Player 7',
                                   field2=72.0,
                                   field3=72.0,
                                   field4=72,
                                   field5=72,
                                   field6=0,
                                   field7=9,
                                   field8=[1, 3, 3, 3, 3, 3, 3, 1, 3],
                                   field9=[0, 4, 4, 4, 4, 4, 4, 1, 4],
                                   field10=1.0,
                                   field11=0.0,
                                   field12=[0, 0, 0, 0, 0, 0, 0, 0, 0]),
        UnknownPlayerDataStructure(field1='Player 8',
                                   field2=72.0,
                                   field3=72.0,
                                   field4=72,
                                   field5=72,
                                   field6=0,
                                   field7=9,
                                   field8=[1, 3, 3, 3, 3, 3, 3, 3, 1],
                                   field9=[0, 4, 4, 4, 4, 4, 4, 4, 1],
                                   field10=1.0,
                                   field11=0.0,
                                   field12=[0, 0, 0, 0, 0, 0, 0, 0, 0])
    ])
