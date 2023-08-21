#!/home/zph/anaconda3/bin/python
from pathlib import Path
import re
from extract_dump import are_different, at_least_one_can_instantiate
from exec_util import exec_one_tc, exec_one_tc_mth
from extract_dump import dumpData
from file_util import check_dir
from file_util import print_ba
from get_impls_util import get_std_impls
import os
import sys
from stack_val_analyze.stack_val_analyze_util import cleanedStackVal
from extract_dump.analyze_exec_instant import _get_can_execute_num
from get_impls_util import get_std_release_impls
debug_impls = get_std_impls()
# release_impls = get_std_release_impls()


def test_env(tc_name, reload=False, reload_dir=None, use_release=False):
    if use_release:
        # impls = release_impls
        pass
    else:
        impls = debug_impls
    for impl in impls:
        print(impl.executor.dump_cmd_fmt)
        print(impl.executor._result_paths)
    if Path(tc_name).exists():
        tc_path = tc_name
        tc_name = Path(tc_name).stem
    else:
        tc_path = 'tcs/{}.wasm'.format(tc_name)
    if reload:
        reload_dir = Path(reload_dir)
        name = Path(tc_path).name
        name = re.sub(r'\.wasm', '', name)
        tc_dumped_data_dir = reload_dir / name
        print(tc_dumped_data_dir)
    else:
        result_base_dir = 'results/one_tc_result'
        os.system('rm -rf {}'.format(result_base_dir))
        result_base_dir = check_dir(result_base_dir)
        tc_dumped_data_dir = check_dir(result_base_dir / tc_name)
    dumped_results = exec_one_tc_mth(impls, tc_path, tc_dumped_data_dir, tc_dumped_data_dir)
    # dumped_results = exec_one_tc(impls, tc_path, tc_dumped_data_dir, tc_dumped_data_dir)
    # print(dumped_results)
    # 
    for dumped_result in  dumped_results:
        print(f'dumped_result.name: {dumped_result.name};;dumped_result.can_initialize: {dumped_result.can_initialize} ;; dumped_result.has_crash: {dumped_result.has_crash} {dumped_result.log_has_failed_content}')
        print(dumped_result.stack_bytes_process_nan)
        if dumped_result.name == 'wasm3_dump':
            print('wasm3_dump')
            print(dumped_result.default_mem_length, dumped_result.mem_num, dumped_result.default_mem_page_num)
            print('------------------')
        if dumped_result.name == 'wasmer_default_dump':
            print('wasmer_default_dump')
            print(dumped_result.default_mem_length, dumped_result.mem_num, dumped_result.default_mem_page_num)
    print('---' * 10)
    # 
    difference_reason = are_different(dumped_results)
    # print(dumped_results)
    diff_keys = []
    if not isinstance(difference_reason, bool):
        for r in difference_reason.values():
            diff_keys.extend(r)
        print('Difference reason:')
        print(difference_reason)
    print('=' * 50)
    print(diff_keys)
    print(at_least_one_can_instantiate(dumped_results))
    print('=' * 50)
    # for result in dumped_results:
    #     assert isinstance(result, dumpData)
    #     print('-' * 25)
    #     print(result.name)
    #     print(result.can_initialize)
    #     print(result.log_content)
    # print(_get_can_execute_num(dumped_results))
    


if __name__ == '__main__':
    argv = sys.argv
    assert len(argv) == 2
    tc_path = argv[1]
    # test_env(tc_path, False, 'result/one',use_release=False)
    test_env(tc_path, False, 'result/one',use_release=False)

