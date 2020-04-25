from typing import List

from attr import dataclass

from libage.scenario.data import ScnDataReader


@dataclass
class TerrainTable:
    unknown_value: int
    passable: List[float]


def load(data: ScnDataReader) -> List[TerrainTable]:
    # Read the terrain tables
    data.mark(name='terrain tables')
    num_terrain_tables = data.uint16(debug='num_terrain_tables')
    num_terrains = data.uint16(debug='num_terrains')
    unknown_values = []
    for terrain_table_id in range(0, num_terrain_tables):
        unknown_value = data.uint32(debug="terrain table {} unknown value".format(terrain_table_id))
        unknown_values.append(unknown_value)
    terrain_tables = []
    for terrain_table_id in range(0, num_terrain_tables):
        passable = [data.float32("passability table={} terrain={}".format(terrain_table_id, terrain_id)) for terrain_id in range(0, num_terrains)]
        terrain_tables.append(TerrainTable(unknown_values[terrain_table_id], passable))
    return terrain_tables
