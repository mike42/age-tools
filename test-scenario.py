#!/usr/bin/env python

# Render mini-map from AOE1 scenario file

import logging

import sys

from libage.scenario import scenario, minimap

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    for file in sys.argv[1:]:
        scenario1 = scenario.load(file)
        im = minimap.draw(scenario1)
        im.save(file + ".png")
