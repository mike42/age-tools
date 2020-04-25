from typing import List

from attr import dataclass

from libage.scenario.data import ScnDataReader


@dataclass
class RandomMapMeta:
    id: int
    borders: tuple
    border_usage: int
    water_shape: int
    base_terrain: int
    land_cover: int
    unused_id: int
    num_lands: int
    pointer1: int
    num_terrains: int
    pointer2: int
    num_objects: int
    pointer3: int
    num_elevations: int
    pointer4: int

    @staticmethod
    def read(data: ScnDataReader):
        id = data.uint32(debug='random_map_id')
        borders = (
            data.uint32(debug='random_map_border_1'),
            data.uint32(debug='random_map_border_2'),
            data.uint32(debug='random_map_border_3'),
            data.uint32(debug='random_map_border_4')
        )
        border_usage = data.uint32(debug='random_map_border_usage')
        water_shape = data.uint32(debug='random_map_water_shape')
        base_terrain = data.uint32(debug='random_map_base_terrain')
        land_cover = data.uint32(debug='random_map_land_cover')
        unused_id = data.uint32(debug='random_map_border_unused_id')
        num_lands = data.uint32(debug='random_map_num_lands')
        pointer1 = data.uint32()
        num_terrains = data.uint32(debug='random_map_num_terrains')
        pointer2 = data.uint32()
        num_objects = data.uint32(debug='random_map_num_objects')
        pointer3 = data.uint32()
        num_elevations = data.uint32(debug='random_map_num_elevations')
        pointer4 = data.int32()
        return RandomMapMeta(
            id,
            borders,
            border_usage,
            water_shape,
            base_terrain,
            land_cover,
            unused_id,
            num_lands,
            pointer1,
            num_terrains,
            pointer2,
            num_objects,
            pointer3,
            num_elevations,
            pointer4
        )


@dataclass
class RandomMapLand:
    id: int
    terrain_type: int
    spacing: int
    base_square_radius: int
    zone: int
    placement_type: int
    land_x: int
    land_y: int
    amount_of_land_used_percent: int
    land_by_player_flag: int
    radius: int
    fade: int
    clumpiness_factor: int

    @staticmethod
    def read(data: ScnDataReader):
        id = data.uint32(debug='random_map_id')
        terrain_type = data.uint8(debug='random_map_terrain_type')
        _padding1 = data.uint16(debug='random_map_padding1')
        _padding2 = data.uint8(debug='random_map_padding2')
        spacing = data.int32(debug='random_map_spacing')
        base_square_radius = data.int32(debug='random_map_base_square_radius')
        zone = data.int8(debug='random_map_zone')
        placement_type = data.int8(debug='random_map_placement_type')
        _padding3 = data.uint16(debug='random_map_padding3')
        land_x = data.int32(debug='random_map_land_x')
        land_y = data.int32(debug='random_map_land_y')
        amount_of_land_used_percent = data.int8(debug='random_map_amount_of_land_used_percent')
        land_by_player_flag = data.int8(debug='random_map_land_by_player_flag')
        _padding4 = data.uint16(debug='random_map_padding4')
        radius = data.int32(debug='random_map_radius')
        fade = data.int32(debug='random_map_fade')
        clumpiness_factor = data.int32(debug='random_map_clumpiness_factor')
        return RandomMapLand(
            id,
            terrain_type,
            spacing,
            base_square_radius,
            zone,
            placement_type,
            land_x,
            land_y,
            amount_of_land_used_percent,
            land_by_player_flag,
            radius,
            fade,
            clumpiness_factor
        )


@dataclass
class RandomMapElevation:
    percent: int
    height: int
    clumps: int
    spacing: int
    base_terrain_type: int
    base_elevation_type: int

    @staticmethod
    def read(data: ScnDataReader):
        percent = data.uint32()
        height = data.int32()
        clumps = data.int32()
        spacing = data.int32()
        base_terrain_type = data.int32()
        base_elevation_type = data.int32()
        return RandomMapElevation(
            percent,
            height,
            clumps,
            spacing,
            base_terrain_type,
            base_elevation_type
        )


@dataclass
class RandomMapTerrain:
    terrain_percent: int
    terrain_terrain_type: int
    terrain_clumps: int
    terrain_spacing: int
    terrain_base_terrain_type: int
    terrain_clumpiness_factor: int

    @staticmethod
    def read(data: ScnDataReader):
        terrain_percent = data.int32(debug='random_map_terrain_percent')
        terrain_terrain_type = data.int32(debug='random_map_terrain_type')
        terrain_clumps = data.int32(debug='random_map_terrain_clumps')
        terrain_spacing = data.int32(debug='random_map_terrain_spacing')
        terrain_base_terrain_type = data.int32(debug='random_map_terraint_type')
        terrain_clumpiness_factor = data.int32(debug='random_map_terrain_clumpiness_factor')
        return RandomMapTerrain(
            terrain_percent,
            terrain_terrain_type,
            terrain_clumps,
            terrain_spacing,
            terrain_base_terrain_type,
            terrain_clumpiness_factor
        )


