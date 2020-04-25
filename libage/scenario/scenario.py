#!/usr/bin/env python3
import logging
from dataclasses import dataclass

from libage.scenario.data import ScnDataReader
from libage.scenario.map import read_map
from libage.scenario.scn_header import ScnHeader


@dataclass
class ScnPlayerBaseProperties:
    active: int
    player_type: int
    civilization: int
    posture: int

    @staticmethod
    def read(data: ScnDataReader):
        return ScnPlayerBaseProperties(
            data.uint32(),
            data.uint32(),
            data.uint32(),
            data.uint32()
        )


@dataclass
class ScnPlayerStartResources:
    wood: int
    gold: int
    food: int
    stone: int
    ore: int
    goods: int
    color: int

    @staticmethod
    def read(data: ScnDataReader, version: float):
        return ScnPlayerStartResources(
            wood=data.uint32(),
            gold=data.uint32(),
            food=data.uint32(),
            stone=data.uint32(),
            ore=data.uint32() if version >= 1.17 else 0,
            goods=data.uint32() if version >= 1.17 else 0,
            color=data.uint32() if version >= 1.24 else 0,
        )


@dataclass
class ScnEngineProperties:
    rge_version: float

    @staticmethod
    def read(data: ScnDataReader, version: float):
        pass


def read_rge_scen(data):
    version = data.float32()
    if version > 1.13:
        for i in range(0, 16):
            # skip past player names
            data.string_fixed(size=256)

    if version > 1.16:
        raise Exception("Not implemented: player string table not understood")

    if version > 1.13:
        for i in range(0, 16):
            player_base = ScnPlayerBaseProperties.read(data)
            logging.debug(player_base)

    if version > 1.07:
        is_conquest = data.boolean8()

    # Something to do with timelines?
    check1 = data.uint16()
    check2 = data.uint16()
    check3 = data.float32()
    if check1 != 0 or check2 != 0 or check3 < -1 or check3 > 1:
        raise Exception("Unexpected values in scenario data, giving up")

    filename = data.string16(debug='filename')

    if version > 1.16:
        raise Exception("Not implemented: scenario instruction string table not understood")

    if version > 1.22:
        raise Exception("Not implemented: scout string table not understood")

    description = data.string16(debug='description')

    if version >= 1.11:
        hints_message = data.string16(debug='hints_message')
        win_message = data.string16(debug='win_message')
        loss_message = data.string16(debug='loss_message')
        history_message = data.string16(debug='history_message')

    if version > 1.22:
        raise Exception("Not implemented: scout data not understood")

    pregame_cinematic = data.string16(debug='pregame_cinematic')
    victory_cinematic = data.string16(debug='victory_cinematic')
    loss_cinematic = data.string16(debug='loss_cinematic')

    if version >= 1.09:
        mission_bmp = data.string16()
        logging.debug("mission_bmp='%s'", mission_bmp)

    if version >= 1.10:
        mission_image = data.uint32()
        width = data.uint32()
        height = data.uint32()
        orientation = data.uint16()
        if width > 0 or height > 0:
            raise Exception("Mission BMP data not understood")

    for i in range(0, 16):
        logging.debug("Player %d build list %s", i, data.string16())

    for i in range(0, 16):
        logging.debug("Player %d city plan %s", i, data.string16())

    if version >= 1.08:
        for i in range(0, 16):
            logging.debug("Player %d personality %s", i, data.string16())

    for i in range(0, 16):
        """ Embedded files """
        build_list_length = data.uint32()
        city_plan_length = data.uint32()
        ai_rules_length = data.uint32() if version >= 1.08 else 0
        data.read(build_list_length)
        data.read(city_plan_length)
        data.read(ai_rules_length)

    if version >= 1.20:
        raise Exception("Not implemented: AI rules not understood")

    if version >= 1.02:
        check4 = data.int32()
        if check4 != -99:
            raise Exception("Check value did not match in scenario data, giving up")

    rge_scen = ScnEngineProperties(
        version
    )
    logging.debug(rge_scen)
    return rge_scen


