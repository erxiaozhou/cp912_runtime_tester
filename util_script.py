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

def unzip_cp910findings():
    wasms = check_dir('../CP910_findings/wasms')
    for p in Path('../CP910_findings').iterdir():
        if p.suffix == '.zip':
            os.system('unzip {}'.format(p))
    # assert 0
    for p in Path('../CP910_findings').iterdir():
        if p.suffix == '.wasm':
            os.system('mv {} {}'.format(p, wasms))


def rename_previous_tcs_to_the_same_dir():
    base_dir_list = [
        '/media/hdd_xj1/cp910_data/tcs_to_check/diff_tcs',
        '/media/hdd_xj1/cp910_data/tcs_to_check/diff_tcs_1114',
        '/media/hdd_xj1/cp910_data/tcs_to_check/diff_tcs5',
        '/media/hdd_xj1/cp910_data/tcs_to_check/diff_tcs6',
        # '/media/hdd_xj1/cp910_data/tcs_to_check/diff_tcs/wasmedge_err_files/wasm_edge_tcs',
    ]
    new_base_dir = check_dir('/media/hdd_xj1/cp910_data/previous_tcs/previous_tcs_in_one')
    for pre_p in base_dir_list:
        pre_p = Path(pre_p)
        pre_p_name = pre_p.name
        for p in pre_p.iterdir():
            if p.suffix == '.wasm':
                name = p.name
                new_name = '{}_{}'.format(pre_p_name, name)
                new_path = new_base_dir / new_name
                cp_file(p, new_path)


def remove_unexecutable_i32():
    i32_add_tcs_dir = Path('./i32_add_tcs')
    for p in i32_add_tcs_dir.iterdir():
        if not tc_executable(p):
            os.system('rm {}'.format(p))



if __name__ == '__main__':
    remove_unexecutable_i32()
