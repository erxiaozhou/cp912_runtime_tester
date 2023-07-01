#!/home/zph/anaconda3/bin/python
import re
import sys, getopt
from pathlib import Path
from file_util import check_dir, save_json, dir_file_num
from file_util import cp_file
from concurrent import futures
import time
from tqdm import tqdm
from debug_util import is_executable_by_impl
from functools import partial
from get_impls_util import get_std_uninst_impls


def check_ori_tcs_executable(ori_tcs_dir, result_json_path, unexecutable_inst_names_path, unexecutable_files_path, func):
    inst2executable_result, unexecutable_paths = _get_inst2executable_result(ori_tcs_dir, func)
    unexecutable_list = []
    for k, v in inst2executable_result.items():
        inst2executable_result[k]['rate'] = v['executable_num'] / v['all_num']
        if v['executable_num'] == 0:
            unexecutable_list.append(k)
    save_json(unexecutable_inst_names_path, unexecutable_list)
    save_json(result_json_path, inst2executable_result)
    save_json(unexecutable_files_path, unexecutable_paths)


def _get_inst2executable_result(ori_tcs_dir, func):
    ori_tcs_dir = Path(ori_tcs_dir)
    inst2executable_result = _init_inst2executable_result(ori_tcs_dir)
    unexecutable_paths = {inst_name:[] for inst_name in inst2executable_result.keys()}

    total_num = dir_file_num(ori_tcs_dir)
    for p in tqdm(ori_tcs_dir.iterdir(), total=total_num):
            if p.suffix != '.wasm':
                continue
            executable, p = func(p)
            inst_name = _get_inst_name_from_path(p)
            if executable:
                inst2executable_result[inst_name]['executable_num'] += 1
            else:
                unexecutable_paths[inst_name].append(str(p))
    return inst2executable_result, unexecutable_paths


def _init_inst2executable_result(ori_tcs_dir):
    inst2executable_result = {}
    for p in ori_tcs_dir.iterdir():
        if p.suffix != '.wasm':
            continue
        inst_name = _get_inst_name_from_path(p)
        if inst_name not in inst2executable_result:
            inst2executable_result[inst_name] = {
                'executable_num': 0,
                'all_num': 0
            }
        inst2executable_result[inst_name]['all_num'] += 1
    return inst2executable_result


def _get_inst_name_from_path(p):
    assert p.suffix == '.wasm'
    stem = p.stem
    inst_name = re.sub(r'_\d+$', '', stem)
    return inst_name


def _get_name_executable_info_impl(impl, p):
    executable = is_executable_by_impl(impl, p)
    return (executable, p)


def _run_one_runtime(result_base_dir, ori_tcs_dir, runtime_config):
    start_time = time.time()
    runtime_name = runtime_config['name']
    runtime_func = runtime_config['func']

    result_base_dir = check_dir(result_base_dir / runtime_name)
    result_json_path = result_base_dir / 'executable_summary.json'
    unexecutable_inst_names_path = result_base_dir / 'unexecutable_inst_names.json'
    unexecutable_files_path = result_base_dir / 'unexcutable_paths.json'
    check_ori_tcs_executable(ori_tcs_dir, result_json_path, unexecutable_inst_names_path, unexecutable_files_path, runtime_func)
    print('Time consuming of {}: {}'.format(runtime_name, time.time() - start_time))
    # copy unexecutable_inst_names file to the parent dir; and rename it
    cp_file(unexecutable_inst_names_path, result_base_dir.parent / (runtime_name + '_unexecutable_inst_names.json'))


def _run_all_runtime(result_base_dir, ori_tcs_dir, runtime_configs):
    with futures.ProcessPoolExecutor(max_workers=10) as executor:
        for runtime_config in runtime_configs:
            executor.submit(_run_one_runtime, result_base_dir, ori_tcs_dir, runtime_config)
    # for result_base_dir, ori_tcs_dir in zip(result_base_dirs, ori_tcs_dirs):
    #     for runtime_config in runtime_configs:
    #         _run_one_runtime(result_base_dir, ori_tcs_dir, runtime_config)


def _get_paras():
    argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:], "hi:o:",["input_dir=","outpur_dir="])
    except getopt.GetoptError:
        print('{} -i <input_dir> -o <output_dir>'.format(argv[0]))
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('{} -i <input_dir> -o <output_dir>'.format(argv[0]))
            sys.exit()
        elif opt in ("-i", "--ifile"):
            ori_tcs_dir = arg
        elif opt in ("-o", "--ofile"):
            result_base_dir = arg
    return check_dir(result_base_dir), ori_tcs_dir


if __name__ == '__main__':
    start_time = time.time()
    result_base_dir, ori_tcs_dir = _get_paras()
    runtime_configs = []
    
    uninst_impls = get_std_uninst_impls()
    uninst_impls_dict = {impl.name: impl for impl in uninst_impls}
    for impl in uninst_impls:
        runtime_configs.append({
            'name': impl.name,
            'func': partial(_get_name_executable_info_impl, impl)
        })

    # for runtime_config in runtime_configs:
    #     print('Start checking {}'.format(runtime_config['name']))
    #     _run_one_runtime(result_base_dir, ori_tcs_dir, runtime_config)
    _run_all_runtime(result_base_dir, ori_tcs_dir, runtime_configs)
    print(result_base_dir)
