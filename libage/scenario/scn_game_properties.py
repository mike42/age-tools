import logging
from dataclasses import dataclass

from libage.scenario.data import ScnDataReader, ScnDataWriter
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
                player_name = data.string_fixed(size=256)
            raise Exception("Not implemented: Don't know how to read player base properties from <1.13 file")
        else:
            player_start_resources = []
            for i in range(0, 16):
                # Ignoring at the moment
                this_player_start_resources = ScnPlayerStartResources.read(data, version)
                player_start_resources.append(this_player_start_resources)

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
                individual_victory_blob = data.read(60)

        if version >= 1.02:
            check5 = data.int32()
            if check5 != -99:
                raise Exception("Check value did not match in scenario data, giving up")

        # Allied victory
        for i in range(0, 16):
            allied_victory = data.uint32()

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

        check3 = data.int32(debug='check value 3')
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

        for j in range(0, 16):  # maybe ?
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

    def write_classic(self, data: ScnDataWriter):
        self.base.write_classic(data)
        version = self.base.rge_version
        if version <= 1.13:
            for i in range(0, 16):
                # Not based on real info at the moment
                data.string_fixed('Player name {}'.format(i), size=256)
            raise Exception("Not implemented: Don't know how to read player base properties from <1.13 file")
        else:
            for i in range(0, 16):
                # Not based on real info at the moment
                res = ScnPlayerStartResources(
                    gold=0,
                    food=200,
                    wood=200,
                    stone=150,
                    ore=0,
                    goods=0,
                    color=0,
                )
                res.write(data, version)

        if version >= 1.02:
            data.int32(-99)  # check

        victory_conquest = 1
        data.uint32(victory_conquest)
        victory_ruins = 0
        data.uint32(victory_ruins)
        victory_artifacts = 0
        data.uint32(victory_artifacts)
        victory_discoveries = 0
        data.uint32(victory_discoveries)
        victory_exploration = 0
        data.uint32(victory_exploration)
        victory_gold = 0
        data.uint32(victory_gold)
        victory_all_flag = False
        data.boolean32(victory_all_flag)

        if version >= 1.13:
            mp_victory_type = 0
            data.uint32(mp_victory_type)
            victory_score = 900
            data.uint32(victory_score)
            victory_time = 9000
            data.uint32(victory_time)

        for i in range(0, 16):
            for j in range(0, 16):
                # stance from player i to j
                diplomatic_stance = 3  # 3 is enemy ?
                data.uint32(diplomatic_stance)

        # 12 victory conditions for each player
        for i in range(0, 16):
            for j in range(0, 12):
                # TODO write these ???
                # all 0's on blank map.
                data.string_fixed('', size=60)

        if version >= 1.02:
            data.int32(-99)  # check value

        # Allied victory
        for i in range(0, 16):
            allied_victory = 0
            data.uint32(allied_victory)

        if version >= 1.24:
            raise Exception("Not implemented: Don't know how to read team information from >=1.24 file")

        if version >= 1.18:
            # Also has disabled units and building, where are they in older versions?
            raise Exception("Not implemented: Don't know how to read tech tree from >=1.18 file")
        elif version > 1.03:
            for i in range(0, 16):
                for j in range(0, 20):
                    # disabled tech player i, position j
                    disabled_tech_id = 1
                    data.uint32(disabled_tech_id)

        if version > 1.04:
            data.uint32(0)  # No idea

        if version >= 1.12:
            data.uint32(0)  # No idea
            full_tech_tree = False
            data.boolean32(full_tech_tree)

        if version > 1.05:
            for i in range(0, 16):
                player_start_age = 0
                data.uint32(player_start_age)

        if version >= 1.02:
            data.int32(-99)  # check value

        if version >= 1.19:
            # 'view'??
            data.uint32(0)
            data.uint32(0)

        if version >= 1.21:
            raise Exception("Not implemented: Don't know how to read map type from >=1.21 file")

        if version >= 1.21:
            raise Exception("Not implemented: Don't know how to read base priorities from >=1.21 file")
