import os
import random
import time
from pathlib import Path
from byte_seq_mask_mutator import mutate_with_mask
from data_comparer import are_different, at_least_one_can_dump
from exec_util import exec_one_tc, exec_one_tc_mth, get_reason_dir
from file_util import (check_dir, cp_file, get_time_string, rm_dir, save_json,
                       write_bytes)
from generate_wasm_tc import _prepare_template, get_wasm_bytes_from_dict, read_next_leb_num
from exec_util import get_wasms_from_a_path
from get_imlps_util import get_std_imlps
from util_get_mask import get_wasm_mask
import leb128
from analyze_reslut_util import get_reason_summary


def _tc_name_generator(ori_tc_path, num, new_tc_dir):
    new_tc_dir = Path(new_tc_dir)
    ori_name = Path(ori_tc_path).name
    assert ori_name.endswith('.wasm')
    stem = ori_name[:-5]
    if stem.count('_') < 2:
        ori_stem = stem
        start_idx = 0
    else:
        follow_underline = stem.split('_')[-2]
        before_underline = '_'.join(stem.split('_')[:-2])
        assert isinstance(follow_underline, str)
        if follow_underline.isdigit():
            start_idx = int(follow_underline) + 1
            ori_stem = before_underline
        else:
            ori_stem = stem
            start_idx = 0
    paths = []
    for i in range(num):
        idx = start_idx + i
        time_str = str(time.time()).replace('.', '')
        new_name = '{}_{}_{}.wasm'.format(ori_stem, idx, time_str)
        path = str(new_tc_dir/new_name)
        paths.append(path)
    return paths


def first_func_info(ori_code_sec):
    func_num, offset = read_next_leb_num(ori_code_sec, offset=0)
    before_func = ori_code_sec[:offset]
    func1_len, offset = read_next_leb_num(ori_code_sec, offset=offset)
    func_body = ori_code_sec[offset:func1_len + offset]
    content_after_func1 = ori_code_sec[func1_len + offset:]
    return before_func, func_body, content_after_func1


def generate_code_sec_tcs(ori_tc_path, mutate_num, new_tc_dir):
    new_tc_dir = Path(new_tc_dir)
    sec_template = _prepare_template(ori_tc_path)
    ori_code_sec = bytearray(sec_template['code'])
    # 
    before_func, ori_func_body, content_after_func1 = first_func_info(ori_code_sec)
    #
    print('ori_tc_path', ori_tc_path)
    print(content_after_func1)
    # 
    masks = get_wasm_mask(ori_func_body + content_after_func1)
    change_num = 1  # random.randint(1,3)
    paths = _tc_name_generator(ori_tc_path, mutate_num, new_tc_dir)
    assert len(paths) == mutate_num
    for i, new_path in enumerate(paths):
        func_body = bytearray(ori_func_body)
        for c in range(change_num):
            func_body = mutate_with_mask(func_body, masks)
            # 
        func1_len = len(func_body) + random.choices([-1, 0, 1], [0.05, 0.9, 0.05], k=1)[0]
        func1_len_ba = leb128.u.encode(func1_len)
        sec_template['code'] = before_func +func1_len_ba+ func_body + content_after_func1
        wasm_bytes = get_wasm_bytes_from_dict(sec_template)
        assert not Path(new_path).exists()
        write_bytes(new_path, wasm_bytes)
    return paths

def _print_ba(ba):
    ba = bytearray(ba)
    print([hex(x) for x in ba])

# def generate_code_sec_tcs_c(ori_tc_path, mutate_num, new_tc_dir):
#     new_tc_dir = Path(new_tc_dir)
#     sec_template = _prepare_template(ori_tc_path)
#     ori_code_sec = bytearray(sec_template['code'])
#     # 
#     before_func, ori_func_body, content_after_func1 = first_func_info(ori_code_sec)
#     print('before_func')
#     _print_ba(before_func)
#     print('ori_func_body')
#     _print_ba(ori_func_body)
#     print(len(ori_func_body))
#     print('content_after_func1')
#     _print_ba(content_after_func1)
#     print('ori_code_sec')
#     _print_ba(ori_code_sec)
#     print(len(ori_code_sec))
#     #
#     masks = get_wasm_mask(ori_code_sec)
#     # print(masks)
#     change_num = 1  # random.randint(1,3)
#     paths = _tc_name_generator(ori_tc_path, mutate_num, new_tc_dir)
#     assert len(paths) == mutate_num
#     for i, new_path in enumerate(paths):
#         func_body = bytearray(ori_func_body)
#         for c in range(change_num):
#             func_body = mutate_with_mask2(func_body, masks)
#             # 
#         # func1_len = len(func_body) + random.choices([-1, 0, 1], [0.05, 0.9, 0.05], k=1)[0]
#         func1_len = len(func_body)
#         #  + random.choices([-1, 0, 1], [0.05, 0.9, 0.05], k=1)[0]
#         func1_len_ba = leb128.u.encode(func1_len)
#         sec_template['code'] = before_func +func1_len_ba+ func_body + content_after_func1
#         wasm_bytes = get_wasm_bytes_from_dict(sec_template)
#         assert not Path(new_path).exists()
#         write_bytes(new_path, wasm_bytes)
#     return paths

