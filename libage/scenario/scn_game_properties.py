import logging
from dataclasses import dataclass

from libage.scenario.data import ScnDataReader
from libage.scenario.scn_engine_properties import ScnEngineProperties
from libage.scenario.scn_player_start_resources import ScnPlayerStartResources


@dataclass
class ScnGameProperties:
    base: ScnEngineProperties

    @staticmethod
    def read_classic(data: ScnDataReader):
        base = ScnEngineProperties.read_classic(data)
        version = base.rge_version
        if version <= 1.13:
            for i in range(0, 16):
                # skip past player names
                data.string_fixed(size=256)
            raise Exception("Not implemented: Don't know how to read player base properties from <1.13 file")
        else:
            for i in range(0, 16):
                # Ignoring at the moment
                res = ScnPlayerStartResources.read(data, version)

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

    @staticmethod
    def read_de(data: ScnDataReader):
        base = ScnEngineProperties.read_de(data)

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

        game_properties = ScnGameProperties(
            base
        )
        logging.debug(game_properties)
        return game_properties
