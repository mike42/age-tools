from typing import List

from attr import dataclass

from libage.scenario.data import ScnDataReader


@dataclass
class TechnologyCost:
    resource: int
    amount: int
    paid: int

    @staticmethod
    def read(data: ScnDataReader):
        return TechnologyCost(
            data.int16(debug='resource'),
            data.int16(debug='amount'),
            data.uint8(debug='paid')
        )


@dataclass
class Technology:
    required_techs: List[int]
    costs: List[TechnologyCost]
    min_required_techs: int
    research_location: int
    langauge_file_name: int
    language_file_desc: int
    research_time: int
    effect: int
    type: int
    icon: int
    button: int
    lang_file_help: int
    lang_file_tech_tree: int
    hotkey: int
    name: str

    @staticmethod
    def read(data: ScnDataReader):
        required_techs = [
            data.int16(debug='required_tech1'),
            data.int16(debug='required_tech2'),
            data.int16(debug='required_tech3'),
            data.int16(debug='required_tech4')
        ]
        costs = [TechnologyCost.read(data) for _ in range(0, 3)]
        min_required_techs = data.int16(debug='min_required_techs')
        research_location = data.int16(debug='research_location')
        langauge_file_name = data.int16(debug='langauge_file_name')
        language_file_desc = data.int16(debug='language_file_desc')
        research_time = data.int16(debug='research_time')
        effect = data.int16(debug='effect')
        type = data.int16(debug='type')
        icon = data.int16(debug='icon')
        button = data.uint8(debug='button')
        lang_file_help = data.int32(debug='lang_file_help')
        lang_file_tech_tree = data.int32(debug='lang_file_tech_tree')
        hotkey = data.uint32(debug='hotkey')
        tech_name_len = data.uint16(debug='name_len')
        name = data.string_fixed(size=tech_name_len, debug='name')
        return Technology(required_techs,
                          costs,
                          min_required_techs,
                          research_location,
                          langauge_file_name,
                          language_file_desc,
                          research_time,
                          effect,
                          type,
                          icon,
                          button,
                          lang_file_help,
                          lang_file_tech_tree,
                          hotkey,
                          name)


def load(data: ScnDataReader) -> List[Technology]:
    """
    Read all technologies from here
    """
    data.mark('technologies')
    num_techs = data.int16(debug='num_techs')
    return [Technology.read(data) for _ in range(0, num_techs)]
