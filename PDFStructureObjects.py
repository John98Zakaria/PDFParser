from collections import namedtuple
from dataclasses import dataclass
import io

from PDFObjects import PDFDict


@dataclass
class PDFStream:
    def __init__(self,stream_dict:PDFDict,startAdress,inuse):
        self.stream_dict = stream_dict
        self.startAddress = startAdress
        self.length = stream_dict["/Length"]
        self.inuse = inuse

    def read_stream(self,file:io.BytesIO)->bytes:
        pass

    def to_bytes(self,file:io.BytesIO,obj_number,object_rev)->bytes:
        byte_representation = f"{obj_number} {object_rev} obj\n{self.stream_dict}".encode("utf-8")
        byte_representation+= self.read_stream(file)
        byte_representation+="\nendsteam\nendobj"

    def __str__(self):
        return f"StreamObject {self.stream_dict}"

class PDFObject:
    def __init__(self, stream_dict, startAdress,inuse):
        self.stream_dict = stream_dict
        self.startAddress = startAdress
        self.inuse = inuse

    def read_stream(self, file: io.BytesIO):
        return b""

    def to_bytes(self,file:io.BytesIO,obj_number, object_rev) -> bytes:
        byte_representation = f"{obj_number} {object_rev} obj\n{self.stream_dict}\nendobj\n".encode("utf-8")
        return byte_representation

    def __str__(self):
        return f"Object {self.stream_dict}"


class XRefTable:
    def __init__(self, xref_address: int, xref_table: list):
        self.address = xref_address
        self.table = self.parse_table(xref_table)

    @staticmethod
    def parse_table(table):
        def parse_entry(entry: bytes) -> tuple:
            if (type(entry) == bytes):
                entry = entry.decode("utf-8")
            entry = entry.split(" ")[:3]
            entry[0] = int(entry[0])
            entry[1] = int(entry[1])
            tup = namedtuple("XrefEntry", ["address", "revision", "in_use_entry"])
            return tup(*entry)
        return list(map(parse_entry,table))


    def __len__(self):
        return len(self.table)

    def __str__(self):
        out_string = f"xref\n0 {len(self)}\n"
        for entry in self.table:
            out_string+= f"{str(entry.address).zfill(10)} {str(entry.revision).zfill(5)} {entry.in_use_entry} \n"
        return out_string

    def __repr__(self):
        return self.__str__()