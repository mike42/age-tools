import logging

from attr import dataclass

#
# @dataclass
# class BaseUnit:
#
from libage.scenario.data import ScnDataReader


def read_base_unit_props(data: ScnDataReader):
    data.mark("base unit")
    unit_name_len = data.uint16(debug='unit_name_len')
    unit_id = data.int16(debug='unit_id')
    unit_name_string_id = data.int16(debug='unit_name_string_id')
    unit_creation_string_id = data.int16(debug='unit_creation_string_id')
    unit_class = data.int16(debug='unit_class')
    standing_sprite = data.int16(debug='standing_sprite')  # no standing sprite #2 here.. ?
    dying_sprite = data.int16(debug='dying_sprite')
    undead_sprite = data.int16(debug='undead_sprite')
    undead_flag = data.int8(debug='undead_flag')
    hp = data.uint16(debug='hp')
    los = data.float32(debug='los')
    garrison_capacity = data.uint8(debug='garrison_capacity')
    collision_radius = (
        data.float32(debug='collision_radius1'),
        data.float32(debug='collision_radius2'),
        data.float32(debug='collision_radius3')
    )
    unit_train_sound = data.int16(debug='train_sound')
    # unit_damage_sound = data.int16(debug='damage_sound')
    unit_death_spawn = data.int16(debug='unit_death_spawn')  # no unit_damage_sound here ??
    unit_sort_number = data.uint8(debug='unit_sort_number')
    unit_can_be_built_on = data.uint8(debug='unit_can_be_built_on')
    unit_button_picture = data.int16(debug='unit_button_picture')
    unit_hide_in_scenario_editor = data.boolean8(debug='unit_hide_in_scenario_editor')
    unit_portrait_picture = data.int16(debug='unit_portrait_picture')
    unit_enabled = data.boolean8(debug='unit_enabled')  # no unit_disabled here ??
    unit_tile_req = (data.int16(debug='unit_tile_req1'), data.int16(debug='unit_tile_req2')) # "Placement side terrains"
    unit_center_tile_req = (data.int16(debug='unit_center_tile_req1'), data.int16(debug='unit_center_tile_req1'))
    unit_construction_radius = (
    data.float32(debug='unit_construction_radius1'), data.float32(debug='unit_construction_radius2'))
    unit_elevation_flag = data.boolean8(debug='unit_elevation_flag')
    unit_fog_flag = data.boolean8(debug='unit_fog_flag')
    unit_terrain_restriction_id = data.uint16(debug='unit_terrain_restriction_id') # "terrain tables"
    unit_movement_type = data.uint8(debug='unit_movement_type')
    unit_attribute_max_amount = data.uint16(debug='unit_attribute_max_amount') # resource capacity
    unit_attribute_rot = data.float32(debug='unit_attribute_rot') # decay
    unit_area_effect_level = data.uint8(debug='unit_area_effect_level')
    unit_combat_level = data.uint8(debug='unit_combat_level')
    unit_select_level = data.uint8(debug='unit_select_level')
    unit_map_draw_level = data.uint8(debug='unit_map_draw_level')
    unit_level = data.uint8(debug='unit_level')
    unit_multiple_attribute_mod = data.float32(debug='unit_multiple_attribute_mod')
    unit_map_color = data.uint8(debug='unit_map_color')
    unit_help_string_id = data.uint32('unit_help_string_id')
    unit_help_page_id = data.uint32(debug='unit_help_page_id')
    unit_hotkey_id = data.uint32(debug='unit_hotkey_id')
    unit_recyclable = data.boolean8(debug='unit_recyclable')
    unit_track_as_resource = data.boolean8(debug='unit_track_as_resource')
    unit_create_doppleganger = data.boolean8(debug='unit_create_doppleganger')
    unit_resource_group = data.uint8(debug='unit_resource_group') # tree/stone/gold etc
    unit_occlusion_mask = data.uint8(debug='unit_occlusion_mask') # "hill mode" in AGE
    unit_obstruction_type = data.uint8(
        debug='unit_obstruction_type')  # dropped unit_selection_shape, unit_civilization, unit_attribute_piece
    # # object flags go here in later versions
    selection_outline_radius = (
        data.float32(debug='selection_outline_radius1'),
        data.float32(debug='selection_outline_radius2'),
        data.float32(debug='selection_outline_radius3')
    )
    for i in range(0, 3):
        attribute_res = data.int16(debug='attribute_res {}'.format(i))
        attribute_amount = data.float32(debug='attribute_amount {}'.format(i))
        attribute_store_mode = data.int8(debug='attribute_store_mode {}'.format(i))
    num_damage_sprites = data.uint8(debug='num_damage_sprites')
    for i in range(0, num_damage_sprites):
        damage_sprite = data.uint16(debug='damage_sprite {}'.format(i))
        damage_percent = data.uint8(debug='damage_percent {}'.format(i))
        damage_apply_mode = data.uint8(debug='damage_apply_mode {}'.format(i))
        damage_unused = data.uint8(debug='damage_unused {}'.format(i))
    unit_selected_sound = data.int16(debug='unit_selected_sound')
    unit_death_sound = data.int16(debug='unit_death_sound')
    unit_attack_reaction = data.uint8(debug='unit_attack_reaction')
    unit_convert_terrain_flag = data.uint8(debug='unit_convert_terrain_flag')
    unit_name = data.string_fixed(size=unit_name_len, debug='unit_name')
    data.uint16(debug='unit_copy_id')     # dropped unit_copy_id, unit_group
    return unit_name


