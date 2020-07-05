from dataclasses import dataclass
from typing import List


from libage.gamedata import technology, civilization, effect, random_map, terrain, terrain_border, sprite, sound, \
    color_table, terrain_table
from libage.gamedata.civilization import Civilization
from libage.gamedata.color_table import ColorTable
from libage.gamedata.effect import Effect
from libage.gamedata.random_map import RandomMapListWrapper
from libage.gamedata.sound import Sound
from libage.gamedata.sprite import Sprite
from libage.gamedata.technology import Technology
from libage.gamedata.terrain import Terrain
from libage.gamedata.terrain_border import TerrainBorder
from libage.gamedata.terrain_table import TerrainTable

from libage.scenario.data import ScnDataReader


@dataclass
class GameDataFile:
    version: str
    terrain_tables: List[TerrainTable]
    color_tables: List[ColorTable]
    sounds: List[Sound]
    sprites: List[Sprite]
    terrains: List[Terrain]
    terrain_borders: List[TerrainBorder]
    random_maps: RandomMapListWrapper
    effects: List[Effect]
    civilizations: List[Civilization]
    technologies: List[Technology]

    @staticmethod
    def read(data: ScnDataReader):
        """
        Read entire game data file from uncompressed data file
        """
        version = data.string_fixed(8)
        terrain_tables = terrain_table.load(data)
        color_tables = color_table.load(data)
        sounds = sound.load(data)
        sprites = sprite.load(data)
        discard_first_map_stuff(data)
        terrains = terrain.load(data)
        terrain_borders = terrain_border.load(data)
        discard_extra_map_stuff(data)
        random_maps = random_map.load(data)
        effects = effect.load(data)
        civilizations = civilization.load(data)
        technologies = technology.load(data)
        return GameDataFile(
            version,
            terrain_tables,
            color_tables,
            sounds, sprites,
            terrains,
            terrain_borders,
            random_maps,
            effects,
            civilizations,
            technologies
        )


def load(filename: str) -> GameDataFile:
    with open(filename, 'rb') as f:
        # Read entire file
        data = ScnDataReader(f.read())
        data.decompress()
        # Decompress only!
        # open("Empires_uncompressed.dat", 'wb').write(data.read())
        # exit(0)
        game_data_file = GameDataFile.read(data)
        data.done()
    return game_data_file


def discard_first_map_stuff(data: ScnDataReader):
    data.mark(name='map tiles')
    data.uint32(debug='__vfptr')
    data.uint32(debug='map_pointer')
    data.uint32(debug='map_width')
    data.uint32(debug='map_height')
    data.uint32(debug='world_width')
    data.uint32(debug='world_height')
    # Advanced Genie Editor describes these as "19 x (Width, Height, Delta Y) 1st is flat tile, then 2x8 elevation ties, then 2 1:1 tiles"
    for i in range(0, 19):
        data.int16(debug='tile width {}'.format(i))
        data.int16(debug='tile height {}'.format(i))
        data.int16(debug='tile delta_y {}'.format(i))
    data.uint16(debug="padding?")


def discard_extra_map_stuff(data: ScnDataReader):
    data.mark("Extra map stuff")
    # NB: Values from genie-rs skip way past random map data in AOE1 files.
    # data.int32(debug='_map_row_offset')
    # data.float32(debug='_map_min_x')
    # data.float32(debug='_map_min_y')
    # data.float32(debug='_map_max_x')
    # data.float32(debug='_map_max_y')
    # data.float32(debug='_map_max_x')
    # data.float32(debug='_map_max_y')
    # data.uint16(debug='_additional_terrain_count')
    # data.uint16(debug='_borders_used')
    # data.uint16(debug='_max_terrain')
    # data.uint16(debug='_tile_width')
    # data.uint16(debug='_tile_height')
    # data.uint16(debug='_tile_half_width')
    # data.uint16(debug='_tile_half_height')
    # data.uint16(debug='_elev_height')
    # data.uint16(debug='_current_row')
    # data.uint16(debug='_current_column')
    # data.uint16(debug='_block_begin_row')
    # data.uint16(debug='_block_end_row')
    # data.uint16(debug='_block_begin_column')
    # data.uint16(debug='_block_end_column')
    # data.int32(debug='_seach_map_pointer')
    # data.int32(debug='_seach_map_rows_pointer')
    # data.uint8(debug='_any_frame_change')
    # data.uint8(debug='_map_visible')
    # data.uint8(debug='_map_fog_of_war')
    # data.read(21 + 157 * 4)
    data.read(68)
