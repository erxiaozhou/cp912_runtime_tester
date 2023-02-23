from collections import Counter
import os
from pathlib import Path
import random
import struct
from extract_dump.extractor import is_failed_content
from file_util import bytes2f32, bytes2uint, check_dir, f32bytes, pickle_dump, pickle_load, print_ba, read_bytes, remove_file_without_exception, rm_dir, save_json, uint2bytes, write_bytes
from nan_detect_util import is_anan, is_nan
import numpy as np
from file_util import path_read
from file_util import path_write
import leb128
import time

def test_test():
    assert 123 == 123

def test_ty_transform_util():
    # int_val = 0b011111111<<23
    # int_val += 1-1
    # test_ba = int.to_bytes(int_val, 4, byteorder='little', signed=False)
    # print(len(test_ba))
    # print_ba(test_ba)
    
    nan = np.nan
    inf = np.inf
    f64_val = 123.0
    i32_inf = bytes2uint(f32bytes(inf))
    i32_nan = bytes2uint(f32bytes(nan))
    print('{:0>32b}'.format(i32_inf))
    print('{:0>32b}'.format(i32_nan))
    inf_add1 = i32_inf + 1
    bytes_inf_add1 = uint2bytes(inf_add1, 4)
    f32_inf_add1 = bytes2f32(bytes_inf_add1)
    print(f32_inf_add1)
    print(is_nan(bytes_inf_add1), is_anan(bytes_inf_add1))


if __name__ == '__main__':
    test_ty_transform_util()
