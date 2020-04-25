import logging

from attr import dataclass

from libage.scenario.data import ScnDataReader


@dataclass
class ScnHeader:
    file_version: bytes
    header_version: float
    timestamp: int
    description: str
    has_singleplayer_victory_condition: bool
    player_count: int

    @staticmethod
    def read(data: ScnDataReader):
        # Load header
        file_version = data.string_fixed(size=4)
        data.mark(name='SCN header', limit=data.uint32())
        scenario_header = ScnHeader(
            file_version=file_version,
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
