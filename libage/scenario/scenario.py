#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List

from libage.constants.versions import AgeVersion
from libage.scenario import scn_unknown_data_structure
from libage.scenario.data import ScnDataReader, ScnDataWriter
from libage.scenario.map import ScnMap, ScnMapTile
from libage.scenario.scn_engine_properties import ScnEngineProperties
from libage.scenario.scn_game_properties import ScnGameProperties
from libage.scenario.scn_header import ScnHeader
from libage.scenario.scn_object import ScenarioObject
from libage.scenario.scn_world_player import WorldPlayer


@dataclass
class ScenarioFile:
    header: ScnHeader
    next_object_id: int
    tribe_scen: ScnGameProperties
    map_scen: ScnMap
    world_players: List[WorldPlayer]
    objects: List[List[ScenarioObject]]

    def write(self, data: ScnDataWriter):
        self.header.write(data)
        data.uint32(self.next_object_id)
        if self.header.header_version >= 3:
            # Assume DE scenario
            raise Exception("Not implemented")
        else:
            self.tribe_scen.write_classic(data)
            self.map_scen.write(data)
            num_players = len(self.world_players)
            data.uint32(num_players)
            player_version = 1.12  # TODO map from header version.
            for player in self.world_players:
                player.write_classic(data, player_version)
            for player_objects in self.objects:
                data.uint32(len(player_objects))
                for player_object in player_objects:
                    player_object.write_classic(data, self.header.file_version)
            # scn_unknown_data_structure.fill(data)


def _reader_for(file_name):
    if not (file_name.lower().endswith(".scn") or file_name.lower().endswith(".scx") or file_name.lower().endswith(
            ".aoescn")):
        raise Exception("Scenario file must end with .scn, .scx or .aoescn")
    with open(file_name, 'rb') as f:
        # Read entire file
        data = ScnDataReader(f.read())
    return data


def load(file_name: str) -> ScenarioFile:
    data = _reader_for(file_name)
    header = ScnHeader.read(data)
    next_object_id = data.uint32()
    if header.header_version >= 3:
        # Assume DE scenario
        tribe_scen = ScnGameProperties.read_de(data)
        map_scen = ScnMap.read(data)

        num_players = data.uint32(debug='num_players')
        world_players = []
        for i in range(1, num_players):
            world_player = WorldPlayer.read_de(data, tribe_scen.base.rge_version)
            world_players.append(world_player)

        scenario_objects = []
        for i in range(0, num_players):
            object_count = data.uint32(debug='object count player {}'.format(i))
            player_objects = []
            for j in range(0, object_count):
                obj = ScenarioObject.read_de(data)
                player_objects.append(obj)
            scenario_objects.append(player_objects)

        scn_unknown_data_structure.skip(data)

        return ScenarioFile(
            header,
            next_object_id,
            tribe_scen,
            map_scen,
            world_players,
            scenario_objects
        )
    else:
        # Assume classic scenario
        tribe_scen = ScnGameProperties.read_classic(data)
        map_scen = ScnMap.read(data)

        num_players = data.uint32()
        player_version = 1.12  # TODO map from header version.
        world_players = []
        for i in range(0, num_players):
            world_player = WorldPlayer.read_classic(data, player_version)
            world_players.append(world_player)

        scenario_objects = []
        for i in range(0, num_players):
            object_count = data.uint32()
            player_objects = []
            for j in range(0, object_count):
                obj = ScenarioObject.read_classic(data, header.file_version)
                player_objects.append(obj)
            scenario_objects.append(player_objects)

        scn_unknown_data_structure.skip(data)

        return ScenarioFile(
            header,
            next_object_id,
            tribe_scen,
            map_scen,
            world_players,
            scenario_objects
        )


def save(scenario: ScenarioFile, file_name: str):
    data = ScnDataWriter()
    scenario.write(data)
    result_bytes = data.done()
    with open(file_name, 'wb') as f:
        f.write(result_bytes)


def decompress(file_name: str, new_file_name: str):
    data = _reader_for(file_name)
    header = ScnHeader.read(data)
    with open(new_file_name, 'wb') as f:
        f.write(data.read())


def create(size: int, version: AgeVersion = AgeVersion.AOE1, player_count=2) -> ScenarioFile:
    """
    Create a blank scenario file
    """
    # Version-specific header info
    if version is AgeVersion.AOE1:
        header = ScnHeader(
            file_version=1.11,
            header_version=2,
            timestamp=876873600,
            description='',
            has_singleplayer_victory_condition=False,
            player_count=player_count
        )
        tribe_scen = ScnGameProperties(
            base=ScnEngineProperties(rge_version=1.149999976158142)
        )
    elif version is AgeVersion.AOE1_ROR:
        header = ScnHeader(
            file_version=1.11,
            header_version=2,
            timestamp=909792000,
            description='',
            has_singleplayer_victory_condition=False,
            player_count=player_count
        )
        tribe_scen = ScnGameProperties(
            base=ScnEngineProperties(rge_version=1.149999976158142)
        )
    elif version is AgeVersion.AOE1_DE:
        header = ScnHeader(
            file_version=3.13,
            header_version=3,
            timestamp=1518912000,
            description='',
            has_singleplayer_victory_condition=False,
            player_count=-1
        )
        tribe_scen = ScnGameProperties(base=ScnEngineProperties(rge_version=3.130000114440918))
    else:
        raise Exception("Unsupported version")
    # Tiles and player info
    map_scen = ScnMap(
        width=size,
        height=size,
        tiles=[ScnMapTile(22, 0, 0) for _ in range(0, size * size)]
    )
    world_players = [WorldPlayer(food=200.0, wood=200.0, gold=0.0, stone=150.0, ore=100.0, goods=0.0, population=75.0)
                     for _ in range(0, 8)]
    base_file = ScenarioFile(
        header=header,
        tribe_scen=tribe_scen,
        map_scen=map_scen,
        world_players=world_players,
        objects=[[] for _ in range(0, 8)],
        next_object_id=1
    )
    return base_file
