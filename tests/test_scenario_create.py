import pytest

from libage.constants.versions import AgeVersion
from libage.scenario import scenario


def test_create_empty_aoe1(tmpdir):
    # Create & write a scenario
    outfile = str(tmpdir.join('foo.scn'))
    scn_created = scenario.create(size=20, version=AgeVersion.AOE1)
    scenario.save(scn_created, outfile)
    # Read it back..
    scn_loaded = scenario.load(outfile)
    assert scn_loaded.map_scen.width == 20
    assert scn_loaded.map_scen.height == 20


def test_create_empty_aoe1_ror(tmpdir):
    # Create & write a scenario
    outfile = str(tmpdir.join('foo.scx'))
    scn_created = scenario.create(size=20, version=AgeVersion.AOE1_ROR)
    scenario.save(scn_created, outfile)
    # Read it back..
    scn_loaded = scenario.load(outfile)
    assert scn_loaded.map_scen.width == 20
    assert scn_loaded.map_scen.height == 20


@pytest.mark.skip(reason="DE write not supported")
def test_create_empty_aoe1_de(tmpdir):
    # Create & write a scenario
    outfile = str(tmpdir.join('foo.aoescn'))
    scn_created = scenario.create(size=20, version=AgeVersion.AOE1_ROR)
    scenario.save(scn_created, outfile)
    # Read it back..
    scn_loaded = scenario.load(outfile)
    assert scn_loaded.map_scen.width is 20
    assert scn_loaded.map_scen.height is 20

