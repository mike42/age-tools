import logging
import sys
from pathlib import Path

from libage.slp import slp, palette

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    pal = palette.load('50500.bin')
    for file in sys.argv[1:]:
        sprite = slp.load(file)
        file_base = Path(file).stem
        for i in range(0, len(sprite.frames)):
            im = slp.draw(sprite, pal, player_id=1, frame_id=i)
            im.save("{}_{:03d}.png".format(file_base, i))
