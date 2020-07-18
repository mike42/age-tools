import os
import unittest

from libage.scenario import scenario

TEST_FILE_DIR = os.path.join(os.path.dirname(__file__), '..', 'test_files')


class TestScenarioFiles(unittest.TestCase):
    def test_scenario_aoe1(self):
        path = os.path.join(TEST_FILE_DIR, 'aoe1_small_islands_random.scn')
        scn = scenario.load(path)
        self.assertEqual(1.11, scn.header.file_version)
        self.assertEqual(2, scn.header.header_version)
        self.assertEqual(2, scn.header.player_count)
        self.assertEqual(200, scn.map_scen.width)
        self.assertEqual(200, scn.map_scen.height)

    def test_scenario_ror(self):
        path = os.path.join(TEST_FILE_DIR, 'aoe1_ror_small_islands_random.scx')
        scn = scenario.load(path)
        self.assertEqual(1.11, scn.header.file_version)
        self.assertEqual(2, scn.header.header_version)
        self.assertEqual(2, scn.header.player_count)
        self.assertEqual(120, scn.map_scen.width)
        self.assertEqual(120, scn.map_scen.height)

    def test_scenario_de(self):
        path = os.path.join(TEST_FILE_DIR, 'aoe1_de_small_islands_random.aoescn')
        scn = scenario.load(path)
        self.assertEqual(3.13, scn.header.file_version)
        self.assertEqual(3, scn.header.header_version)
        self.assertEqual(-1, scn.header.player_count)
        self.assertEqual(72, scn.map_scen.width)
        self.assertEqual(72, scn.map_scen.height)


if __name__ == '__main__':
    unittest.main()