@dataclass
class ScnGameProperties:
    base: ScnEngineProperties

    @staticmethod
    def read(data: ScnDataReader):
        base = read_rge_scen(data)
        version = base.rge_version
        if version <= 1.13:
            for i in range(0, 16):
                # skip past player names
                data.string_fixed(size=256)
            raise Exception("Not implemented: Don't know how to read player base properties from <1.13 file")
        else:
            for i in range(0, 16):
                res = ScnPlayerStartResources.read(data, version)
                print(res)

        if version >= 1.02:
            check5 = data.int32()
            if check5 != -99:
                raise Exception("Check value did not match in scenario data, giving up")

        victory_conquest = data.uint32()
        victory_ruins = data.uint32()
        victory_artifacts = data.uint32()
        victory_discoveries = data.uint32()
        victory_exploration = data.uint32()
        victory_gold = data.uint32()
        victory_all_flag = data.boolean32()

        if version >= 1.13:
            mp_victory_type = data.uint32()
            victory_score = data.uint32()
            victory_time = data.uint32()

        for i in range(0, 16):
            for j in range(0, 16):
                stance = data.uint32()
                logging.debug("Diplomacy from=%d to=%d stance=%d", i, j, stance)

        # 12 victory conditions for each player
        for i in range(0, 16):
            for j in range(0, 12):
                # TODO read these ???
                data.read(60)

        if version >= 1.02:
            check5 = data.int32()
            if check5 != -99:
                raise Exception("Check value did not match in scenario data, giving up")

        # Allied victory
        for i in range(0, 16):
            data.uint32()

        if version >= 1.24:
            raise Exception("Not implemented: Don't know how to read team information from >=1.24 file")

        if version >= 1.18:
            # Also has disabled units and building, where are they in older versions?
            raise Exception("Not implemented: Don't know how to read tech tree from >=1.18 file")
        elif version > 1.03:
            for i in range(0, 16):
                for j in range(0, 20):
                    disabled_tech_id = data.uint32()
                    logging.debug("Disabled tech player %d, position %d: %d", i, j, disabled_tech_id)

        if version > 1.04:
            data.uint32()  # No idea

        if version >= 1.12:
            data.uint32()  # No idea
            full_tech_tree = data.boolean32()

        if version > 1.05:
            for i in range(0, 16):
                player_start_age = data.uint32()

        if version >= 1.02:
            check6 = data.int32()
            if check6 != -99:
                raise Exception("Check value did not match in scenario data, giving up")

        if version >= 1.19:
            # 'view'??
            data.uint32()
            data.uint32()

        if version >= 1.21:
            raise Exception("Not implemented: Don't know how to read map type from >=1.21 file")

        if version >= 1.21:
            raise Exception("Not implemented: Don't know how to read base priorities from >=1.21 file")

        game_properties = ScnGameProperties(
            base
        )
        logging.debug(game_properties)
        return game_properties


@dataclass()
class WorldPlayer:
    food: float
    wood: float
    gold: float
    stone: float
    ore: float
    goods: float
    population: float

    @staticmethod
    def read(data: ScnDataReader, player_version: float):
        return WorldPlayer(
            data.float32() if player_version > 1.06 else 200.0,
            data.float32() if player_version > 1.06 else 200.0,
            data.float32() if player_version > 1.06 else 50.0,
            data.float32() if player_version > 1.06 else 100.0,
            data.float32() if player_version > 1.12 else 100.0,
            data.float32() if player_version > 1.12 else 0.0,
            data.float32() if player_version > 1.14 else 75.0,
        )


@dataclass()
class ScenarioObject:
    position: tuple
    id: int
    type_id: int
    state: int
    angle: float
    frame: int
    garrisoned_in:  int

    @staticmethod
    def read(data: ScnDataReader, file_version: str):
        file_version_flt = float(file_version)
        return ScenarioObject(
            (data.float32(), data.float32(), data.float32()),
            data.uint32(),
            data.uint16(),
            data.uint8(),
            data.float32(),
            # Not used in AOE1
            -1 if file_version_flt < 1.15 else data.uint16(),
            -1 if file_version_flt < 1.13 else data.uint32()
        )


def load(file_name: str):
    if not (file_name.endswith(".scn") or file_name.endswith(".scx")):
        raise Exception("Scenario file must end with .scn or .scx")
    with open(file_name, 'rb') as f:
        # Read entire file
        data = ScnDataReader(f.read())
    header = ScnHeader.read(data)
    next_object_id = data.uint32()
    tribe_scen = ScnGameProperties.read(data)
    map_scen = read_map(data)
    num_players = data.uint32()
    player_version = 1.12  # TODO map from header version.
    world_players = []
    for i in range(1, num_players):
        world_player = WorldPlayer.read(data, player_version)
        world_players.append(world_player)

    scenario_objects = []
    for i in range(0, num_players):
        object_count = data.uint32()
        player_objects = []
        for j in range(0, object_count):
            obj = ScenarioObject.read(data, header.file_version)
            player_objects.append(obj)
        scenario_objects.append(player_objects)

    return {
        'filename': file_name,
        'header': header,
        'next_object_id': next_object_id,
        'tribe_scen': tribe_scen,
        'map_scen': map_scen,
        'world_players': world_players,
        'objects': scenario_objects
    }
