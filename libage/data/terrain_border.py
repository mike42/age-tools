from dataclasses import dataclass
from typing import List

from libage.scenario.data import ScnDataReader


@dataclass
class TerrainBorder:

    @staticmethod
    def read(data: ScnDataReader):
        data.boolean8(debug="border_enabled")
        data.boolean8(debug="border_random")
        data.string_fixed(size=13, debug='border_name')
        data.string_fixed(size=13, debug='border_texture_name')  # Maybe read as int and test agains -1?
        data.int32(debug='border_slp_id')
        data.int32(debug='border_slp_pointer')
        data.int32(debug='border_sound_id')
        data.uint8(debug='border_minimap_color_high')
        data.uint8(debug='border_minimap_color_medium')
        data.uint8(debug='border_minimap_color_low')
        # Same as terrain animation
        data.boolean8(debug='border_manimation_enabled')
        data.int16(debug='border_anim_num_frames')
        data.int16(debug='border_anim_num_pause_frames')
        data.float32(debug='border_anim_frame_interval')
        data.float32(debug='border_anim_replay_delay')
        data.int16(debug='border_anim_frame')
        data.int16(debug='border_anim_draw_frame')
        data.float32(debug='border_anim_animate_last')
        data.boolean8(debug='border_anim_frame_changed')
        data.boolean8(debug='border_anim_drawn')
        for j in range(0, 19):
            for k in range(0, 12):
                data.uint16(debug="border_elevation_sprite_frames {} {}".format(j, k))  # frames
                data.uint16(debug="border_elevation_sprite_facets {} {}".format(j, k))  # facets
                data.uint16(debug="border_elevation_sprite_rame_id {} {}".format(j, k))  # frame_id

        data.int8(debug='border_draw_tile')
        data.uint8(debug='padding')
        data.int16(debug='border_underlay_terrain')
        data.int16(debug='border_style')
        return TerrainBorder()


def load(data: ScnDataReader) -> List[TerrainBorder]:
    """
    Read all of the terrain borders
    """
    data.mark(name='terrain borders')
    return [TerrainBorder.read(data) for _ in range(0, 16)]
