from attr import dataclass

from libage.scenario.data import ScnDataReader

@dataclass
class Terrain:

    @staticmethod
    def read(data: ScnDataReader):
        return Terrain()


def load(data: ScnDataReader):
    # Terrain
    data.mark(name='terrain')
    # num_terrains_override = num_terrains
    num_terrains_override = 32
    for i in range(0, num_terrains_override):
        data.boolean8(debug='terrain_enabled {}'.format(i))
        data.uint8(debug='terrain_random {}'.format(i)) # always 0?
        data.string_fixed(size=13, debug='terrain_name {}'.format(i))
        data.string_fixed(size=13, debug='terrain_texture_name {}'.format(i))  # Maybe read as int and test agains -1?
        data.int32(debug='terrain_slp_id {}'.format(i))
        data.int32(debug='terrain_slp_pointer {}'.format(i))
        data.int32(debug='terrain_sound_id {}'.format(i))
        data.uint8(debug='terrain_minimap_color_high {}'.format(i)) #  These colors are off-by-one compared with AGE.
        data.uint8(debug='terrain_minimap_color_medium {}'.format(i))
        data.uint8(debug='terrain_minimap_color_low {}'.format(i))
        data.uint8(debug='terrain_minimap_color_cliff_lt {}'.format(i))
        data.uint8(debug='terrain_minimap_color_cliff_rt {}'.format(i))
        data.int8(debug='terrain_passable_id {}'.format(i))
        data.int8(debug='terrain_impassable_id {}'.format(i))
        # Animation
        data.boolean8(debug='terrain_animation_enabled {}'.format(i))
        data.int16(debug='terrain_anim_num_frames {}'.format(i))
        data.int16(debug='terrain_anim_num_pause_frames {}'.format(i))
        data.float32(debug='terrain_anim_frame_interval {}'.format(i))
        data.float32(debug='terrain_anim_replay_delay {}'.format(i))
        data.int16(debug='terrain_anim_frame {}'.format(i))
        data.int16(debug='terrain_anim_draw_frame {}'.format(i))
        data.float32(debug='terrain_anim_animate_last {}'.format(i))
        data.boolean8(debug='terrain_anim_frame_changed {}'.format(i))
        data.boolean8(debug='terrain_anim_drawn {}'.format(i))
        # Elevation sprites
        for j in range(0, 19):
            data.uint16(debug="terrain_elevation_sprite_frames {} {}".format(i, j))  # frames
            data.uint16(debug="terrain_elevation_sprite_facets {} {}".format(i, j)) # facets
            data.uint16(debug="terrain_elevation_sprite_frame_id {} {}".format(i, j)) # frame_id
        data.int16(debug="terrain_to_draw {}".format(i))
        data.uint16(debug="terrain_rows {}".format(i))
        data.uint16(debug="terrain_cols {}".format(i))
        # Borders
        for j in range(0, num_terrains_override):
            data.uint16(debug="terrain_border {} {}".format(i, j))

        # Objects
        for j in range(0, 30):
            data.uint16(debug="terrain_object_id {} {}".format(i, j))
        for j in range(0, 30):
            data.int16(debug="terrain_density {} {}".format(i, j))
        for j in range(0, 30):
            data.int8(debug="terrain_placement_flag {} {}".format(i, j))  # 0 for random, 1 for central

        data.uint16(debug="terrain_object_count {}".format(i))
        data.uint16(debug="padding {}".format(i))
    return []