from pathlib import Path
from file_util import rm_dir
from analyze_reslut_util import reasonSummary
from analyze_reslut_util import dumped_data_base_dir2reason_base_dir
from run_dir_testing import log_content_categorize
from run_dir_testing import detect_canrun_cannotdump
from run_dir_testing import test_with_mutation
from run_dir_testing import mutationParas
from path_group_util import analyzeResultDirs
from run_dir_testing.tester_util import testerExecPaths
from get_impls_util import get_std_impls


def rewrite_reason_base_dir_by_dumped_data_base_dir_core(reason_base_dir, dumped_data_base_dir):
    if Path(reason_base_dir).exists():
        rm_dir(reason_base_dir)
    dumped_data_base_dir = Path(dumped_data_base_dir)
    dumped_data_base_dir2reason_base_dir(dumped_data_base_dir, reason_base_dir)


def rewrite_reason_base_dir_by_dumped_data_base_dir(result_base_dir, rewrite_reason_summary=True):
    # reason_base_dir = '/media/hdd_xj1/cp910_data/main_testing/reasons'
    # dumped_data_base_dir = '/media/hdd_xj1/cp910_data/main_testing/result'
    result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811_3'
    exec_paths = testerExecPaths.from_result_base_dir(result_base_dir)
    reason_base_dir = exec_paths.reason_dir
    dumped_data_base_dir = exec_paths.dumped_data_base_dir
    rewrite_reason_base_dir_by_dumped_data_base_dir_core(reason_base_dir, dumped_data_base_dir)
    if rewrite_reason_summary:
        analyze_result_ps = analyzeResultDirs(result_base_dir)
        reason_summary_base_dir = analyze_result_ps.reason_summary_base_dir
        if Path(reason_summary_base_dir).exists():
            rm_dir(reason_summary_base_dir)
        reasonSummary(reason_summary_base_dir, reason_base_dir, exec=True)


def rewrite_reason_log_category_by_dumped_data_base_dir(result_base_dir):
    exec_paths = testerExecPaths.from_result_base_dir(result_base_dir)
    reason_base_dir = exec_paths.reason_dir
    dumped_data_base_dir = exec_paths.dumped_data_base_dir
    rm_dir(reason_base_dir)
    dumped_data_base_dir2reason_base_dir(dumped_data_base_dir, reason_base_dir)

    analyze_result_ps = analyzeResultDirs(result_base_dir)
    reason_summary_base_dir = analyze_result_ps.reason_summary_base_dir
    log_category_base_dir = analyze_result_ps.log_category_base_dir
    rm_dir(reason_summary_base_dir)
    rm_dir(log_category_base_dir)
    reason_summary = reasonSummary(reason_summary_base_dir, reason_base_dir, exec=True)
    log_content_categorize(reason_summary.only_exec_smry_path, log_category_base_dir, dumped_data_base_dir, modes=['all', 's1', 's2', 's3', 'only_interesting', 'only_highlight'])


def rewrite_dumped_data_base_dir_by_re_exec_diff_tcs(result_base_dir, re_exec_result_dir, impls, rewrite_ori_dumped_data=False, remove_re_exec_result_dir=False):
    ori_exec_paths = testerExecPaths.from_result_base_dir(result_base_dir)
    paras = mutationParas.get_no_mutation_paras(re_exec_result_dir, ori_exec_paths.diff_tc_dir, impls=impls)
    test_with_mutation(paras)
    new_paths = paras.tester_exec_paths
    detect_canrun_cannotdump(new_paths, re_exec_result_dir)

    new_result_ps = analyzeResultDirs(re_exec_result_dir)
    new_reason_summary_base_dir = new_result_ps.reason_summary_base_dir
    new_log_category_base_dir = new_result_ps.log_category_base_dir
    reason_summary = reasonSummary(new_reason_summary_base_dir, new_paths.reason_dir)
    log_content_categorize(reason_summary.only_exec_smry_path, new_log_category_base_dir, new_paths.dumped_data_base_dir, modes=['all', 's1', 's2', 's3', 'only_interesting', 'only_highlight'])
    if rewrite_ori_dumped_data:
        ori_result_ps = analyzeResultDirs(result_base_dir)
        data_pairs = [
            [ori_result_ps.reason_summary_base_dir, new_reason_summary_base_dir],
            [ori_result_ps.log_category_base_dir, new_log_category_base_dir],
            [ori_exec_paths.dumped_data_base_dir, new_paths.dumped_data_base_dir], 
            [ori_exec_paths.reason_dir, new_paths.reason_dir]
        ]
        for ori_dir, new_dir in data_pairs:
            if Path(ori_dir).exists():
                rm_dir(ori_dir)
                Path(new_dir).rename(ori_dir)
    if remove_re_exec_result_dir:
        rm_dir(re_exec_result_dir)


if __name__ == '__main__':
    impls = get_std_impls()
    rewrite_dumped_data_base_dir_by_re_exec_diff_tcs('/media/ssd_wd1/cp910_data/main_testing_v125_350_9811_2', '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811_2/re_exec', impls, True, False)
    # rewrite_dumped_data_base_dir_by_re_exec_diff_tcs('/media/ssd_wd1/cp910_data/main_testing_v125_350_9811_3', '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811_3/re_exec', True, False)
    # rewrite_reason_log_category_by_dumped_data_base_dir('/media/ssd_wd1/cp910_data/main_testing_v125_350_9811_3')
