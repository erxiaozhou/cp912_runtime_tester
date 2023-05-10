from stack_val_analyze import category_stack
from path_group_util import tester_exec_paths
from analyze_reslut_util import get_reason_summarys
from path_group_util import analyze_result_dirs


def category_stack_of_result_base_dir(result_base_dir, category_result_dir):
    exec_paths = tester_exec_paths.from_result_base_dir(result_base_dir)
    analyze_result_ps = analyze_result_dirs(result_base_dir)
    paths = get_reason_summarys(analyze_result_ps.reason_summary_base_dir, exec_paths.reason_dir, exec=True)
    stack_reason_summary = paths['stack']
    category_stack(stack_reason_summary, exec_paths.dumped_data_base_dir, category_result_dir)


if __name__ == '__main__':
    category_result_dir = './tt/stack_analysis'
    result_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811_2'
    category_stack_of_result_base_dir(result_base_dir, category_result_dir)
