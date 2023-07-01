from stack_val_analyze import category_stack
from run_dir_testing.tester_util import testerExecPaths
from analyze_reslut_util import reasonSummary
from path_group_util import analyzeResultDirs


def category_stack_of_result_base_dir(result_base_dir, category_result_dir):
    exec_paths = testerExecPaths.from_result_base_dir(result_base_dir)
    analyze_result_ps = analyzeResultDirs(result_base_dir)
    reason_summary = reasonSummary(analyze_result_ps.reason_summary_base_dir, exec_paths.reason_dir, exec=True)
    category_stack(reason_summary.stack_smry_path, exec_paths.dumped_data_base_dir, category_result_dir)


if __name__ == '__main__':
    category_result_dir = './tt/stack_analysis'
    result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811_2'
    category_stack_of_result_base_dir(result_base_dir, category_result_dir)
