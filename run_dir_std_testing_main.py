#!/home/zph/anaconda3/bin/python
import sys
from run_dir_testing_util import detect_canrun_cannotdump, log_content_categorize
from run_dir_testing_util import set_paras_with_mutation
from run_dir_std_testing import test_with_mutation
from analyze_reslut_util import get_reason_summarys
from path_group_util import analyze_result_dirs


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
        tested_dir = '../spec/extract_document/test_tcs/f64.max'
        tested_dir = './ori_tcs/tcs_v11'
        tested_dir = './ori_tcs/testing'
        tested_dir = './ori_tcs/v12_5'
    else:
        reason_base_dir = argv[1]
        tested_dir = argv[2]

    # result_base_dir = '/media/hdd_xj1/cp910_data/f32_add_executable_v3'
    # tested_dir = './ori_tcs/f32_add/executable'
    analyze_result_ps = analyze_result_dirs(result_base_dir)
    paras, exec_paths = set_paras_with_mutation(tested_dir, result_base_dir, one_tc_limit=50, mutate_num=3)
    test_with_mutation(**paras)
    
    detect_canrun_cannotdump(exec_paths, result_base_dir)

    paths = get_reason_summarys(analyze_result_ps.reason_summary_base_dir, exec_paths.reason_dir)
    log_content_categorize(paths['only_exec'], analyze_result_ps.log_category_base_dir, exec_paths.dumped_data_base_dir)
