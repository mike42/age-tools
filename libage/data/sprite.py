from dataclasses import dataclass
from typing import List


from libage.scenario.data import ScnDataReader


@dataclass
class SpriteDelta:
    field1: int
    field2: int
    field3: int
    field4: int
    field5: int
    field6: int
    field7: int

    @staticmethod
    def read(data: ScnDataReader):
        # Not complete yet!
        return SpriteDelta(
            data.uint16(),
            data.uint16(),
            data.uint32(),
            data.int16(),
            data.int16(),
            data.int16(),
            data.int16()
        )


@dataclass
class SpriteFacetProperty:
    delay: int
    sound_id: int

    @staticmethod
    def read(data: ScnDataReader):
        return SpriteFacetProperty(
            data.int16(),
            data.uint16()
        )


@dataclass
class SpriteFacet:
    properties: List[SpriteFacetProperty]

    @staticmethod
    def read(data: ScnDataReader):
        return SpriteFacet([SpriteFacetProperty.read(data) for _ in range(0, 3)])


@dataclass
class Sprite:
    sprite_id: int
    sprite_name: int
    sprite_filename: int
    sprite_slp_id: int
    sprite_is_loaded: bool
    sprite_color_flag: bool
    sprite_layer: int
    sprite_color_table: int
    sprite_transparent_selection: bool
    sprite_bounding_box: tuple
    sprite_sound_id: int
    attack_sounds_used: bool
    sprite_num_frames: int
    sprite_num_facets: int
    sprite_base_speed: int
    sprite_frame_rate: float
    sprite_replay_delay: float
    sprite_sequence_type: int
    sprite_other_id: int
    sprite_mirror_flag: int
    sprite_deltas: List[SpriteDelta]
    facets: List[SpriteFacet]

    @staticmethod
    def read(data: ScnDataReader, sprite_id):
        sprite_name = data.string_fixed(21, debug='sprite_name')
        sprite_filename = data.string_fixed(13, debug='sprite_filename')
        sprite_slp_id = data.uint32(debug='sprite_slp_id')
        sprite_is_loaded = data.boolean8(debug='sprite_is_loaded')
        sprite_color_flag = data.boolean8(debug='sprite_color_flag')
        sprite_layer = data.uint8(debug='sprite_layer')
        sprite_color_table = data.int16(debug='sprite_color_table')
        sprite_transparent_selection = data.boolean8(debug='sprite_transparent_selection')
        sprite_bounding_box = (
            data.int16(),  # X1
            data.int16(),  # Y1
            data.int16(),  # X2
            data.int16())  # Y2
        sprite_num_deltas = data.uint16(debug='sprite_num_deltas')
        sprite_sound_id = data.int16(debug='sprite_sound_id')
        attack_sounds_used = data.boolean8()
        sprite_num_frames = data.uint16()
        sprite_num_facets = data.uint16()
        sprite_base_speed = data.float32()
        sprite_frame_rate = data.float32()
        sprite_replay_delay = data.float32()
        sprite_sequence_type = data.uint8()
        sprite_other_id = data.uint16(debug='sprite_other_id')
        sprite_mirror_flag = data.uint8()
        # sprite_other_flag = data.uint8() # Reading 1 byte too far here, one of these must not be in the AOE1 file.
        sprite_deltas = [SpriteDelta.read(data) for _ in range(0, sprite_num_deltas)]
        facets = [SpriteFacet.read(data) for _ in range(0, sprite_num_facets)] if attack_sounds_used else []
        return Sprite(
            sprite_id,
            sprite_name,
            sprite_filename,
            sprite_slp_id,
            sprite_is_loaded,
            sprite_color_flag,
            sprite_layer,
            sprite_color_table,
            sprite_transparent_selection,
            sprite_bounding_box,
            sprite_sound_id,
            attack_sounds_used,
            sprite_num_frames,
            sprite_num_facets,
            sprite_base_speed,
            sprite_frame_rate,
            sprite_replay_delay,
            sprite_sequence_type,
            sprite_other_id,
            sprite_mirror_flag,
            sprite_deltas,
            facets
        )


def load(data: ScnDataReader) -> List[Sprite]:
    """
    Read all the sprites
    """
    data.mark(name='sprites')
    num_sprites = data.uint16(debug='num_sprites')
    sprites_exist = [data.uint32() for _ in range(0, num_sprites)]
    sprites = []
    for sprite_id in range(0, num_sprites):
        if sprites_exist[sprite_id] == 0:
            continue
        sprite = Sprite.read(data, sprite_id)
        sprites.append(sprite)
    return sprites