@dataclass
class RandomMapObject:
    unit_type: int
    terrain_type: int
    group_flag: int
    scale_flag: int
    group_size: int
    group_size_variance: int
    group_count: int
    group_area: int
    player_id: int
    land_id: int
    min_distance_to_players: int
    max_distance_to_players: int

    @staticmethod
    def read(data: ScnDataReader):
        unit_type = data.uint32()
        terrain_type = data.int32()
        group_flag = data.int8()
        scale_flag = data.int8()
        _padding5 = data.uint16()
        group_size = data.int32()
        group_size_variance = data.int32()
        group_count = data.int32()
        group_area = data.int32()
        player_id = data.int32()
        land_id = data.int32()
        min_distance_to_players = data.int32()
        max_distance_to_players = data.int32()
        return RandomMapObject(
            unit_type,
            terrain_type,
            group_flag,
            scale_flag,
            group_size,
            group_size_variance,
            group_count,
            group_area,
            player_id,
            land_id,
            min_distance_to_players,
            max_distance_to_players
        )


@dataclass
class RandomMapElevationListWrapper:
    pointer: int
    items: List[RandomMapElevation]

    @staticmethod
    def read(data: ScnDataReader):
        # Not present in AOE1 data file, a bit of a guess
        random_map_num_elevations = data.uint32(debug='random_map_num_elevations')
        pointer = data.uint32(debug='random_map_elevation_pointer')
        items = [RandomMapElevation.read(data) for _ in range(0, random_map_num_elevations)]
        return RandomMapElevationListWrapper(
            pointer,
            items
        )


@dataclass
class RandomMapObjectListWrapper:
    pointer: int
    items: List[RandomMapObject]

    @staticmethod
    def read(data: ScnDataReader):
        random_map_num_objects = data.uint32(debug='random_map_num_objects')
        pointer = data.uint32()
        items = [RandomMapObject.read(data) for _ in range(0, random_map_num_objects)]
        return RandomMapObjectListWrapper(
            pointer,
            items
        )


@dataclass
class RandomMapTerrainListWrapper:
    pointer: int
    items: List[RandomMapTerrain]

    @staticmethod
    def read(data: ScnDataReader):
        random_map_num_terrains = data.int32(debug='random_map_terrain_count')  # could be land ID??
        pointer = data.uint32(debug='random_map_terrain_pointer')
        items = [RandomMapTerrain.read(data) for _ in range(0, random_map_num_terrains)]
        return RandomMapTerrainListWrapper(
            pointer,
            items
        )


@dataclass
class RandomMapLandListWrapper:
    pointer: int
    items: List[RandomMapLand]

    @staticmethod
    def read(data: ScnDataReader):
        random_map_num_lands = data.int32(debug='random_map_land_count')
        pointer = data.uint32(debug='random_map_land_pointer')
        items = [RandomMapLand.read(data) for _ in range(0, random_map_num_lands)]
        return RandomMapLandListWrapper(
            pointer,
            items
        )


@dataclass
class RandomMap:
    random_map_borders: tuple
    border_usage: int
    water_shape: int
    base_terrain: int
    land_cover: int
    unused_id: int
    lands: RandomMapLandListWrapper
    terrains: RandomMapTerrainListWrapper
    objects: RandomMapObjectListWrapper
    elevations: RandomMapElevationListWrapper

    @staticmethod
    def read(data: ScnDataReader):
        random_map_borders = (
            data.uint32(debug='random_map_border_1'),
            data.uint32(debug='random_map_border_2'),
            data.uint32(debug='random_map_border_3'),
            data.uint32(debug='random_map_border_4')
        )
        border_usage = data.uint32(debug='random_map_border_usage')
        water_shape = data.uint32(debug='random_map_water_shape')
        base_terrain = data.uint32(debug='random_map_base_terrain')
        land_cover = data.uint32(debug='random_map_land_cover')
        unused_id = data.uint32(debug='random_map_border_unused_id')
        lands = RandomMapLandListWrapper.read(data)
        terrains = RandomMapTerrainListWrapper.read(data)
        objects = RandomMapObjectListWrapper.read(data)
        elevations = RandomMapElevationListWrapper.read(data)
        return RandomMap(
            random_map_borders,
            border_usage,
            water_shape,
            base_terrain,
            land_cover,
            unused_id,
            lands,
            terrains,
            objects,
            elevations
        )


@dataclass
class RandomMapListWrapper:
    num_random_maps: int
    random_maps_pointer: int
    random_map_meta: List[RandomMapMeta]
    random_maps: List[RandomMap]

    @staticmethod
    def read(data: ScnDataReader):
        data.mark('random maps')
        num_random_maps = data.uint32(debug='num_random_maps')
        random_maps_pointer = data.uint32(debug='random_maps_pointer')  # 39845000 in empires_up.dat
        random_map_meta = [RandomMapMeta.read(data) for _ in range(0, num_random_maps)]
        # Data from random_map_meta repeats here
        random_maps = [RandomMap.read(data) for _ in range(0, num_random_maps)]
        return RandomMapListWrapper(
            num_random_maps,
            random_maps_pointer,
            random_map_meta,
            random_maps
        )


def load(data: ScnDataReader) -> RandomMapListWrapper:
    """
    Read all random maps from here
    """
    return RandomMapListWrapper.read(data)
