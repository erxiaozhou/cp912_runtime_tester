#!/home/zph/anaconda3/bin/python
from pathlib import Path
import re
from data_comparer import are_different, at_least_one_can_instantiate
from exec_util import exec_one_tc, exec_one_tc_mth
from extract_dump import dump_data
from file_util import check_dir
from file_util import print_ba
from get_imlps_util import get_std_imlps
import os
import sys
from stack_val_analyze.stack_val_analyze_util import cleaned_stack_val
from data_comparer import _get_can_execute_num
from get_imlps_util import get_std_release_impls
debug_imlps = get_std_imlps()
release_impls = get_std_release_impls()



def test_env(tc_name, reload=False, reload_dir=None, use_release=False):
    if use_release:
        imlps = release_impls
    else:
        imlps = debug_imlps
    for impl in imlps:
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
    dumped_results = exec_one_tc_mth(imlps, tc_path, tc_dumped_data_dir, tc_dumped_data_dir)
    # dumped_results = exec_one_tc(imlps, tc_path, tc_dumped_data_dir, tc_dumped_data_dir)
    # print(dumped_results)
    difference_reason = are_different(dumped_results)
    # print(dumped_results)
    diff_keys = []
    if not isinstance(difference_reason, bool):
        for r in difference_reason.values():
            diff_keys.extend(r)
        print('Difference reason:')
        print(difference_reason)
    print(diff_keys)
    print(at_least_one_can_instantiate(dumped_results))
    print('=' * 50)
    for result in dumped_results:
        assert isinstance(result, dump_data)
        print('-' * 25)
        print(result.name)
        print(result.can_initialize)
        # print(result.name, result.has_instance, result.default_table_len)
        # print(result.stack_types)
        print(result.log_content)
        # if not result.failed_exec:
        #     print_ba(result.stack_bytes[0])
        #     # print(result.stack_infered_vals[0])
        #     print(cleaned_stack_val.from_dump_data(result).key)
        #     print(result.failed_exec)
    print(_get_can_execute_num(dumped_results))
    
        # print(result.stack_bytes)
        # if result.stack_bytes:
        #     print([hex(x) for x in result.stack_bytes[0]])
        # print('Content ', '-' * 30)
        
        # for diff_key in diff_keys:
        #     print('>    {}: {}'.format(diff_key, getattr(result, diff_key)))


if __name__ == '__main__':
    # test_env('i32.store16_465')
    # test_env('/home/zph/DGit/wasm_projects/runtime_tester/diff_tcs/i64.ge_u_4_98_98_99_99_96_97_80_98_95_96_87_95_69.wasm')
    # test_env('./test_nan/tt.wasm')
    # test_env('diff_tcs/i32.rotl_83_90_96_99_96_85_98_58.wasm')
    # test_env('diff_tcs4/f64.max_151_4_13_18_2_17_18_19_16_13_16_0_12_14_12_1.wasm')
    # test_env('./diff_tcs4/i32.store_1160_8_1_0_16_4_13_0_19_9_11_12_17_19_18_6_7_7_5.wasm')
    # test_env('tt.wasm')
    # test_env('./diff_tcs/i32.rotl_88_96_93_98_95_99_93_97_99_97_98_97_91_90_99_98_94_88_99_98_99_98_95_93_96_96_93_86_48_88_0_35.wasm')
    # test_env('/media/hdd_xj1/all_tcs/test_std_new_tcs/i32.add_0_7_16744796413940542.wasm', False, 'result/one')
    argv = sys.argv
    assert len(argv) == 2
    tc_path = argv[1]
    # test_env(tc_path, False, 'result/one',use_release=False)
    test_env(tc_path, False, 'result/one',use_release=True)

