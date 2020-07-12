import logging
from dataclasses import dataclass

from libage.scenario.data import ScnDataReader


@dataclass
class ScnHeader:
    file_version: float
    header_version: float
    timestamp: int
    description: str
    has_singleplayer_victory_condition: bool
    player_count: int

    @staticmethod
    def read(data: ScnDataReader):
        # Load header
        file_version = data.string_fixed(size=4)
        file_version_float = float(file_version)
        data.mark(name='SCN header', limit=data.uint32())  # header size
        if file_version_float > 3:
            # DE scenario a bit different
            unknown_field_1 = data.uint32(debug='unknown_field_1')  # eg. 3
            timestamp = data.uint32(debug='Timestamp maybe')
            unknown_field_2 = data.uint16(debug='unknown_field_2')  # eg. 2656
            description = data.string16(debug='description')
            scenario_header = ScnHeader(
                file_version=file_version_float,
                header_version=0,
                timestamp=timestamp,
                description=description,
                has_singleplayer_victory_condition=False,
                player_count=0
            )
        else:
            scenario_header = ScnHeader(
                file_version=file_version_float,
                header_version=data.uint32(),
                timestamp=data.uint32(),
                description=data.string32(),
                has_singleplayer_victory_condition=data.boolean32(),
                player_count=data.uint32()
            )
        data.unmark()
        logging.debug(scenario_header)
        data.decompress()

        return scenario_header
