from pypeg2 import *

"""
Elements which may appear anywhere in an RMS script
"""


class LiteralValue(str):
    grammar = re.compile(r"((\d+(\.\d+)?)|(\.\d+))")


class ConstValue(str):
    grammar = re.compile(r"[A-Z]+[A-Za-z0-9_]*")


class RandomValue(List):
    grammar = "rnd(", csl(LiteralValue), ")"


command_argument = [
    LiteralValue,
    ConstValue,
    RandomValue
]

newline = ignore(re.compile(r'\n+'))

"""
Known commands
"""


class CommandKeyword(Keyword):
    grammar = Enum(
        K("ai_info_map_type"),
        K("base_elevation"),
        K("base_size"),
        K("base_terrain"),
        K("border_fuzziness"),
        K("bottom_border"),
        K("cliff_curliness"),
        K("clumping_factor"),
        K("group_placement_radius"),
        K("group_variance"),
        K("height_limits"),
        K("land_percent"),
        K("land_position"),
        K("left_border"),
        K("max_distance_to_other_zones"),
        K("max_distance_to_players"),
        K("max_length_of_cliff"),
        K("max_number_of_cliffs"),
        K("min_distance_cliffs"),
        K("min_distance_group_placement"),
        K("min_distance_to_players"),
        K("min_length_of_cliff"),
        K("min_number_of_cliffs"),
        K("number_of_clumps"),
        K("number_of_groups"),
        K("number_of_objects"),
        K("number_of_tiles"),
        K("other_zone_avoidance_distance"),
        K("random_placement"),
        K("replace_terrain"),
        K("right_border"),
        K("set_avoid_player_start_areas"),
        K("set_flat_elevation_only"),
        K("set_flat_terrain_only"),
        K("set_gaia_object_only"),
        K("set_loose_grouping"),
        K("set_place_for_every_player"),
        K("set_scale_by_groups"),
        K("set_scale_by_size"),
        K("set_scaling_to_map_size"),
        K("set_tight_grouping"),
        K("set_zone_by_team"),
        K("spacing_to_other_terrain_types"),
        K("temp_min_distance_group_placement"),
        K("terrain_cost"),
        K("terrain_size"),
        K("terrain_to_place_on"),
        K("terrain_type"),
        K("top_border"),
        K("zone")
    )


"""
All blocks (unknown blocks cannot be read)
"""

class BlockKeyword(Keyword):
    grammar = Enum(
        K("create_land"),
        K("create_player_lands"),
        K("create_elevation"),
        K("create_terrain"),
        K("create_object"),
        K("create_connect_all_players_land")
    )


class SectionKeyword(Keyword):
    grammar = Enum(
        K("PLAYER_SETUP"),
        K("LAND_GENERATION"),
        K("ELEVATION_GENERATION"),
        K("CLIFF_GENERATION"),
        K("TERRAIN_GENERATION"),
        K("CONNECTION_GENERATION"),
        K("OBJECTS_GENERATION")
    )


class Command(List):
    # Covers known commands
    grammar = attr("name", CommandKeyword), \
        maybe_some(command_argument)


class UnknownCommand(List):
    things_to_skip = "start_random|percent_chance|end_random|if|elseif|else|endif"
    command_regex = re.compile(r"^(?!" + things_to_skip + ")[a-z]+[a-z0-9_]*")

    grammar = attr("name", command_regex), \
              optional(attr("arg1", command_argument)), \
              optional(attr("arg2", command_argument)), \
              optional(attr("arg3", command_argument)), \
              optional(attr("arg4", command_argument)), \
              optional(attr("arg5", command_argument)), \
              optional(attr("arg6", command_argument)), \
              optional(attr("arg7", command_argument)), \
              optional(attr("arg8", command_argument))


class BlockIdentifier(List):
    # Covers known commands
    grammar = attr("name", BlockKeyword), maybe_some(newline), optional(command_argument)


"""
Preprocessor-style commands
"""


class Define(List):
    grammar = '#define', ConstValue


class Const(List):
    grammar = "#const", ConstValue, command_argument


class Include(List):
    filename_regex = re.compile(r"[A-Za-z_0-9\\.]+")

    grammar = '#include_drs', attr("name", filename_regex), optional(attr("value", command_argument))


"""
Define all structures which can nest
"""


class RandomBranch(List):
    pass


class BlockCommands(List):
    pass


class If(List):
    pass


class ElseIf(List):
    pass


class Else(List):
    pass


class ConditionalBranch(List):
    pass


class RandomSection(List):
    pass


class Section(List):
    pass


commands = [
    newline,
    Section,
    Define,
    Const,
    Include,
    RandomBranch,
    ConditionalBranch,
    BlockCommands,
    BlockIdentifier,
    Command,
    UnknownCommand
]

commands_but_not_sections = [
    newline,
    Define,
    Const,
    Include,
    RandomBranch,
    ConditionalBranch,
    BlockCommands,
    BlockIdentifier,
    Command,
    UnknownCommand
]

class Commands(List):
    grammar = maybe_some(commands)

class Weight(List):
    grammar = optional(command_argument)

class Condition(List):
    grammar = optional(command_argument)

BlockCommands.grammar = "{", maybe_some(commands), optional("}"), maybe_some(newline)

# Random: start_random, percent_chance, end_random
RandomBranch.grammar = "start_random", maybe_some(newline), maybe_some([newline, RandomSection]), "end_random"
RandomSection.grammar = "percent_chance", Weight, Commands

# Conditionals: if, elseif, else, endif.
ConditionalBranch.grammar = "if", maybe_some(newline), If, maybe_some(ElseIf), optional(Else), optional("endif")
If.grammar = Condition, Commands
ElseIf.grammar = "elseif", maybe_some(newline), Condition, Commands
Else.grammar = "else", Commands

Section.grammar = '<', attr("name", Symbol), '>', maybe_some(commands_but_not_sections)
