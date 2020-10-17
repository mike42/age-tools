import pytest

from libage.scenario import scenario


def test_create_small(tmpdir):
    outfile = tmpdir.join('foo.scn')
    with pytest.raises(Exception):
        scn = scenario.create(size=20)
    # scn.write(outfile)