def read_animated_unit_props(data):
    # animated unit props
    speed = data.float32('speed')
    return ''


def read_moving_unit_props(data):
    # moving unit props
    walk_graphic = data.int16(debug='walk_graphic')
    run_graphic = data.int16(debug='run_graphic')
    turn_speed = data.float32(debug='turn_speed')
    size_class = data.uint8(debug='size_class')
    trailing_unit = data.int16(debug='trailing_unit')
    trailing_options = data.uint8(debug='trailing_options')
    trailing_spacing = data.float32(debug='trailing_spacing')
    move_algorithm = data.uint8(debug='move_algorithm')


def read_action_unit_props(data):
    # action unit props
    data.mark('action unit props')
    data.int16(debug='default_task') # -1 probable default task
    data.float32(debug='search_radius') # 4 probable search radius
    data.float32(debug='work_rate') # 20 probable work rate
    data.int16(debug='drop_site') # 204 probable drop site
    data.int16(debug='backup_drop_site') # 204 probable drop site
    data.uint8(debug='task_by_group') # = task swap group?
    data.int16(debug='attack_sound')
    data.int16(debug='move_sound')
    data.uint8(debug='run_pattern') # not really checked
    num_tasks = data.int16(debug='num_tasks') # 0 for academy, 2 for alligator, assuming num_tasks
    for i in range(0, num_tasks): # Ordering could be off here
        data.mark('a task')
        data.int16(debug='action_task_type')
        data.int16(debug='unknown')
        data.uint8(debug='unknown')
        data.int16(debug='action_type')
        data.int16(debug='action_class')
        data.int16(debug='action_unit')
        data.int16(debug='action_terrain')
        data.int16(debug='action_resource_in')
        data.int16(debug='action_productivity_resource')
        data.int16(debug='action_resource_out')
        data.int16(debug='action_unused_resource')
        data.float32(debug='workval1')
        data.float32(debug='workval2')
        data.float32(debug='workval3')
        data.uint8(debug='action_is_default_maybe') # default flag?
        data.float32(debug='action_search_wait_time')
        data.int32(debug='unknown') # flags? could all be uint8's?
        data.int16(debug='unknown')
        data.int16(debug='unknown')
        data.uint8(debug='unknown')
        data.int16(debug='moving_graphic')
        data.int16(debug='proceeding_graphic')
        data.int16(debug='working_graphic')
        data.int16(debug='carrying_graphic')
        data.int16(debug='resource_gathering_sound')
        data.int16(debug='resource_deposit_sound')


def read_base_combat_unit_props(data):
    # base combat unit props
    data.mark('base combat unit props')
    data.uint8(debug='base_armor')
    num_attacks = data.uint16(debug='num_attacks')
    for i in range(0, num_attacks):
        data.mark('attack')
        data.int16(debug='attack_type')
        data.int16(debug='attack_amt')

    num_armors = data.int8(debug='num_armors')
    data.int8(debug='unknown') # 0 ?
    for i in range(0, num_armors): # Ordering is very speculative
        data.mark('armor')
        data.int16(debug='armor_type')
        data.int16(debug='armor_amt')

    data.int16(debug='defense_terrain_bonus')
    data.float32(debug='weapon_range_max')
    data.float32(debug='blast_width')
    data.float32(debug='reload_time')  # 'attack speed'
    data.int16(debug='projectile_unit')
    data.int16(debug='base_hit_chance')
    data.uint8(debug='break_off_combat')
    data.int16(debug='frame_delay')
    data.float32(debug='graphic_displacement1')
    data.float32(debug='graphic_displacement2')
    data.float32(debug='graphic_displacement3')
    data.uint8(debug='blast_attack_level')
    data.float32(debug='weapon_range_min')
    # Skipped missed missile spread
    data.uint16(debug='attack_graphic')
    data.uint16(debug='displayed_armor')
    data.uint16(debug='displayed_attack')
    data.float32(debug='displayed_range')
    data.float32(debug='displayed_reload_time')


