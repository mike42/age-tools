#!/usr/bin/env python3
import logging
from dataclasses import dataclass
from typing import List

from libage.scenario import scn_unknown_data_structure
from libage.scenario.data import ScnDataReader
from libage.scenario.experimental_de_data import experimental_parse_de_scenario
from libage.scenario.map import read_map, ScnMap
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


def reader_for(file_name):
    if not (file_name.lower().endswith(".scn") or file_name.lower().endswith(".scx") or file_name.lower().endswith(".aoescn")):
        raise Exception("Scenario file must end with .scn, .scx or .aoescn")
    with open(file_name, 'rb') as f:
        # Read entire file
        data = ScnDataReader(f.read())
    return data


def load(file_name: str) -> ScenarioFile:
    data = reader_for(file_name)
    header = ScnHeader.read(data)
    if header.file_version > 3:
        logging.warning("AOE DE Scenarios are not supported")
        experimental_parse_de_scenario(data, header)
        raise Exception("Cannot read this version of scenario files")
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

    scn_unknown_data_structure.skip(data)
    data.done()
    return ScenarioFile(
        header,
        next_object_id,
        tribe_scen,
        map_scen,
        world_players,
        scenario_objects
    )


def decompress(file_name: str, new_file_name: str):
    data = reader_for(file_name)
    header = ScnHeader.read(data)
    with open(new_file_name, 'wb') as f:
        f.write(data.read())
