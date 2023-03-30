from run_dir_std_testing import test_with_mutation
from run_dir_testing_util import log_content_categorize
from analyze_reslut_util import get_reason_summarys
from run_dir_testing_util import detect_canrun_cannotdump
from run_dir_testing_util import get_no_mutation_paras
from path_group_util import analyze_result_dirs
from stack_val_analyze import category_stack

def general_main():
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing/rerun_diff'
    tested_dir = '/media/hdd_xj1/cp910_data/main_testing/diff_tcs'


def test_findings():
    result_base_dir = 'results/CP910_findings'
    tested_dir = 'CP910_findings/wasms'


def test_previous_tcs():
    # result_base_dir = '/media/hdd_xj1/cp910_data/previous_tcs/result_previous_tcs_in_one'
    result_base_dir = '/media/hdd_xj1/cp910_data/previous_tcs/previous_tcs_in_one_result'
    tested_dir = '/media/hdd_xj1/cp910_data/previous_tcs/previous_tcs_in_one'


if __name__ == '__main__':
    result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/re_exec'
    tested_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/except_dir'
    # 
    tested_dir = 'ori_tcs/testing_f32_add'
    result_base_dir = 'tt/testing_f32_add_result'
    # 
    analyze_paths = analyze_result_dirs(result_base_dir)
    paras, exec_paths = get_no_mutation_paras(result_base_dir, tested_dir)
    test_with_mutation(**paras)
    detect_canrun_cannotdump(exec_paths, result_base_dir)
    reason_base_dir = exec_paths.reason_dir
    paths = get_reason_summarys(analyze_paths.reason_summary_base_dir, reason_base_dir)
    log_content_categorize(paths['only_exec'], analyze_paths.log_category_base_dir, exec_paths.dumped_data_base_dir)
    category_stack(paths['stack'], exec_paths.dumped_data_base_dir, analyze_paths.stack_category_base_dir)
