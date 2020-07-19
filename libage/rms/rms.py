from pypeg2 import *

# Using C-style comment for now.
# TODO: Actual game does not accept non-whitespace either side of /* and */
from libage.rms.rms_common import commands

comment_rms = re.compile(r"(?ms)/\*.*?\*/")

# Commands are newline-delimited, cant ignore newlines completely
whitespace_rms = re.compile("(?m)[ \t\r]+")


class RmsFile(List):
    grammar = maybe_some(commands)


def read_str(content: str, filename=None) -> RmsFile:
    """
    # Read from string
    # """
    return parse(content, RmsFile,
                 comment=comment_rms,
                 whitespace=whitespace_rms,
                 filename=filename)


def read(file_name: str):
    """
    Read from file
    """
    if not (file_name.lower().endswith(".rms") or file_name.lower().endswith(".rms2") or file_name.lower().endswith(".def") or file_name.lower().endswith(".inc")):
        raise Exception("Random map script file must end in .rms or .rms2. Included files must be .inc or .def.")
    with open(file_name, 'rb') as f:
        # endoding: megarandom script has a rogue Latin-1 š on line 2807 which doesn't parse.
        return read_str(f.read().decode('iso-8859-1'), filename=file_name)
