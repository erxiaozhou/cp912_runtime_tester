from debug_util import is_executable_by_impl
from exec_util import exec_one_tc_mth
from file_util import check_dir
from .analyze_data_util import analyze_data
from .std_exec_get_log import get_logs
from debug_util import get_log_by_impl
from debug_util import get_log_by_lastest_impl
from debug_util import is_executable_by_latest_impl
from get_imlps_util import get_std_imlps
from pathlib import Path

imlps = get_std_imlps()
def print_stack(tc_path):
    tc_name = Path(tc_path).stem
    result_base_dir = Path('results/one_tc_result')
    tc_dumped_data_dir = check_dir(result_base_dir / tc_name)
    dumped_results = exec_one_tc_mth(imlps, tc_path, tc_dumped_data_dir, tc_dumped_data_dir)
    for result in dumped_results:
        if not result.failed_exec:
            print(result.name)
            print(result.stack_bytes[0], result.stack_types[0])
            print('-' * 50)

def rule1():
    # 0xC5，的bug下，只有iwasm能运行，不是额外的bug
    key = "(('iwasm_classic_interp_dump', \"'f32'_False\"), ('iwasm_fast_interp_dump', \"'f32'_False_ninf\"))"
    path = '/media/hdd_xj1/cp910_data/main_testing_v17_340_9811/stack_category_base/2.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v17_340_9811/diff_tcs'
    analysis_base = analyze_data(path, key, tcs_base_dir)

    analysis_base.print_first_tc_log()
    print('*'* 50)
    print_stack(analysis_base.first_tc_path)


def rule2():
    # WAVM 出了 illegal_anan，f32, f64都有
    key = "(('WAVM_default', \"'f64'_True_illegal_anan\"), ('WasmEdge_disableAOT_newer', \"'f64'_True_anan\"), ('iwasm_classic_interp_dump', \"'f64'_True_anan\"), ('iwasm_fast_interp_dump', \"'f64'_True_anan\"), ('wasm3_dump', \"'f64'_True_anan\"), ('wasmer_default_dump', \"'f64'_True_anan\"), ('wasmi_interp', \"'f64'_True_anan\"))"
    path = '/media/hdd_xj1/cp910_data/main_testing_v17_340_9811/stack_category_base/3.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v17_340_9811/diff_tcs'
    analysis_base = analyze_data(path, key, tcs_base_dir)

    analysis_base.print_first_tc_log()
    print('*'* 50)
    print_stack(analysis_base.first_tc_path)

def rule3():
    # 很多 illegal anan..............
    key = "(('WAVM_default', \"'f64'_True_anan\"), ('WasmEdge_disableAOT_newer', \"'f64'_True_illegal_anan\"), ('iwasm_classic_interp_dump', \"'f64'_True_illegal_anan\"), ('iwasm_fast_interp_dump', \"'f64'_True_illegal_anan\"), ('wasm3_dump', \"'f64'_True_cnan\"), ('wasmer_default_dump', \"'f64'_True_anan\"), ('wasmi_interp', \"'f64'_True_illegal_anan\"))"
    path = '/media/hdd_xj1/cp910_data/main_testing_v17_340_9811/stack_category_base/4.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v17_340_9811/diff_tcs'
    analysis_base = analyze_data(path, key, tcs_base_dir)

    analysis_base.print_first_tc_log()
    print('*'* 50)
    print_stack(analysis_base.first_tc_path)

def rule4():
    # cnan间符号不同。。。f32.min的两个operand分别是inf nan就能触发
    key = "(('WAVM_default', \"'f64'_True_cnan\"), ('WasmEdge_disableAOT_newer', \"'f64'_True_cnan\"), ('iwasm_classic_interp_dump', \"'f64'_True_cnan\"), ('iwasm_fast_interp_dump', \"'f64'_True_cnan\"), ('wasm3_dump', \"'f64'_True_cnan\"), ('wasmer_default_dump', \"'f64'_True_cnan\"), ('wasmi_interp', \"'f64'_True_cnan\"))"
    path = '/media/hdd_xj1/cp910_data/main_testing_v17_340_9811/stack_category_base/5.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v17_340_9811/diff_tcs'
    analysis_base = analyze_data(path, key, tcs_base_dir)

    analysis_base.print_first_tc_log()
    print('*'* 50)
    print_stack(analysis_base.first_tc_path)

# 都是legal的，但是符号可能不同。anan处理掉后，符号成了0,和符号位为1的cnan会出现diff