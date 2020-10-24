import os

from libage.scenario import scenario

TEST_FILE_DIR = os.path.join(os.path.dirname(__file__), '..', 'test_files')


def test_scenario_aoe1():
    path = os.path.join(TEST_FILE_DIR, 'aoe1_small_islands_random.scn')
    scn = scenario.load(path)
    assert 1.11 == scn.header.file_version
    assert 2 == scn.header.header_version
    assert 2 == scn.header.player_count
    assert 200 == scn.map_scen.width
    assert 200 == scn.map_scen.height


def test_scenario_ror():
    path = os.path.join(TEST_FILE_DIR, 'aoe1_ror_small_islands_random.scx')
    scn = scenario.load(path)
    assert 1.11 == scn.header.file_version
    assert 2 == scn.header.header_version
    assert 2 == scn.header.player_count
    assert 120 == scn.map_scen.width
    assert 120 == scn.map_scen.height


def test_scenario_de():
    path = os.path.join(TEST_FILE_DIR, 'aoe1_de_small_islands_random.aoescn')
    scn = scenario.load(path)
    assert 3.13 == scn.header.file_version
    assert 3 == scn.header.header_version
    assert -1 == scn.header.player_count
    assert 72 == scn.map_scen.width
    assert 72 == scn.map_scen.height


def test_blank_scenario_ror():
    path = os.path.join(TEST_FILE_DIR, 'blank_scenario_ror.scx')
    scn = scenario.load(path)
    assert 1.11 == scn.header.file_version
    assert 2 == scn.header.header_version
    assert 2 == scn.header.player_count
    assert 144 == scn.map_scen.width
    assert 144 == scn.map_scen.height
