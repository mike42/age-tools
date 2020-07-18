from pypeg2 import *

# Using C-style comment for now.
# TODO: Actual game does not accept non-whitespace either side of /* and */
comment_rms = re.compile(r"(?ms)/\*.*?\*/")

# Commands are newline-delimited, cant ignore newlines completely
whitespace_rms = re.compile("(?m)[ \t\r]+")

newline = re.compile(r'\n+')

command_argument = re.compile(r"[A-Za-z0-9_]+")  # constant or numeric literal


class ConstDefinition(List):
    constant_name_regex = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")

    grammar = "#const", attr("name", constant_name_regex), optional(attr("value", command_argument)), maybe_some(
        newline)


class CommandKeyword(Keyword):
    grammar = Enum(
        # Player setup stuff
        K("ai_info_map_type"),
        K("random_placement"),

        # Land stuff
        K("base_terrain"),

        # create_land stuff
        K("border_fuzziness"),
        K("bottom_border"),
        K("land_percent"),
        K("land_position"),
        K("left_border"),
        K("number_of_tiles"),
        K("right_border"),
        K("terrain_type"),
        K("top_border"),

        # create_player_lands stuff
        K("terrain_type"),
        K("base_size"),
        K("base_elevation"),
        K("number_of_tiles"),
        K("clumping_factor"),
        K("other_zone_avoidance_distance"),
        K("right_border"),
        K("left_border"),
        K("top_border"),
        K("bottom_border"),
        K("set_zone_by_team"),

        # create_elevation stuff
        K("number_of_clumps"),
        K("set_scale_by_size"),

        # create_terrain stuff
        K("base_terrain"),
        K("land_percent"),
        K("number_of_clumps"),
        K("clumping_factor"),
        K("set_avoid_player_start_areas"),
        K("spacing_to_other_terrain_types"),
        K("set_scale_by_groups"),
        K("height_limits"),

        # create_object stuff
        K("set_place_for_every_player"),
        K("group_placement_radius"),
        K("min_distance_to_players"),
        K("max_distance_to_players"),
        K("number_of_objects"),
        K("number_of_groups"),
        K("set_gaia_object_only"),
        K("set_place_for_every_player"),
        K("min_distance_to_players"),
        K("min_distance_group_placement"),
        K("set_loose_grouping"),
        K("terrain_to_place_on"),
        K("set_tight_grouping"),
        K("temp_min_distance_group_placement"),
        K("set_scaling_to_map_size"),

        # Not really commands
        K("start_random"),
        K("percent_chance"),
        K("end_random"),
        K("if"),
        K("elseif"),
        K("else"),
        K("endif")

    )


class BlockCommandKeyword(Keyword):
    grammar = Enum(
        K("create_land"),
        K("create_player_lands"),
        K("create_elevation"),
        K("create_terrain"),
        K("create_object")
    )


class Command(List):
    # TODO capture arguments as a list here
    grammar = attr("name", CommandKeyword), \
              optional(attr("arg1", command_argument)), \
              optional(attr("arg2", command_argument)), \
              optional(attr("arg3", command_argument)), \
              optional(attr("arg4", command_argument)), \
              optional(attr("arg5", command_argument)), \
              optional(attr("arg6", command_argument)), \
              optional(attr("arg7", command_argument)), \
              optional(attr("arg8", command_argument)), \
              maybe_some(newline)


class CommandBlock(List):
    grammar = attr("name", BlockCommandKeyword), \
              optional(attr("arg1", command_argument)), \
              maybe_some(newline), \
              "{", maybe_some([
        Command,
        newline
    ]), "}", maybe_some(newline)


class PlayerSetupSection(List):
    grammar = '<PLAYER_SETUP>', maybe_some([
        newline,
        ConstDefinition,
        CommandBlock,
        Command
    ])


class LandGenerationSection(List):
    grammar = '<LAND_GENERATION>', maybe_some([
        newline,
        ConstDefinition,
        CommandBlock,
        Command
    ])


class ElevationGenerationSection(List):
    grammar = '<ELEVATION_GENERATION>', maybe_some([
        newline,
        ConstDefinition,
        CommandBlock,
        Command
    ])


class CliffGenerationSection(List):
    grammar = '<CLIFF_GENERATION>', maybe_some([
        newline,
        ConstDefinition,
        CommandBlock,
        Command
    ])


class TerrainGernationSection(List):
    grammar = '<TERRAIN_GENERATION>', maybe_some([
        newline,
        ConstDefinition,
        CommandBlock,
        Command
    ])


class ConnectionGenerationSection(List):
    grammar = '<CONNECTION_GENERATION>', maybe_some([
        newline,
        ConstDefinition,
        CommandBlock,
        Command
    ])


class ObjectsGenerationSection(List):
    grammar = '<OBJECTS_GENERATION>', maybe_some([
        newline,
        ConstDefinition,
        CommandBlock,
        Command
    ])


class RmsFile(List):
    grammar = maybe_some([newline, ConstDefinition]), \
              maybe_some([
                  PlayerSetupSection,
                  LandGenerationSection,
                  ElevationGenerationSection,
                  CliffGenerationSection,
                  TerrainGernationSection,
                  ConnectionGenerationSection,
                  ObjectsGenerationSection
              ])


def read_str(content: str, filename=None) -> RmsFile:
    """
    # Read from string
    # """
    return parse(content, RmsFile,
                 comment=comment_rms,
                 whitespace=whitespace_rms,
                 filename=filename)


def read(path: str):
    """
    Read from file
    """
    with open(path, 'r') as f:
        return read_str(f.read(), filename=path)
