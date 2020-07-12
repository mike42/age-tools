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
        header_size = data.uint32();
        data.mark(name='SCN header', limit=header_size)  # header size
        header_version = data.uint32(debug='header_version')

        if header_version >= 3:
            # DE scenario a bit different
            timestamp = data.uint32(debug='Timestamp maybe')
            string_marker = data.uint16(debug='string_marker')  # always 2656
            description = data.string16(debug='description')
            # Data sometimes here sometimes not. Need to check remaining bytes in header size to see if we can read it.
            if header_size - data.bytes_read_since_mark >= 8:
                # might not account for all possibilities for these fields
                has_single_player_victory_condition = data.boolean32()
                player_count = data.uint32()
            else:
                has_single_player_victory_condition = False
                player_count = -1
            scenario_header = ScnHeader(
                file_version=file_version_float,
                header_version=header_version,
                timestamp=timestamp,
                description=description,
                has_singleplayer_victory_condition=has_single_player_victory_condition,
                player_count=player_count
            )
        else:
            timestamp = data.uint32(debug='timestamp')
            scenario_header = ScnHeader(
                file_version=file_version_float,
                header_version=header_version,
                timestamp=timestamp,
                description=data.string32(),
                has_singleplayer_victory_condition=data.boolean32(),
                player_count=data.uint32()
            )
        logging.debug(scenario_header)
        data.unmark()
        data.decompress()

        return scenario_header
