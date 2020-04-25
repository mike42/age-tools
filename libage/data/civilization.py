from typing import List

from attr import dataclass

from libage.data.unit import read_unit
from libage.scenario.data import ScnDataReader

@dataclass
class Civilization:

    @staticmethod
    def read(data: ScnDataReader):
        return Civilization()


def load(data: ScnDataReader) -> List[Civilization]:
    """
    Read all civilizations from here
    """
    data.mark("civilizations")
    num_civs = data.int16(debug='num_civs')
    for i in range(0, num_civs):
        data.uint8(debug='civ_type {}'.format(i))
        data.string_fixed(size=20, debug='civ_name {}'.format(i))
        civ_num_attributes = data.uint16(debug='civ_num_attributes {}'.format(i))
        civ_effect = data.int16(debug='civ_effect {}'.format(i))
        # civ_bonus_effect = data.int16(debug='civ_bonus_effect {}'.format(i)) # Might not exist in AOE1 dat.
        civ_attributes = [data.float32(debug='civ_attribute {} {}'.format(i, x)) for x in range(0, civ_num_attributes)]
        civ_icon_set = data.uint8(debug='civ_icon_set {}'.format(i))
        civ_num_units = data.uint16(debug='civ_num_units {}'.format(i))
        civ_unit_available = [data.boolean32(debug='civ_unit_available {} {}'.format(i, x)) for x in range(0, civ_num_units)]
        for j in range(0, civ_num_units):
            if not civ_unit_available[j]:
                continue
            read_unit(data)
    return []
