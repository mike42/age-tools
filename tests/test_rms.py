import inspect
import os
import unittest

from pypeg2.xmlast import thing2xml

from libage.rms import rms

TEST_FILE_DIR = os.path.join(os.path.dirname(__file__), '..')


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
        self.assertEqual(7, len(f))
