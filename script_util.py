#!/home/zph/anaconda3/bin/python
import os
from pathlib import Path
import random
import struct
from debug_util import wasm2wat
from extract_dump.extractor import is_failed_content
from file_util import check_dir, cp_file, pickle_dump, pickle_load, read_bytes, remove_file_without_exception, rm_dir, save_json, write_bytes
import numpy as np
from file_util import path_read
from file_util import path_write
import leb128
import time

from run_dir_std_testing import tc_executable

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

def get_inst_tcs(tgt_dir, inst_name, base_dir='./ori_tcs/tcs_v8'):
    tgt_dir = Path(tgt_dir)
    check_dir(tgt_dir)
    base_dir = Path(base_dir)
    name_fmt = inst_name + '_{}.wasm'
    idx = 0
    while True:
        name = name_fmt.format(idx)
        ori_path = base_dir / name
        if ori_path.exists():
            new_path = tgt_dir / name
            cp_file(ori_path, new_path)
            idx += 1
        else:
            break


def get_executable_tcs(base_dir, result_dir):
    base_dir = Path(base_dir)
    result_dir = check_dir(result_dir)
    for wasm_path in base_dir.iterdir():
        name = wasm_path.name
        if tc_executable(wasm_path):
            new_path = result_dir / name
            cp_file(wasm_path, new_path)


def wasms_dir2wats(base_dir, result_dir):
    base_dir = Path(base_dir)
    result_dir = check_dir(result_dir)
    for wasm_path in base_dir.iterdir():
        print(wasm_path)
        stem = wasm_path.name[:-5]
        wat_path = result_dir / (stem+'.wat')
        wasm2wat(wasm_path, wat_path)


if __name__ == '__main__':
    # generate_f32_abs_wats()
    all_tcs_dir = './ori_tcs/tcs_v8'
    all_tcs_dir = '../spec/extract_document/f32_test'
    inst_name = 'f32.add'
    f32_add_base_dir = Path('./ori_tcs/f32_add')
    f32_add_all_tcs_dir = f32_add_base_dir / 'all_tcs'
    f32_add_executable_dir = f32_add_base_dir / 'executable'
    f32_add_wats_dir = f32_add_base_dir / 'wats'
    get_inst_tcs(f32_add_all_tcs_dir, inst_name, all_tcs_dir)
    get_executable_tcs(f32_add_all_tcs_dir, f32_add_executable_dir)
    wasms_dir2wats(f32_add_executable_dir, f32_add_wats_dir)

