from enum import Enum
from typing import List

from PIL import Image, ImageDraw
from attr import dataclass

from libage.scenario.data import ScnDataReader
from libage.slp.palette import Palette


@dataclass
class SlpHeader:
    version: str
    frames: int
    comment: str

    @staticmethod
    def read(data: ScnDataReader):
        return SlpHeader(
            data.string_fixed(4),
            data.uint32(),
            data.string_fixed(24)
        )


@dataclass
class SlpFrameInfo:
    command_table_offset: int
    outline_table_offset: int
    palette_offset: int
    props: int
    width: int
    height: int
    centre_x: int
    centre_y: int

    @staticmethod
    def read(data: ScnDataReader):
        return SlpFrameInfo(
            data.uint32(),
            data.uint32(),
            data.uint32(),
            data.uint32(),
            data.int32(),
            data.int32(),
            data.int32(),
            data.int32()
        )


@dataclass
class SlpOutlineRow:
    left_space: int
    right_space: int

    @staticmethod
    def read(data: ScnDataReader):
        return SlpOutlineRow(
            data.uint16(),
            data.uint16()
        )


@dataclass
class SlpOutline:
    row: List[SlpOutlineRow]

    @staticmethod
    def read(data: ScnDataReader, count: int):
        rows = [SlpOutlineRow.read(data) for _ in range(0, count)]
        data.done()
        return SlpOutline(rows)


@dataclass
class SlpCommandOffset:
    row: List[int]

    @staticmethod
    def read(data: ScnDataReader, count: int):
        rows = [data.uint32() for _ in range(0, count)]
        data.done()
        return SlpCommandOffset(rows)


class SlpDrawCommandType(Enum):
    PALETTE_PIXELS_DRAW = 1
    TRANSPARENT_DRAW = 2
    PLAYER_PIXELS_DRAW = 3
    PALETTE_PIXEL_REPEAT = 4
    PLAYER_PIXEL_REPEAT = 5
    EXTENDED_COMMAND = 6
    SHADOW_DRAW = 7
    END_OF_ROW = 8


@dataclass
class SlpDrawCommand:
    # A good reference for this is:
    # https://github.com/SFTtech/openage/blob/9f13a91184e16af761fd9b654ff66cb3665261dd/doc/media/slp-files.md
    type: SlpDrawCommandType
    len: int
    pixels: bytes

    @staticmethod
    def read(data: ScnDataReader):
        cmd_byte = data.uint8()
        if cmd_byte & 0x03 == 0x00:
            # "Lesser draw"
            draw_len = cmd_byte >> 2
            draw_px = data.read(draw_len)
            # if draw len == 0 ??
            return SlpDrawCommand(SlpDrawCommandType.PALETTE_PIXELS_DRAW, draw_len, draw_px)
        elif cmd_byte & 0x03 == 0x01:
            # "Lesser skip"
            draw_len = cmd_byte >> 2
            if draw_len == 0:
                draw_len = data.uint8()
            return SlpDrawCommand(SlpDrawCommandType.TRANSPARENT_DRAW, draw_len, b"")
        elif cmd_byte & 0x0F == 0x02:
            # "Greater draw"
            draw_len = ((cmd_byte & 0xF0) << 4) + data.uint8()
            draw_px = data.read(draw_len)
            return SlpDrawCommand(SlpDrawCommandType.PALETTE_PIXELS_DRAW, draw_len, draw_px)
        elif cmd_byte & 0x0F == 0x03:
            # "Greater skip"
            draw_len = ((cmd_byte & 0xF0) << 4) + data.uint8()
            return SlpDrawCommand(SlpDrawCommandType.TRANSPARENT_DRAW, draw_len, b"")
        elif cmd_byte & 0x0F == 0x06:
            # "Player color draw"
            draw_len = cmd_byte >> 4
            if draw_len == 0:
                draw_len = data.uint8()
            draw_px = data.read(draw_len)
            return SlpDrawCommand(SlpDrawCommandType.PLAYER_PIXELS_DRAW, draw_len, draw_px)
        elif cmd_byte & 0x0F == 0x07:
            # "Fill"
            draw_len = cmd_byte >> 4
            if draw_len == 0:
                draw_len = data.uint8()
            draw_px = data.read(1)
            return SlpDrawCommand(SlpDrawCommandType.PALETTE_PIXEL_REPEAT, draw_len, draw_px)
        elif cmd_byte & 0x0F == 0x0A:
            # "Player color fill"
            draw_len = cmd_byte >> 4
            if draw_len == 0:
                draw_len = data.uint8()
            draw_px = data.read(1)
            return SlpDrawCommand(SlpDrawCommandType.PLAYER_PIXEL_REPEAT, draw_len, draw_px)
        elif cmd_byte & 0x0F == 0x0B:
            draw_len = cmd_byte >> 4
            if draw_len == 0:
                draw_len = data.uint8()
            return SlpDrawCommand(SlpDrawCommandType.SHADOW_DRAW, draw_len, b"")
        elif cmd_byte & 0x0F == 0x0E:
            cmd_idx = cmd_byte >> 4
            return SlpDrawCommand(SlpDrawCommandType.EXTENDED_COMMAND, 1, bytes([cmd_idx]))
        elif cmd_byte == 0x0F: # ? Strange end of row??
            return SlpDrawCommand(SlpDrawCommandType.END_OF_ROW, 0, b"")
        print(cmd_byte)
        raise Exception("Unrecognised SLP draw byte, file may be corrupt.")

