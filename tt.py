import os
from pathlib import Path
import struct
from file_util import check_dir, pickle_dump, pickle_load, read_bytes, remove_file_without_exception, rm_dir, save_json, write_bytes
import numpy as np
from file_util import path_read
from file_util import path_write
import leb128


def print_ba(ba):
    print([hex(x) for x in ba])


class a:
    def __init__(self) -> None:
        self.a1 = None
        self.a2 = 'a123'
        self.a3 = 135

    def as_pkl(self, path):
        pickle_dump(path, self)


if __name__ == '__main__':
    # test_env('./tcs_v2')
    # test_env('./tcs')
    # bs_32 = bytearray(struct.pack('<f', np.nan))
    # bs_64 = bytearray(struct.pack('<d', np.nan))
    # print(bs_32)
    # print(bs_64)
    # pinf_32 = bytearray(struct.pack('<f', np.inf))
    # pinf_64 = bytearray(struct.pack('<d', np.inf))
    # print(bs_32, get_f32_h10(bs_32))
    # print(bs_64, get_f64_h13(bs_64))
    # print(pinf_32, get_f32_h10(pinf_32))
    # print(pinf_64, get_f64_h13(pinf_64))

    # data = {
    #     'abc': bytearray([1,2,3])
    # }
    # # save_json('data.json', data)
    # pickle_dump('data.json', data)
    # data2 = pickle_load('data.json')
    # assert data == data2
    # num_bytes
    # print(np.frombuffer(bytes([0,0x80,0x80, 0,0,0,0x5f,0x78]), 'double'))
    # print_ba(leb128.u.encode(0x40))
    # print(leb128.u.decode(bytearray([0x40])))
    # print(leb128.u.decode(bytearray([0, 0x80])))
    # print(leb128.u.decode(bytearray([0, 0x80,0, 0x80])))

    # print(leb128.i.decode(bytearray([0x9B, 0xE4, 0xF9, 0xB0, 0x79])))
    # print(leb128.i.decode(bytearray([0xF2, 0xB6, 0x91, 0xDC, 0x03])))
    # print([hex(x) for x in leb128.i.encode(5)])
    # print([hex(x) for x in leb128.i.encode(10)])
    ba = bytearray([1,2,3,4])
    ba.insert(4, 255)
    print(ba)
