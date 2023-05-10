#!/home/zph/anaconda3/bin/python
import sys
from run_dir_testing_util import detect_canrun_cannotdump, log_content_categorize
from run_dir_testing_util import set_paras_with_mutation
from run_dir_std_testing import test_with_mutation
from analyze_reslut_util import get_reason_summarys
from path_group_util import analyze_result_dirs
from stack_val_analyze import category_stack


def _test_and_analyze(result_base_dir, analyze_paths, paras, exec_paths):
    test_with_mutation(**paras)
    detect_canrun_cannotdump(exec_paths, result_base_dir)

    paths = get_reason_summarys(analyze_paths.reason_summary_base_dir, exec_paths.reason_dir)
    log_content_categorize(paths['only_exec'], analyze_paths.log_category_base_dir, exec_paths.dumped_data_base_dir)
    category_stack(paths['stack'], exec_paths.dumped_data_base_dir, analyze_paths.stack_category_base_dir)

if __name__ == '__main__':
    argv = sys.argv
    assert len(argv) in [1, 3]
    if len(argv) == 1:
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing2'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_10_200'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v4.6'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v6.2'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v8.3'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v9.6'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v10.1'
        result_base_dir = '/media/hdd_xj1/cp910_data/f64_max_base/50_5_nodatacount'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v11.1_2_50'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v12_550'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v12_250'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v12_5502'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v12_450_9811'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v12_350_9811'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v12_250_9811'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v12_250_9811_2'
        result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v125_250_9811'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811_2'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811_2'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811_3'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811_4'
        result_base_dir = '/media/ssd_wd1/cp910_data/only_i32_add_550_9811'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v13_550_9811_2'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v14_350_9811_2'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v14.1_550_9811_2'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v14.1_550_9811_3'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v14.1_450_9811'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v14.1_550_9811_p10MC'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v14.1_550_9811_p10MC2'
        result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_store_sub_550_9811_p10MC2'
        # result_base_dir = '/media/ssd_wd1/cp910_data/testing'
        # result_base_dir = 'tt/tmp_tcs_r'
        tested_dir = '../spec/extract_document/test_tcs/f64.max'
        tested_dir = './ori_tcs/tcs_v11'
        tested_dir = './ori_tcs/testing'
        tested_dir = './ori_tcs/v12_5'
        tested_dir = './ori_tcs/only_i32_add/tcs'
        tested_dir = './ori_tcs/v13'
        tested_dir = './ori_tcs/v14.1'
        tested_dir = './ori_tcs/i32_store_sub'
        # tested_dir = './tt/tmp_tcs'
    else:
        reason_base_dir = argv[1]
        tested_dir = argv[2]


    result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_store_sub_550_9811_p10MC2_2'
    tested_dir = './ori_tcs/i32_store_sub'
    result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v14.1_340_9811_p50MC' #560
    tested_dir = './ori_tcs/v14.1'
    result_base_dir = '/media/ssd_wd1/cp910_data/v14.1_empty_tcs_340_9811' #560
    tested_dir = 'ori_tcs/v14.1_empty_tcs'
    result_base_dir = '/media/ssd_wd1/cp910_data/v15_debug_empty_tcs_560_9811_p50MC' #560
    tested_dir = 'ori_tcs/debug_v15'
    result_base_dir = '/media/ssd_wd1/cp910_data/v15_debug_empty_tcs_560_9811_p50MC' #560
    result_base_dir = '/media/ssd_wd1/cp910_data/v15_debug_empty_tcs_5100_9811_p50MC' #560
    tested_dir = 'ori_tcs/v16'
    # analyze_paths = analyze_result_dirs(result_base_dir)
    # paras, exec_paths = set_paras_with_mutation(tested_dir, result_base_dir, one_tc_limit=100, mutate_num=5, p10_mutate_coarse=0.5)
    # _test_and_analyze(result_base_dir, analyze_paths, paras, exec_paths)

    result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_store_sub_250_9811_2'
    tested_dir = './ori_tcs/i32_store_sub'
    result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v14.1_340_9811_3'
    tested_dir = './ori_tcs/v14.1'
    result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v16_340_9811_2'
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v18_330_9811_2'
    tested_dir = 'ori_tcs/v18'
    # analyze_paths = analyze_result_dirs(result_base_dir)
    # paras, exec_paths = set_paras_with_mutation(tested_dir, result_base_dir, one_tc_limit=40, mutate_num=3, p10_mutate_coarse=None, use_release=False)
    # _test_and_analyze(result_base_dir, analyze_paths, paras, exec_paths)

    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v17_340_9811_release'
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v18_330_9811_release'
    tested_dir = 'ori_tcs/v17'
    tested_dir = 'ori_tcs/v18'
    # analyze_paths = analyze_result_dirs(result_base_dir)
    # paras, exec_paths = set_paras_with_mutation(tested_dir, result_base_dir, one_tc_limit=30, mutate_num=3, p10_mutate_coarse=None, use_release=True)
    # _test_and_analyze(result_base_dir, analyze_paths, paras, exec_paths)


    
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v18.1_340_9811_no_mutation'
    tested_dir = 'ori_tcs/v18.1'
    analyze_paths = analyze_result_dirs(result_base_dir)
    paras, exec_paths = set_paras_with_mutation(tested_dir, result_base_dir, one_tc_limit=40, mutate_num=3, p10_mutate_coarse=0.0, use_release=False)
    _test_and_analyze(result_base_dir, analyze_paths, paras, exec_paths)
