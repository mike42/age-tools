import logging
from typing import List

from attr import dataclass

from libage.scenario.data import ScnDataReader


@dataclass
class DRSHeader:
    banner: str
    version: str
    identifier: str
    num_tables: int
    metadata_bytes: int

    @staticmethod
    def read(data: ScnDataReader):
        return DRSHeader(
            data.string_fixed(40),
            data.string_fixed(4),
            data.string_fixed(12),
            data.uint32(),
            data.uint32()
        )


@dataclass
class DRSResourceType:
    resource_type: bytes

    def to_fileext(self):
        # knock off spaces, last character (eg. 'bina' -> 'bin')
        res_str = self.resource_type[::-1]
        return res_str.decode('ascii')[0:3].strip()

    @staticmethod
    def read(data: ScnDataReader):
        return DRSResourceType(data.read(4))


@dataclass
class DRSTableResource:
    id: int
    offset: int
    size: int

    @staticmethod
    def read(data: ScnDataReader):
        return DRSTableResource(
            data.uint32(),
            data.uint32(),
            data.uint32()
        )


@dataclass
class DRSTable:
    resource_type: DRSResourceType
    resource_offset: int
    num_resources: int

    @staticmethod
    def read(data: ScnDataReader):
        return DRSTable(DRSResourceType.read(data),
                        data.uint32(),
                        data.uint32())


@dataclass
class DRSResources:
    resources: List[DRSTableResource]

    @staticmethod
    def read(data: ScnDataReader, num_resources: int):
        resources = [DRSTableResource.read(data) for _ in range(0, num_resources)]
        return DRSResources(resources)


def load(file_name: str):
    if not (file_name.endswith(".drs")):
        raise Exception("Game asset archive must end with .drs")

    with open(file_name, 'rb') as f:
        print("Reading {}".format(file_name))
        all_data_bytes = f.read()
        data = ScnDataReader(all_data_bytes)
        header = DRSHeader.read(data)
        logging.debug(header)

        print("File has {} tables".format(header.num_tables))
        tables = []
        for i in range(0, header.num_tables):
            table = DRSTable.read(data)
            tables.append(table)

        table_resource_lists = []
        for i in range(0, header.num_tables):
            table_resource_list = DRSResources.read(data, tables[i].num_resources)
            table_resource_lists.append(table_resource_list)

        for i in range(0, header.num_tables):
            table = tables[i]
            resource_list = table_resource_lists[i]
            for resource in resource_list.resources:
                resource_start = resource.offset
                resource_end = resource.offset + resource.size
                resource_content = all_data_bytes[resource_start:resource_end]
                resource_fn = ("{}.{}".format(resource.id, table.resource_type.to_fileext()))
                print("Writing {}".format(resource_fn))
                open(resource_fn, 'wb').write(resource_content)
