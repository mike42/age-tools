#!/usr/bin/env python3

import logging
from enum import Enum
from typing import List

from PIL import Image

from libage.scenario import scenario
from libage.scenario.map import ScnMapTile, ScnMap


class UnderlyingTerrain(Enum):
    GRASS = 0
    DESERT = 1
    WATER = 2
    DEEP_WATER = 3


class Direction(Enum):
    NORTH = 0
    NORTH_EAST = 1
    EAST = 2
    SOUTH_EAST = 3
    SOUTH = 4
    SOUTH_WEST = 5
    WEST = 6
    NORTH_WEST = 7


def texture_tile_select(x, y, terrain: list):
    return terrain[((x // 2) % 2) + (y % 2)]


def base_terrain_select(this_tile: ScnMapTile):
    if this_tile.terrain == 1:
        return UnderlyingTerrain.WATER
    elif this_tile.terrain == 0 or this_tile.terrain == 10 or this_tile.terrain == 20 or this_tile.terrain == 19:
        return UnderlyingTerrain.GRASS
    elif this_tile.terrain == 6 or this_tile.terrain == 13 or this_tile.terrain == 2:
        return UnderlyingTerrain.DESERT
    elif this_tile.terrain == 4:
        # Shallows!
        return UnderlyingTerrain.WATER
    elif this_tile.terrain == 22:
        return UnderlyingTerrain.DEEP_WATER
    else:
        # Assume grass
        return UnderlyingTerrain.GRASS


def map_get_tile(map: ScnMap, x: int, y: int):
    return map.tiles[x + y * map.height]


def map_terrain_or_default(map: ScnMap, x, y, default: UnderlyingTerrain):
    if x < 0 or y < 0 or x >= map.width or y >= map.height:
        return default
    return base_terrain_select(map_get_tile(map, x, y))


def neighbour_terrain_type(map: ScnMap, x: int, y: int):
    default = base_terrain_select(map_get_tile(map, x, y))
    north = map_terrain_or_default(map, x + 1, y - 1, default)
    north_east = map_terrain_or_default(map, x + 1, y, default)
    east = map_terrain_or_default(map, x + 1, y + 1, default)
    south_east = map_terrain_or_default(map, x, y + 1, default)
    south = map_terrain_or_default(map, x - 1, y + 1, default)
    south_west = map_terrain_or_default(map, x - 1, y, default)
    west = map_terrain_or_default(map, x - 1, y - 1, default)
    north_west = map_terrain_or_default(map, x, y - 1, default)
    ret = [north, north_east, east, south_east, south, south_west, west, north_west]
    return ret


def select_border(neighbours: List[UnderlyingTerrain], check: UnderlyingTerrain):
    if neighbours[Direction.NORTH_WEST.value] == check and neighbours[Direction.WEST.value] == check and neighbours[Direction.SOUTH_WEST.value] == check:
        return 0
    if neighbours[Direction.NORTH_WEST.value] == check and neighbours[Direction.NORTH.value] == check and neighbours[Direction.NORTH_EAST.value] == check:
        return 1
    if neighbours[Direction.SOUTH_WEST.value] == check and neighbours[Direction.SOUTH.value] == check and neighbours[Direction.SOUTH_EAST.value] == check:
        return 2
    if neighbours[Direction.NORTH_EAST.value] == check and neighbours[Direction.EAST.value] == check and neighbours[Direction.SOUTH_EAST.value] == check:
        return 3

    if neighbours[Direction.NORTH_WEST.value] == check:
        return 8
    if neighbours[Direction.SOUTH_EAST.value] == check:
        return 9
    if neighbours[Direction.SOUTH_WEST.value] == check:
        return 10
    if neighbours[Direction.NORTH_EAST.value] == check:
        return 11

    if neighbours[Direction.WEST.value] == check:
        return 4
    if neighbours[Direction.NORTH.value] == check:
        return 5
    if neighbours[Direction.SOUTH.value] == check:
        return 6
    if neighbours[Direction.EAST.value] == check:
        return 7

    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    scenario1 = scenario.load('aoe1_ror_inland_tiny_random.scx')

    # Some terrains
    grass = []
    water = []
    desert = []
    water_dark = []
    for i in range(0, 4):
        grass.append(Image.open("terrain/15001_{:03d}.png".format(i)))
    for i in range(0, 4):
        water.append(Image.open("terrain/15002_{:03d}.png".format(i)))
    for i in range(0, 4):
        desert.append(Image.open("terrain/15000_{:03d}.png".format(i)))
    for i in range(0, 4):
        water_dark.append(Image.open("terrain/15003_{:03d}.png".format(i)))

    # Some borders
    border_desert_water = []
    border_grass_desert = []
    for i in range(0, 12):
        border_desert_water.append(Image.open("border/20000_{:03d}.png".format(i)))
    for i in range(0, 12):
        border_grass_desert.append(Image.open("border/20001_{:03d}.png".format(i)))

    TILE_WIDTH = 64
    TILE_HEIGHT = 32

    world_width = scenario1.map_scen.width
    world_height = scenario1.map_scen.height

    display_width = TILE_WIDTH + (((world_width - 1) + (world_height - 1)) * (TILE_WIDTH // 2))
    display_height = TILE_HEIGHT + (((world_width - 1) + (world_height - 1)) * (TILE_HEIGHT // 2))

    outp = Image.new('RGBA', (display_width, display_height), (255, 255, 255, 0))

    diamond_left_x = 0  # This is basically a constant
    diamond_left_y = (world_width - 1) * (TILE_HEIGHT // 2)

    for world_x in range(0, world_width):
        for world_y in range(0, world_height):
            this_tile_display_x = diamond_left_x + ((TILE_WIDTH // 2) * (world_x + world_y))
            this_tile_display_y = diamond_left_y + ((TILE_HEIGHT // 2) * (world_y - world_x))
            this_tile = map_get_tile(scenario1.map_scen, world_x, world_y)
            # Figure out what the base tile would be
            this_tile_terrain_type = base_terrain_select(this_tile)
            if this_tile_terrain_type == UnderlyingTerrain.DEEP_WATER:
                this_tile_terrain_frame_list = water_dark
            elif this_tile_terrain_type == UnderlyingTerrain.WATER:
                this_tile_terrain_frame_list = water
            elif this_tile_terrain_type == UnderlyingTerrain.DESERT:
                this_tile_terrain_frame_list = desert
            else:
                this_tile_terrain_frame_list = grass
            this_terrain_tile_frame = texture_tile_select(world_x, world_y, this_tile_terrain_frame_list)
            outp.paste(this_terrain_tile_frame, (this_tile_display_x, this_tile_display_y), this_terrain_tile_frame)
            # Paste in any bordering info (some are semi-transparent tiles)
            neighbours = neighbour_terrain_type(scenario1.map_scen, world_x, world_y)
            if this_tile_terrain_type == UnderlyingTerrain.DESERT and UnderlyingTerrain.WATER in neighbours:
                border_direction = select_border(neighbours, UnderlyingTerrain.WATER)
                outp.paste(border_desert_water[border_direction], (this_tile_display_x, this_tile_display_y), border_desert_water[border_direction])
            elif this_tile_terrain_type == UnderlyingTerrain.GRASS and UnderlyingTerrain.DESERT in neighbours:
                border_direction = select_border(neighbours, UnderlyingTerrain.DESERT)
                outp.paste(border_grass_desert[border_direction], (this_tile_display_x, this_tile_display_y), border_grass_desert[border_direction])

    # Just checking type IDs
    # how_common_is = {}
    # for player_id in range(0, len(scenario1['objects'])):
    #     for object in scenario1['objects'][player_id]:
    #         if object.type_id not in how_common_is:
    #             how_common_is[object.type_id] = 0
    #         how_common_is[object.type_id] = how_common_is[object.type_id] + 1
    # for w in sorted(how_common_is, key=how_common_is.get, reverse=True):
    #     print(w, how_common_is[w])

    # for file in sys.argv[1:]:
    #
    #     w_tiles = scenario1['map_scen'].width
    #     h_tiles = scenario1['map_scen'].height
    #     print(w_tiles)
    #     print(h_tiles)

    outp.save('foo.png')
