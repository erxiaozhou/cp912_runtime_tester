from collections import Counter
import os
from pathlib import Path
import random
import struct
from extract_dump import is_failed_content
from file_util import pickle_dump, pickle_load, print_ba, read_bytes, read_json
from file_util import remove_file_without_exception, rm_dir, save_json
from file_util import uint2bytes, write_bytes
from nan_detect_util import is_anan, is_nan
import numpy as np
from file_util import path_read
from file_util import path_write
import leb128
import subprocess
from extract_dump.process_dump_data_util import get_f64
from random import random
from collections import Counter

class test_base:
    def __init__(self) -> None:
        self.a = 1
        self.b = 2
        self.c = 3
    
    def to_dict(self, path=None):
        # TODO
        data = {}
        data.update(self.__dict__)
        if path is not None:
            pickle_dump(path, data)
        return data


class test_class(test_base):
    def __init__(self) -> None:
        super().__init__()
        self.d = 4
    def to_dict(self, path=None):
        # return super().to_dict(path)
        new_obj = test_base()
        for k in new_obj.__dict__.keys():
            new_obj.__dict__[k] = self.__dict__[k]
        return new_obj.__dict__


def process_a_key(key):
    data = eval(key)
    assert isinstance(data, tuple)



if __name__ == '__main__':
    # print(bytearray(f32bytes(np.inf)))
    # print('{:b}'.format(bytes2uint(f32bytes(np.inf))))
    # print('{:b}'.format(bytes2uint(f32bytes(-np.inf))))
    # print('{:b}'.format(bytes2uint(f64bytes(np.inf))))
    # print('{:b}'.format(bytes2uint(f64bytes(-np.inf))))
    # pinf_32 = 0b01111111100000000000000000000000
    # ninf_32 = 0b11111111100000000000000000000000
    # pinf_64 = 0b0111111111110000000000000000000000000000000000000000000000000000
    # ninf_64 = 0b1111111111110000000000000000000000000000000000000000000000000000
    # p1 = Path('./tt/tt.wat')
    # p2 = Path('./tt/t2/tt.wasm')
    # p1.rename(p2)
    without_dt = read_bytes('tt.wasm')
    # with_dt = read_bytes('ori_tcs/only_i32_add_with_datacount/tcs/i32.add_0.wasm')
    # for i in range(max(len(without_dt), len(with_dt))):
    #     if with_dt[i] != without_dt[i]:
    #         break
    # print_ba(with_dt[i:])
    # print_ba(without_dt[i:])
    # without_dt_ba = bytearray(without_dt)
    # print(len(without_dt_ba))
    # without_dt_ba = without_dt_ba[:0xB2] + bytearray([0xc, 0x1, 0x3]) + without_dt_ba[0xB2:]
    # print(len(without_dt_ba))
    # write_bytes('tt2.wasm', without_dt_ba)
    # print_ba(leb128.u.encode(0x3d7a))
    # print(leb128.u.decode(bytearray([0xc7, 0x05])))
    # ba = read_bytes('./WAVM_illegalop_fd3d70.wasm')
    # ba = ba[:0x60] + bytearray([0x1A]) + ba[0x60:]
    # write_bytes('./WAVM_illegalop_fd3d70.wasm', ba)

    # d = {k:0 for k in range(10)}
    # d = Counter(d)
    # for i in range(100000):
    #     d[int(random()*10)] += 1
    # print(d)
    # err = subprocess.run('ls tt | wc -l', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, timeout=10).stderr
    # out = subprocess.run('ls tt | wc -l', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, timeout=10).stdout
    # print(out, type(out))
    # print(err, type(err))

    # a = bytearray(b'\x39\x00\x00\x00\x00\x00\xf0\x7f')
    # print(get_f64(a))

    # data = read_json('ctgy2insts.json')
    # visited_insts = set()
    # new_d = dict()
    # for k, insts in data.items():
    #     for inst in insts:
    #         assert inst not in visited_insts
    #         visited_insts.add(inst)
    #         new_d[inst] = k
    # save_json('inst2ctgys.json', new_d)

    a = 6
    print(int(a/2))
    a=5
    print(int(a/2))



    