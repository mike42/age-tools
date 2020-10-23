import logging
from dataclasses import dataclass

from libage.scenario.data import ScnDataReader, ScnDataWriter
from libage.scenario.scn_player_base_properties import ScnPlayerBaseProperties


@dataclass
class ScnEngineProperties:
    rge_version: float

    @staticmethod
    def read_classic(data: ScnDataReader):
        # TODO actually store this stuff
        version = data.float32(debug='version')
        if version > 1.13:
            for i in range(0, 16):
                # skip past player names
                player_name = data.string_fixed(size=256)

        if version > 1.16:
            raise Exception("Not implemented: player string table not understood")

        if version > 1.13:
            for i in range(0, 16):
                player_base = ScnPlayerBaseProperties.read(data)
                logging.debug(player_base)

        is_conquest = False
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

    @staticmethod
    def read_de(data: ScnDataReader):
        version = data.float32(debug='version')

        for i in range(0, 16):
            data.uint16(debug='some number here')  # 2656
            data.string16(debug='player tribe name')

        if version >= 3.13:
            # These 16 bytes are not present in some DE scenarios bundled w/ the game, labelled version 3.125.
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

        if version < 3.13:
            data.mark('extra data observed in 3.125 version')
            for i in range(0, 32):
                data.int32(debug='unknown value 1 {}'.format(i))  # 500
            for i in range(0, 32):
                data.int32(debug='unknown value 2 {}'.format(i))  # 0

        check2 = data.int32(debug='check value 2')
        if check2 != -99:
            raise Exception("Check value did not match in scenario data, giving up")

        rge_scen = ScnEngineProperties(
            version
        )
        logging.debug(rge_scen)
        return rge_scen

    def write_classic(self, data: ScnDataWriter):
        # TODO actually use stored values for this stuff
        data.float32(self.rge_version)
        if self.rge_version > 1.13:
            for i in range(0, 16):
                # player names
                data.string_fixed('Player name {}'.format(i), size=256)

        if self.rge_version > 1.16:
            raise Exception("Not implemented: player string table not understood")

        if self.rge_version > 1.13:
            for i in range(0, 16):
                player_base = ScnPlayerBaseProperties(
                    active=1,
                    player_type=0,
                    civilization=0,
                    posture=0)
                player_base.write(data)

        if self.rge_version > 1.07:
            is_conquest = False
            data.boolean8(is_conquest)

        # Some check values?
        data.uint16(0)
        data.uint16(0)
        data.float32(0)

        filename = 'example.scn'
        data.string16(filename)

        if self.rge_version > 1.16:
             raise Exception("Not implemented: scenario instruction string table not understood")

        if self.rge_version > 1.22:
             raise Exception("Not implemented: scout string table not understood")

        description = "description"
        data.string16(description)

        if self.rge_version >= 1.11:
            hints_message = ""
            data.string16(hints_message)
            win_message = ""
            data.string16(win_message)
            loss_message = ""
            data.string16(loss_message)
            history_message = ""
            data.string16(history_message)

        if self.rge_version > 1.22:
            raise Exception("Not implemented: scout data not understood")

        pregame_cinematic = ""
        data.string16(pregame_cinematic)
        victory_cinematic = ""
        data.string16(victory_cinematic)
        loss_cinematic = ""
        data.string16(loss_cinematic)

        if self.rge_version >= 1.09:
            mission_bmp = ""
            data.string16(mission_bmp)

        if self.rge_version >= 1.10:
             mission_image = 0
             data.uint32(mission_image)
             width = 0
             data.uint32(width)
             height = 0
             data.uint32(height)
             orientation = 0
             data.uint16(orientation)

        for i in range(0, 16):
            player_build_list = ""
            data.string16(player_build_list)

        for i in range(0, 16):
            player_city_plan = ""
            data.string16(player_city_plan)

        if self.rge_version >= 1.08:
            for i in range(0, 16):
                player_personality = ""
                data.string16(player_personality)

        for i in range(0, 16):
            """ Embedded files """
            build_list_length = 0
            data.uint32(build_list_length)
            city_plan_length = 0
            data.uint32(city_plan_length)
            if self.rge_version >= 1.08:
                ai_rules_length = 0
                data.uint32(ai_rules_length)
            else:
                data.uint32(0)
            # Would write build_list, city plan, AI rules if lens weren't 0

        if self.rge_version >= 1.20:
            raise Exception("Not implemented: AI rules not understood")

        if self.rge_version >= 1.02:
            data.int32(-99)  # Check value
