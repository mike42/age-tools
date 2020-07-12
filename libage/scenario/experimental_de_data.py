"""
Work in progress: just walk through the fields we know about and do nothing
"""
import logging

from libage.scenario import scn_unknown_data_structure
from libage.scenario.data import ScnDataReader
from libage.scenario.map import read_map
from libage.scenario.scn_header import ScnHeader
from libage.scenario.scn_player_base_properties import ScnPlayerBaseProperties


def experimental_parse_de_scenario(data: ScnDataReader, header: ScnHeader):
    next_object_id = data.uint32()
    version = data.float32(debug='version')

    # rge_scen data
    for i in range(0, 16):
        data.uint16(debug='some number here')  # 2656
        data.string16(debug='player tribe name')

    for i in range(0, 16):
        # Guessing its a string ref, have not checked
        data.int32(debug="unknown_string_ref for player {}".format(i))

    for i in range(0, 16):
        player_base_props = ScnPlayerBaseProperties.read(data)
        logging.debug(player_base_props)

    data.boolean32(debug='conquest maybe')
    data.float32(debug='probable check field')

    data.uint8(debug='unknown field')

    data.uint16(debug='some number here')  # 2656
    data.string16(debug='scenario_name')

    data.uint16(debug='some number here')  # 2656
    data.string16(debug='scenario_instructions')

    data.uint16(debug='some number here')  # 2656
    data.string16(debug='history_string')

    data.uint16(debug='some number here')  # 2656
    data.string16(debug='victory_string')

    data.uint16(debug='some number here')  # 2656
    data.string16(debug='loss_string')

    data.uint16(debug='some number here')  # 2656
    data.string16(debug='history_string')

    data.int32(debug='instructions_string_reference')
    data.uint16(debug='some_number_here')  # 2656
    data.string16(debug='instructions_vox')

    data.int32(debug='hints_string_reference')
    data.uint16(debug='some_number_here')  # 2656
    data.string16(debug='hints_vox')

    data.int32(debug='victory_string_reference')
    data.uint16(debug='some_number_here')  # 2656
    data.string16(debug='victory_vox')

    data.int32(debug='loss_string_reference')
    data.uint16(debug='some_number_here')  # 2656
    data.string16(debug='loss_vox')

    data.int32(debug='history_string_reference')
    data.uint16(debug='some_number_here')  # 2656
    data.string16(debug='history_vox')

    # Not sure if cinematics or per-player personality, AI, city plans etc

    data.uint16(debug='some_number_here')  # 2656
    data.string16(debug='unidentified_string 1')  # ' <None> '

    data.uint16(debug='some_number_here')  # 2656
    data.string16(debug='unidentified_string 2')  # ' <None> '

    data.uint16(debug='some_number_here')  # 2656
    data.string16(debug='unidentified_string 3')  # ' <None> '

    data.uint16(debug='some_number_here')  # 2656
    data.string16(debug='unidentified_string 4')  # ' <None> '

    data.uint32(debug='unidentified number 1')  # 0
    data.uint32(debug='unidentified number 2')  # 0
    data.uint32(debug='unidentified number 3')  # 0
    data.uint16(debug='unidentified number 4')  # 1

    for i in range(0, 16):
        data.string16(debug="ai player {}".format(i))

    for i in range(0, 16):
        data.string16(debug="city plan player {}".format(i))

    for i in range(0, 16):
        data.string16(debug="personality player {}".format(i))

    for i in range(0, 16):
        some_length1 = data.uint32(debug='some length maybe')
        some_length2 = data.uint32(debug='some length maybe')
        some_length3 = data.uint32(debug='some length maybe')
        data.string_fixed(some_length1, debug='some string 1')
        data.string_fixed(some_length2, debug='some string 2')
        data.string_fixed(some_length3, debug='some string 3')

    check1 = data.int32(debug='check value 1')
    if check1 != -99:
        raise Exception("Check value did not match in scenario data, giving up")
    check2 = data.int32(debug='check value 2')
    if check2 != -99:
        raise Exception("Check value did not match in scenario data, giving up")

    # expecting global victory conditions around here somewhere
    for i in range(0, 8):
        data.uint32(debug='unknown value a {}'.format(i))
    data.uint32(debug='unknown value b')  # 900
    data.uint32(debug='unknown value c')  # 9000

    # expecting diplomacy
    for i in range(0, 16):
        for j in range(0, 16):
            val = data.uint32()
            logging.debug("Unknown value from=%d to=%d val=%d", i, j, val)  # lots of '3'.

    # expecting 12 individual victory conditions for each player
    for i in range(0, 16):
        for j in range(0, 12):
            # TODO read these ???
            data.read(60)

    check3 = data.int32(debug='check value 2')
    if check3 != -99:
        raise Exception("Check value did not match in scenario data, giving up")

    # Probably allied victory
    for i in range(0, 16):
        data.uint32(debug='allied victory player {}'.format(i))

    # disabled tech
    for i in range(0, 16):
        for j in range(0, 20):
            disabled_tech_id = data.uint32()
            logging.debug("Disabled tech player %d, position %d: %d", i, j, disabled_tech_id)

    data.uint32(debug='unknown field 1')
    data.uint32(debug='unknown field 2')
    data.uint32(debug='unknown field 3')  # might be full tech tree

    for j in range(0, 16): # maybe ?
        data.uint32(debug='starting age player {}'.format(j))

    check4 = data.int32(debug='check value 2')
    if check4 != -99:
        raise Exception("Check value did not match in scenario data, giving up")

    # view ?
    data.float32()
    data.float32()

    # looks like map goes here
    map_scen = read_map(data)

    num_players = data.uint32()
    for i in range(1, num_players):
        # food stone wood gold
        data.float32(debug='some resource, player {}'.format(i))
        data.float32(debug='some resource, player {}'.format(i))
        data.float32(debug='some resource, player {}'.format(i))
        data.float32(debug='some resource, player {}'.format(i))
        # population
        data.float32(debug='population player {}'.format(i))

    # Walk past objects
    data.mark('objects')
    scenario_objects = []
    for i in range(0, num_players):
        object_count = data.uint32(debug='object count player {}'.format(i))
        player_objects = []
        for j in range(0, object_count):
            position = (data.float32(), data.float32(), data.float32())
            data.uint32()  #  id
            data.uint16()  # type_id
            data.uint8()  # state
            data.float32()  # angle
    scn_unknown_data_structure.skip(data)
    data.done()
