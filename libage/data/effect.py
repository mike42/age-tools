from typing import List

from attr import dataclass

from libage.scenario.data import ScnDataReader


@dataclass
class EffectCommand:
    type: int
    params: tuple

    @staticmethod
    def read(data: ScnDataReader):
        effect_comamnd_type = data.uint8()
        effect_params = (
            data.int16(),
            data.int16(),
            data.int16(),
            data.float32()
        )
        return EffectCommand(effect_comamnd_type, effect_params)


@dataclass
class Effect:
    name: str
    commands: List[EffectCommand]

    @staticmethod
    def read(data: ScnDataReader):
        effect_name = data.string_fixed(size=31, debug='effect_name')
        effect_num_commands = data.uint16(debug='effect_num_commands')
        commands = [EffectCommand.read(data) for _ in range(0, effect_num_commands)]
        return Effect(effect_name, commands)


def load(data: ScnDataReader) -> List[Effect]:
    """
    Read all effects from here
    """
    data.mark("effects")
    num_effects = data.uint32()
    return [Effect.read(data) for _ in range(0, num_effects)]

