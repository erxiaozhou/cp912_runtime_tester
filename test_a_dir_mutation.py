import os
import random
from pathlib import Path
from concurrent import futures
from byte_seq_mutator import mutate
from data_comparer import all_can_dump, are_different
from exec_util import exec_one_tc_mth, get_imlp_combine_name, get_reason_dir, get_reason_path_to_save
from file_util import (check_dir, cp_file, read_bytes,
                       remove_file_without_exception, rm_dir, save_json,
                       write_bytes)
from generate_wasm_tc import _prepare_template, get_wasm_bytes_from_dict
from impl_paras import impl_paras
from test_a_dir import exec_one_tc
from wasm_impls import common_runtime


def get_wasms_from_a_path(dir_):
    tc_paths = []
    dir_ = Path(dir_)
    for p in dir_.iterdir():
        if p.suffix == '.wasm':
            path = str(p)
            tc_name = p.stem
            tc_paths.append((tc_name, path))
    return tc_paths


def get_imlps():
    imlp_names = list(impl_paras.keys())
    imlps = []
    for name in imlp_names:
        if 'wasm3' in name:
            continue
        imlp = common_runtime.from_dict(name, impl_paras[name])
        imlps.append(imlp)
    return imlps


def mutate_and_write(ori_seq, new_path, change_num):
    new_seq = bytearray(ori_seq)
    for _ in range(change_num):
        new_seq = mutate(new_seq)
    write_bytes(new_path, new_seq)


def generate_tcs(ori_tc_path, mutate_num, new_tc_dir):
    new_tc_dir = Path(new_tc_dir)
    ori_name = Path(ori_tc_path).stem
    if len(ori_name) > 100:
        return []
    seq = read_bytes(ori_tc_path)
    change_num = random.randint(1,3)
    paths = []
    to_do = []
    with futures.ProcessPoolExecutor(max_workers=20) as executor:
        for i in range(mutate_num):
            name = '{}_{}.wasm'.format(ori_name, i)
            new_path = str(new_tc_dir/name)
            future = executor.submit(mutate_and_write, seq, new_path, change_num)
            to_do.append(future)
            paths.append(new_path)
        for future in futures.as_completed(to_do):
            pass
    return paths


def generate_code_sec_tcs(ori_tc_path, mutate_num, new_tc_dir):
    new_tc_dir = Path(new_tc_dir)
    ori_name = Path(ori_tc_path).stem
    if len(ori_name) > 150:
        return []
    sec_template = _prepare_template(ori_tc_path)
    ori_code_sec = sec_template['code']
    change_num = random.randint(1,3)
    paths = []
    for i in range(mutate_num):
        code_sec = bytearray(ori_code_sec)
        name = '{}_{}.wasm'.format(ori_name, i)
        new_path = str(new_tc_dir/name)
        for c in range(change_num):
            code_sec = mutate(code_sec)
        sec_template['code'] = bytearray(code_sec)
        wasm_bytes = get_wasm_bytes_from_dict(sec_template)
        write_bytes(new_path, wasm_bytes)
        paths.append(new_path)
    return paths

def test_env(tested_dir, new_tc_dir, diff_tc_dir, result_dir, one_tc_limit = 6000, cur_generate_num = 60):
    imlps = get_imlps()
    os.system('rm -rf {}'.format(result_dir))
    result_dir = check_dir(result_dir)
    new_tc_dir = check_dir(new_tc_dir)
    diff_tc_dir = check_dir(diff_tc_dir)
    
    # reasons = {}
    tc_paths = get_wasms_from_a_path(tested_dir)
    except_tc_dir = check_dir('except_dir')
    reason_dir = get_reason_dir(tested_dir, imlps, 'mutation')
    reason_dir = check_dir(reason_dir)
    for tc_name, tc_path in tc_paths:
        print(tc_path)
        possible_m = [tc_path]
        generated_tc_num = 0
        while possible_m:
            tc_path = possible_m.pop()
            tc_name = Path(tc_path).stem
            tc_result_dir = check_dir(result_dir / tc_name)
            try:
                dumped_results = exec_one_tc_mth(imlps, tc_name, tc_path, tc_result_dir, tc_result_dir)
                difference_reason = are_different(dumped_results, tc_name)
            except:
                cp_file(tc_path, except_tc_dir)
            if all_can_dump(dumped_results) and (not difference_reason):
                if one_tc_limit > generated_tc_num:
                    paths = generate_code_sec_tcs(tc_path, cur_generate_num, new_tc_dir)
                    generated_tc_num += cur_generate_num
                    possible_m.extend(paths)
            if difference_reason:
                cp_file(tc_path, diff_tc_dir)
                json_file_name = ''.join((tc_name, '.json'))
                json_path = str(reason_dir / json_file_name)
                save_json(json_path, difference_reason)
            else:
                rm_dir(tc_result_dir)
            # * 这么做是假设tc_path不会再被用到
            if Path(tc_path).is_relative_to(new_tc_dir):
                remove_file_without_exception(tc_path)


if __name__ == '__main__':
    test_env('./tcs_v2', 'mutate_tcs', 'diff_tcs8', 'result9')
    # test_env('./tcs')