def read_combat_unit_props(data):
    # combat unit props
    data.mark('combat unit props')
    for i in range(0, 3):
        data.int16(debug='resource')
        data.int16(debug='cost')
        data.uint8(debug='deduct')
        data.uint8(debug='padding')

    data.uint16(debug='train_time')
    data.int16(debug='create_at_building')
    data.uint8(debug='create_button')
    data.uint8(debug='displayed_pierce_armor')
    data.mark("end of combat unit")
    # skipped a bunch of fields here


def read_building_unit_props(data):
    # building props - probably starts with construction sprite
    data.uint16(debug='construction_sprite')
    data.int16(debug='unknown') # 0
    data.int16(debug='unknown') # 0
    data.uint8(debug='unknown') # 1
    data.int16(debug='stack_unit')
    data.int16(debug='foundation_terrain') # 8
    data.int16(debug='unknown') # -1 possible default task (one other candidate)
    data.int16(debug='initiates_technology') # 72
    data.int16(debug='unknown')


def read_combat_unit(data):
    """ ENTIRELY GUESSWORK """
    base_props = read_base_unit_props(data)
    animated_props = read_animated_unit_props(data)
    moving_unit_props = read_moving_unit_props(data)
    action_unit_props = read_action_unit_props(data)
    base_combat_unit_props = read_base_combat_unit_props(data)
    combat_unit_props = read_combat_unit_props(data)
    data.int8(debug='unknown') # 0?


def read_building_unit(data: ScnDataReader):
    base_props = read_base_unit_props(data)
    animated_props = read_animated_unit_props(data)
    moving_unit_props = read_moving_unit_props(data)
    action_unit_props = read_action_unit_props(data)
    base_combat_unit_props = read_base_combat_unit_props(data)
    combat_unit_props = read_combat_unit_props(data)
    building_unit_props = read_building_unit_props(data)


def read_missile_unit(data: ScnDataReader):
    base_props = read_base_unit_props(data)
    animated_props = read_animated_unit_props(data)
    moving_unit_props = read_moving_unit_props(data)
    action_unit_props = read_action_unit_props(data)
    base_combat_unit_props = read_base_combat_unit_props(data)
    data.int8(debug='unknown')
    data.int32(debug='unknown')
    data.float32(debug='unknown')


def read_decorative_unit(data: ScnDataReader):
    base_props = read_base_unit_props(data)


def read_moving_unit(data: ScnDataReader):
    base_props = read_base_unit_props(data)
    animated_props = read_animated_unit_props(data)
    moving_unit_props = read_moving_unit_props(data)


def read_animated_unit(data: ScnDataReader):
    base_props = read_base_unit_props(data)
    animated_props = read_animated_unit_props(data)


def read_tree(data):
    base_props = read_base_unit_props(data)


def read_action_unit(data):
    base_props = read_base_unit_props(data)
    animated_props = read_animated_unit_props(data)
    moving_unit_props = read_moving_unit_props(data)
    action_unit_props = read_action_unit_props(data)


def read_doppleganger_unit(data):
    base_props = read_base_unit_props(data)
    animated_props = read_animated_unit_props(data)


def read_unit(data: ScnDataReader):
    # next data structure to read depends on the unit type!
    unit_type = data.uint8(debug='unit type'.format())
    if unit_type == 10:  # base
        read_decorative_unit(data)
    elif unit_type == 15:  # tree
        raise Exception("Not implemented")
    elif unit_type == 20:  # animated
        read_animated_unit(data)
    elif unit_type == 25:  # doppleganger
        read_doppleganger_unit(data)
    elif unit_type == 30:  # moving
        read_moving_unit(data)
    elif unit_type == 40:  # action
        read_action_unit(data)
    elif unit_type == 50:  # base
        raise Exception("Not implemented")
    elif unit_type == 60:  # missile
        read_missile_unit(data)
    elif unit_type == 70:
        read_combat_unit(data)
    elif unit_type == 80:
        read_building_unit(data)
    elif unit_type == 90:
        read_tree(data)
    else:
        raise Exception("Dont know how to read unit type {}".format(unit_type))


def debug_count_until(byte: int, data: ScnDataReader):
    for i in range(0, 500):
        if data.uint8() == byte:
            print("Need to skip {} bytes".format(i))
            return
    logging.info("Value not found")
    exit(1)
