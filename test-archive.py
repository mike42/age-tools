import logging
import sys

from libage.archive import archive

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    for file in sys.argv[1:]:
        archive1 = archive.load(file)
        # for file in archive1.files():
        #     print(file.header)
