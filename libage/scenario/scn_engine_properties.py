import logging
from dataclasses import dataclass

from libage.scenario.data import ScnDataReader
from libage.scenario.scn_player_base_properties import ScnPlayerBaseProperties


@dataclass
class ScnEngineProperties:
    rge_version: float

    @staticmethod
    def read(data: ScnDataReader):
        version = data.float32(debug='version')
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