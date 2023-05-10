from pathlib import Path
import re
from file_util import read_json, save_json, path_read, path_write
from debug_util import get_log_by_impl, is_executable_by_impl
from script_compare_wasm import compare_2wasms


base_dir = Path('/media/ssd_wd1/cp910_data/only_i32_add_550_9811')
diff_tcs_base_dir = base_dir / 'diff_tcs'
ori_tcs_base_dir = Path('/home/zph/DGit/wasm_projects/runtime_tester/ori_tcs/only_i32_add/tcs')
stack_diff_tc_names_json_path = base_dir / 'stack_category_base/2.json'

c5_case_path= '/home/zph/DGit/wasm_projects/runtime_tester/for_motivation_example/i32add_in_me_c5.wasm'
wasmedge_section_size_mismatch_json_path = '/media/ssd_wd1/cp910_data/only_i32_add_550_9811/log_category_base/only_interesting_log_category/5.json'


def print_c5_case_log():
    assert is_executable_by_impl('iwasm_classic_interp_dump', c5_case_path)
    assert is_executable_by_impl('iwasm_fast_interp_dump', c5_case_path)
    iwasm_classic_log = get_log_by_impl('iwasm_classic_interp_dump', c5_case_path, 'stdout')
    iwasm_fast_log = get_log_by_impl('iwasm_fast_interp_dump', c5_case_path, 'stdout')
    print('iwasm_classic_log:', iwasm_classic_log, '\n', '-'*20)
    print('iwasm_fast_log:', iwasm_fast_log, '\n', '-'*20)
    '''
    iwasm_classic_log: 0x0:i32 
    --------------------
    iwasm_fast_log: 0x5:i32 
    --------------------
    '''

def analyze_wasmedge_section_size_mismatch():
    diff_tc_stems = list(read_json(wasmedge_section_size_mismatch_json_path).values())[0]
    name_p = r'^(i32\.add_\d+)_\d+_\d+$'
    name_p = re.compile(name_p)
    for diff_tc_stem in diff_tc_stems:
        diff_tc_name = f'{diff_tc_stem}.wasm'
        diff_tc_path = diff_tcs_base_dir / diff_tc_name
        print(diff_tc_stem)
        ori_tc_stem = name_p.findall(diff_tc_stem)[0]
        ori_tc_name = f'{ori_tc_stem}.wasm'
        ori_tc_path = ori_tcs_base_dir / ori_tc_name
        assert diff_tc_path.exists()
        assert ori_tc_path.exists()
        compare_2wasms(diff_tc_path, ori_tc_path)
        print('*'*20)
        # assert 0


