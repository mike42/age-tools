import logging

from libage.data import game_data

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    data_file = game_data.load("Empires.dat")
