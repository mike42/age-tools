from typing import List

from attr import dataclass

from libage.scenario.data import ScnDataReader


@dataclass
class ColorTable:
    name: str
    id: int
    drs_res: int
    minimap_color: int
    # According to advanced genie editor: 0=Transform,1=Transform player color,2=Shadow,3=Translucent
    color_table_type: int

    @staticmethod
    def read(data: ScnDataReader):
        color_table_name = data.string_fixed(30, debug='color_table_name')
        color_table_id = data.uint16(debug='color_table_id')
        drs_res = data.uint16(debug='color_table_drs_res')  # All blanks?
        minimap_color = data.uint8(debug='color_table_minimap_color')  # Possibly a minimap color?
        color_table_type = data.uint8(debug='color_table_type')  # All 1's except the last one, which is 2.
        return ColorTable(color_table_name, color_table_id, drs_res, minimap_color, color_table_type)


def load(data: ScnDataReader) -> List[ColorTable]:
    """
    Read in all of the colors
    """
    data.mark(name='colors')
    num_color_tables = data.uint16(debug='num_color_tables')
    return [ColorTable.read(data) for _ in range(0, num_color_tables)]
