import io
import logging
import struct
import zlib


class ScnDataWriter:
    """
    Write out data files (Opposite of ScnDataWriter)
    """

    def __init__(self):
        self.uncompressed_segment = io.BytesIO()
        self.compressed_segment = io.BytesIO()
        self.data = self.uncompressed_segment

    def compress(self):
        """
        Start writing to compressed data segment
        """
        self.data = self.compressed_segment

    def done(self) -> bytes:
        compressor = zlib.compressobj(wbits=-15)
        self.compressed_segment.seek(0)
        self.uncompressed_segment.write(compressor.compress(self.compressed_segment.read()))
        self.uncompressed_segment.write(compressor.flush())
        self.uncompressed_segment.seek(0)
        return self.uncompressed_segment.read()

    def uint8(self, value: int):
        value_bytes = value.to_bytes(1, byteorder='little', signed=False)
        self.data.write(value_bytes)

    def int8(self, value: int):
        value_bytes = value.to_bytes(1, byteorder='little', signed=True)
        self.data.write(value_bytes)

    def uint16(self, value: int):
        value_bytes = value.to_bytes(2, byteorder='little', signed=False)
        self.data.write(value_bytes)

    def int16(self, value: int):
        value_bytes = value.to_bytes(2, byteorder='little', signed=True)
        self.data.write(value_bytes)

    def uint32(self, value: int):
        value_bytes = value.to_bytes(4, byteorder='little', signed=False)
        self.data.write(value_bytes)

    def int32(self, value: int):
        value_bytes = value.to_bytes(4, byteorder='little', signed=True)
        self.data.write(value_bytes)

    def float32(self, value: float):
        value_bytes = struct.pack('f', value)
        self.data.write(value_bytes)

    def string_fixed(self, value: str, size: int):
        value_bytes = value.encode('ascii')
        current_size = len(value_bytes)
        if current_size > size:
            raise Exception("Expected {} bytes but got {} bytes (value too long)", size, len(value_bytes))
        elif current_size < size:
            # Pad with 0x00
            value_bytes += b"\x00" * (size - current_size)
        self.data.write(value_bytes)

    def string16(self, value):
        size = len(value)
        self.uint16(size)
        self.string_fixed(value, size)

    def boolean32(self, value):
        self.uint32(1 if value else 0)

    def string32(self, value):
        size = len(value)
        self.uint32(size)
        self.string_fixed(value, size)

    def boolean8(self, value):
        self.uint8(1 if value else 0)


class ScnDataReader:
    """
    Wrap all I/O read operations to the SCN file
    """

    def __init__(self, data):
        self.mark_name = ''
        self.bytes_read_since_mark = 0
        self.byteio = io.BytesIO(data)

    def read(self, size=None):
        if size is not None:
            self.bytes_read_since_mark = self.bytes_read_since_mark + size
        ret = self.byteio.read(size)
        if size is not None and size != len(ret):
            raise Exception("Unexpected end of file")
        return ret

    def uint8(self, debug=None):
        ret = int.from_bytes(self.read(1), byteorder='little', signed=False)
        if debug is not None:
            logging.debug("Read uint8 %s='%d'", debug, ret)
        return ret

    def int8(self, debug=None):
        ret = int.from_bytes(self.read(1), byteorder='little', signed=True)
        if debug is not None:
            logging.debug("Read uint8 %s='%d'", debug, ret)
        return ret

    def uint16(self, debug=None):
        ret = int.from_bytes(self.read(2), byteorder='little', signed=False)
        if debug is not None:
            logging.debug("Read uint16 %s='%d'", debug, ret)
        return ret

    def int16(self, debug=None):
        ret = int.from_bytes(self.read(2), byteorder='little', signed=True)
        if debug is not None:
            logging.debug("Read int16 %s='%d'", debug, ret)
        return ret

    def uint32(self, debug=None):
        ret = int.from_bytes(self.read(4), byteorder='little', signed=False)
        if debug is not None:
            logging.debug("Read uint32 %s='%d'", debug, ret)
        return ret

    def int32(self, debug=None) -> int:
        ret = int.from_bytes(self.read(4), byteorder='little', signed=True)
        if debug is not None:
            logging.debug("Read int32 %s='%d'", debug, ret)
        return ret

    def float32(self, debug=None) -> float:
        ret = struct.unpack('f', self.read(4))[0]
        if debug is not None:
            logging.debug("Read float32 %s='%f'", debug, ret)
        return ret

    def string_fixed(self, size, debug=None) -> str:
        """
        Fixed-length string dropping anything after the null.
        """
        ret = self.stop_at_null(self.read(size).decode('ascii'))
        if debug is not None:
            logging.debug("Read string %s='%s'", debug, ret)
        return ret

    @staticmethod
    def stop_at_null(str):
        ret = ''
        for i in range(0, len(str)):
            if str[i] == '\0':
                break
            else:
                ret += str[i]
        return ret

    def string16(self, debug=None):
        """
        Variable-length string, with length read from first two bytes
        """
        size = self.uint16()
        return self.string_fixed(size, debug)

    def string32(self, debug=None):
        """
        Variable-length string, with length read from first four bytes
        """
        size = self.uint32()
        return self.string_fixed(size, debug)

    def boolean32(self, debug=None):
        ret = self.uint32() != 0
        logging.debug("Read boolean %s='%s'", debug, ret)
        return ret

    def boolean8(self, debug=None):
        ret = self.uint8() != 0
        logging.debug("Read boolean %s='%s'", debug, ret)
        return ret

    def decompress(self):
        """
        De-compress remaining data
        """
        compressed_data = self.byteio.read()
        decompressed_data = zlib.decompress(compressed_data, wbits=-15)
        self.byteio = io.BytesIO(decompressed_data)

    def mark(self, name, limit=None):
        """
        Mark the beginning of a fixed-length block of data. We count how many bytes we are
        asked to read from here (may eg. include variable-length fields), and check this
        when we unmark(), so that we can detect mis-reads.
        """
        self.mark_info = {'name': name, 'limit': limit, 'offset': hex(self.byteio.tell())}
        self.bytes_read_since_mark = 0
        logging.debug(self.mark_info)

    def unmark(self):
        if self.bytes_read_since_mark != self.mark_info['limit']:
            raise Exception("The structure {} has length {}, but we read {}".format(self.mark_info['name'],
                                                                                    self.mark_info['limit'],
                                                                                    self.bytes_read_since_mark))

    def done(self):
        remainder = self.byteio.read()
        remainder_len = len(remainder)
        if remainder_len > 0:
            raise Exception("Expected end of file, but there are {} bytes left".format(remainder_len))
