import inspect
import os
import unittest

from libage.rms import rms

TEST_FILE_DIR = os.path.join(os.path.dirname(__file__), '..', 'test_files')


class TestRmsFiles(unittest.TestCase):
    def test_sections_only(self):
        sections_only = inspect.cleandoc("""
            <PLAYER_SETUP>
            <LAND_GENERATION>
            <ELEVATION_GENERATION>
            <CLIFF_GENERATION>
            <TERRAIN_GENERATION>
            <CONNECTION_GENERATION>
            <OBJECTS_GENERATION>
            """)
        f = rms.read_str(sections_only)
        self.assertEqual(7, len(f))   # The 7 named sections

    def test_commented_block_close(self):
        # Observed in mediterranean RMS, so I guess this is valid
        test_str = inspect.cleandoc("""
            <CONNECTION_GENERATION>
            create_connect_all_players_land
            {
            /*  replace_terrain GRASS         DESERT
            replace_terrain WATER         SHALLOW
            } */
            """)
        f = rms.read_str(test_str)
        self.assertEqual(1, len(f))

    def test_random_probability(self):
        # Observed rnd(x,y) in Serengeti RMS
        test_str = inspect.cleandoc("""
            create_terrain SOMETHING
            {
            base_terrain                   SOMETHING_ELSE
            land_percent                   rnd(123,456)
            }
            """)
        f = rms.read_str(test_str)
        self.assertEqual("create_terrain", f[0].name)
        self.assertEqual("land_percent", f[1][1].name)
        self.assertEqual("123", f[1][1][0][0])
        self.assertEqual("456", f[1][1][0][1])
