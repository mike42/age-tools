from typing import List

from attr import dataclass

from libage.scenario.data import ScnDataReader


@dataclass
class SoundItem:
    filename: str
    resource_id: int
    probability: int

    @staticmethod
    def read(data: ScnDataReader):
        return SoundItem(
            data.string_fixed(13, debug='sound_filename'),
            data.uint32(debug='sound_resource_id'),
            data.uint16(debug='sound_probability')
        )


@dataclass
class Sound:
    id: int
    play_delay: int
    cache_time: int
    items: List[SoundItem]

    @staticmethod
    def read(data: ScnDataReader):
        id = data.uint16(debug='sound_id')
        play_delay = data.uint16(debug='sound_play_delay')
        num_items = data.uint16(debug='sound_num_items')
        cache_time = data.uint32()
        items = [SoundItem.read(data) for _ in range(0, num_items)]
        return Sound(
            id,
            play_delay,
            cache_time,
            items
        )


def load(data: ScnDataReader) -> List[Sound]:
    data.mark(name='sounds')
    num_sounds = data.uint16(debug='num_sounds')
    return [Sound.read(data) for _ in range(0, num_sounds)]
