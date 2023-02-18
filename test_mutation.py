#!/home/zph/anaconda3/bin/python
import os
from pathlib import Path
import random
import struct
from extract_dump.extractor import is_failed_content
from file_util import check_dir, cp_file, pickle_dump, pickle_load, read_bytes, remove_file_without_exception, rm_dir, save_json, write_bytes
import numpy as np
from file_util import path_read
from file_util import path_write
import leb128
import time
from test_a_dir_std import tc_executable
from test_a_dir_std import generate_code_sec_tcs_c


def remove_unexecutable_i32():
    i32_add_tcs_dir = Path('./i32_add_tcs')
    for p in i32_add_tcs_dir.iterdir():
        if not tc_executable(p):
            os.system('rm {}'.format(p))


def test_mutation():
    ori_tc_path = './i32_add_tcs/i32.add_both0.wasm'
    mutate_num = 1
    new_tc_dir = './results/one_tc_result'
    paths = generate_code_sec_tcs_c(ori_tc_path, mutate_num, new_tc_dir)
    # print('-' * 30)
    # path = paths [0]
    # paths = generate_code_sec_tcs_c(path, mutate_num, new_tc_dir)



if __name__ == '__main__':
    test_mutation()