def tc_executable(tc_path):
    imlps = get_std_imlps()
    tc_name = Path(tc_path).stem
    tc_result_dir = 'results/one_tc_result'
    dumped_results = exec_one_tc(imlps, tc_name, tc_path, tc_result_dir, tc_result_dir)
    if at_least_one_can_dump(dumped_results):
        return True
    else:
        return False

def test_with_mutation(tested_dir, new_tc_dir, diff_tc_dir, result_dir, config_log_path, reason_dir, one_tc_limit = 6000, mutate_num = 60, except_dir='except_dir', skip_common_diff=False, add_mutation=True):
    imlps = get_std_imlps()
    assert not Path(result_dir).exists()
    # os.system('rm -rf {}'.format(result_dir))
    result_dir = check_dir(result_dir)
    new_tc_dir = check_dir(new_tc_dir)
    diff_tc_dir = check_dir(diff_tc_dir)
    tc_paths = get_wasms_from_a_path(tested_dir)
    except_tc_dir = check_dir(except_dir)
    reason_dir = check_dir(reason_dir)
    # tc execution info
    exec_info = {
        'ori_tc_num': 0,
        'all_exec_times': 0,
        'at_least_one_can_dump': 0,
        'difference_num': 0
    }
    assert isinstance(reason_dir, Path)
    start_time = time.time()
    for tc_name, tc_path in tc_paths:
        exec_info['ori_tc_num'] += 1
        possible_m = [tc_path]
        generated_tc_num = 0
        while possible_m:
            tc_path = possible_m.pop()
            tc_name = Path(tc_path).stem
            tc_result_dir = check_dir(result_dir / tc_name)
            try:
                print(tc_path)
                # assert 0
                dumped_results = exec_one_tc_mth(imlps, tc_name, tc_path, tc_result_dir, tc_result_dir)
                # dumped_results = exec_one_tc(imlps, tc_name, tc_path, tc_result_dir, tc_result_dir)
                exec_info['all_exec_times'] += 1
                difference_reason = are_different(dumped_results, tc_name, skip_common_diff )
                # print(_get_can_init_num(dumped_results))
                # input()
                # ! 重新考虑 difference_reason 
                # if all_can_dump(dumped_results) and (not difference_reason):
                # assert 0, print(_get_can_init_num(dumped_results), at_least_one_can_dump(dumped_results))
                if at_least_one_can_dump(dumped_results):
                    exec_info['at_least_one_can_dump'] += 1
                    if add_mutation and (one_tc_limit > generated_tc_num):
                        paths = generate_code_sec_tcs(tc_path, mutate_num, new_tc_dir)
                        generated_tc_num += mutate_num
                        possible_m.extend(paths)
                if difference_reason:
                    exec_info['difference_num'] += 1
                    cp_file(tc_path, diff_tc_dir)
                    json_file_name = ''.join((tc_name, '.json'))
                    json_path = reason_dir / json_file_name
                    save_json(json_path, difference_reason)
                else:
                    rm_dir(tc_result_dir)
                # * 这么做是假设tc_path不会再被用到
                # if Path(tc_path).is_relative_to(new_tc_dir):
                #     remove_file_without_exception(tc_path)
                
            except AssertionError as e:
                raise e
            except Exception as e:
                # raise e
                cp_file(tc_path, except_tc_dir)
    end_time = time.time()
    # save config
    config_log = {
        'tested_dir': str(tested_dir),
        'new_tc_dir': str(new_tc_dir),
        'dumped_result_dir': str(result_dir),
        'except_dir': str(except_dir),
        'reason_dir': str(reason_dir),
        'runtimes': [imlp.name for imlp in imlps],
        'one_tc_limit': one_tc_limit,
        'mutate_num': mutate_num,
        'skip_common_diff': skip_common_diff,
        'exec_info': exec_info,
        'exection_time': end_time - start_time
    }
    save_json(config_log_path, config_log)
    # back up config file
    config_stem = Path(config_log_path).stem
    config_base_dir = Path(config_log_path).parent
    config_backup_name = ''.join((config_stem, get_time_string(), '.json'))
    config_backup_path = config_base_dir / config_backup_name
    save_json(config_backup_path, config_log)


if __name__ == '__main__':
    tested_dir = './ori_tcs/test_work_tcs'
    # tested_dir = 'one_i32add'
    new_tc_dir = '/media/hdd_xj1/all_tcs/test_std_new_tcs'
    result_dir = './results/test_std/result'
    diff_tc_dir = './results/test_std/diff_tcs'
    except_dir = './results/test_std/except_dir'
    config_log_path = './results/test_std/config_log.json'
    reason_dir = './results/test_std/reasons'
    paras = {
        'tested_dir': tested_dir,  # 输入
        'new_tc_dir': new_tc_dir,  # 生成的所有 test case
        'result_dir': result_dir,  # 有difference的数据, pkl, log什么的
        'diff_tc_dir': diff_tc_dir,  # 有difference 的 tc
        'except_dir': except_dir,  # 造成except的 tc
        'config_log_path': config_log_path,
        'reason_dir': reason_dir,
        'one_tc_limit': 50,
        'mutate_num': 5,
        'skip_common_diff': False
    }
    test_with_mutation(**paras)
    get_reason_summary(reason_dir, './results/test_std/reason_summary.json')