@dataclass
class SlpRow:
    commands: List[SlpDrawCommand]
    outline: SlpOutlineRow

    @staticmethod
    def read(data: ScnDataReader, outline: SlpOutlineRow):
        commands = []
        more_commands_expected = (outline.left_space < 0x8000 and outline.right_space < 0x800)
        while more_commands_expected:
            this_command = SlpDrawCommand.read(data)
            commands.append(this_command)
            if this_command.type == SlpDrawCommandType.END_OF_ROW:
                more_commands_expected = False
        return SlpRow(commands, outline)


@dataclass
class SlpFrame:
    info: SlpFrameInfo
    rows: List[SlpRow]


@dataclass
class SlpFile:
    header: SlpHeader
    frames: List[SlpFrame]


def load(file_name: str):
    if not (file_name.endswith(".slp")):
        raise Exception("SLP file must end with .slp")

    with open(file_name, 'rb') as f:
        all_data = f.read()
        data = ScnDataReader(all_data)

    header = SlpHeader.read(data)
    frames = []
    for i in range(0, header.frames):
        data.mark('frame {}'.format(i))
        frame_info = SlpFrameInfo.read(data)
        # Sub-reader for outline data (identified by offset)
        outline_region_start = frame_info.outline_table_offset
        outline_region_end = outline_region_start + frame_info.height * 4
        outline_reader = ScnDataReader(all_data[outline_region_start:outline_region_end])
        frame_outline = SlpOutline.read(outline_reader, frame_info.height)
        # Sub-reader for pixel offsets
        command_offset_region_start = frame_info.command_table_offset
        command_offset_region_end = command_offset_region_start + frame_info.height * 4
        command_offset_reader = ScnDataReader(all_data[command_offset_region_start:command_offset_region_end])
        command_offset = SlpCommandOffset.read(command_offset_reader, frame_info.height)
        # Sub-reader for pixel data (very inefficient..)
        command_data_reader = ScnDataReader(all_data)
        command_data_reader.read(command_offset.row[0])  # read and discard so that we don't need to do maths to find in-file offset
        rows = []
        for y in range(0, frame_info.height):
            row = SlpRow.read(command_data_reader, frame_outline.row[y])
            rows.append(row)
        frames.append(SlpFrame(frame_info, rows))
    return SlpFile(header, frames)


def pal_col(pal, color_idx):
    color_rgb = pal.cols[color_idx]
    return (color_rgb.r, color_rgb.g, color_rgb.b)


def player_col(pal, color_idx, player_id):
    player_col_idx = color_idx + player_id * 16
    if player_col_idx > 255:
        player_col_idx = 0
    return pal_col(pal, player_col_idx)


def draw(slp_file: SlpFile, pal: Palette, player_id=1, frame_id=0):
    slp_frame = slp_file.frames[frame_id]
    outp = Image.new('RGBA', (slp_frame.info.width, slp_frame.info.height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(outp)
    for y in range(0, slp_frame.info.height):
        slp_row = slp_frame.rows[y]
        pixels = []
        if slp_row.outline.left_space >= 0x8000 or slp_row.outline.right_space >= 0x8000:
            # transparent row
            continue
        # Left space
        for _ in range(0, slp_row.outline.left_space):
            pixels.append((0, 0, 0, 0))
        # Some actual pixels
        for cmd in slp_row.commands:
            if cmd.type == SlpDrawCommandType.PALETTE_PIXELS_DRAW:
                # Write some pixels
                for color_idx in cmd.pixels:
                    pixels.append(pal_col(pal, color_idx))
            elif cmd.type == SlpDrawCommandType.PLAYER_PIXELS_DRAW:
                # Write in pixels
                for color_idx in cmd.pixels:
                    pixels.append(player_col(pal, color_idx, player_id))
            elif cmd.type == SlpDrawCommandType.PALETTE_PIXEL_REPEAT:
                # Write in repeated pixel
                color_idx = ord(cmd.pixels)
                color_rgb = pal_col(pal, color_idx)
                for i in range(0, cmd.len):
                    pixels.append(color_rgb)
            elif cmd.type == SlpDrawCommandType.PLAYER_PIXEL_REPEAT:
                # Write in repeated pixel
                color_idx = ord(cmd.pixels)
                color_rgb = player_col(pal, color_idx, player_id)
                for i in range(0, cmd.len):
                    pixels.append(color_rgb)
            elif cmd.type == SlpDrawCommandType.TRANSPARENT_DRAW:
                # Draw some transparent pixels
                for i in range(0, cmd.len):
                    pixels.append((0, 0, 0, 0))
            elif cmd.type == SlpDrawCommandType.SHADOW_DRAW:
                # Draw darkness for shadow?
                for i in range(0, cmd.len):
                    pixels.append((0, 0, 0, 128))
            elif cmd.type == SlpDrawCommandType.EXTENDED_COMMAND:
                # Do nothing ?
                pass
            elif cmd.type == SlpDrawCommandType.END_OF_ROW:
                # Nothing much
                pass
            else:
                print(cmd)
                raise Exception("Don't know what to do")
        # Right space
        for _ in range(0, slp_row.outline.right_space):
            pixels.append((0, 0, 0, 0))
        # Quick check:
        if len(pixels) != slp_frame.info.width:
            print("Width check is failing")
           # raise("Unexpected width!") #  maybe after the files stop reading back incorrectly??
        # Draw it out!
        for x in range(0, slp_frame.info.width):
            try:
                draw.point((x, y), pixels[x])
            except IndexError:
                # Be very tolerant
                pass
    return outp

