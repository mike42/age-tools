from libage.scenario.data import ScnDataReader, ScnDataWriter


def skip(data: ScnDataReader):
    # Not sure how to walk through this trailing data yet.
    # Fails on both Multiplayer Border Patrol maps bundled with ROR and DE.
    # This data seems to be either 1320 or 708 bytes long.
    return
    # Some kind of per-player data structure here
    data.uint32(debug="unknown field")  # Only seen 9.
    for i in range(0, 8):
        data.string16(debug='player_name_repeated')
        data.float32(debug='unknown field 1')
        data.float32(debug='unknown field 2')
        data.uint16(debug='unknown field 3')
        data.uint16(debug='unknown field 4')
        data.uint8(debug='unknown field 5')
        data.uint16(debug='unknown field 6')
        for j in range(0, 9):
            data.uint8(debug='unknown field player {} {}'.format(i, j))
        for j in range(0, 9):
            data.uint32(debug='unknown field player {} {}'.format(i, j))
        data.float32(debug="unknown field")  # 1.00
        data.float32(debug="unknown field")  # only seen 0. guess this could be float as well ?
        for j in range(0, 9): # all 0's. guessing it could hold another list of 9 values?
            data.uint8(debug='unknown field player {} {}'.format(i, j))

        data.done()


def fill(data: ScnDataWriter):
    # TODO
    pass
