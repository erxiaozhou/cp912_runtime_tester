from log_content_util.log_content_analyze import log_content_categorize_by_one_reason_path
from run_dir_testing.run_dir_testing_util import analyze, log_content_categorize, category_stack
from pathlib import Path
from file_util import check_dir
from file_util import read_json, cp_file
from analyze_reslut_util.get_reason_util import dumped_data_base_dir2reason_base_dir, dumped_data_base_dir2reason_summary_json
from run_dir_testing.testing_paras_util import get_tester_exec_paths


# reason_json_path = '/host_data/v18.1_subset_mutation/reason_summarys/only_exec_summary.json'
# dumped_data_base_dir = '/host_data/v18.1_subset_mutation/dumped_data'
# log_categorize_dir = './tt/only_highlight_log_category'
# strategy_mode = 'all'
# for strategy in ['all', 's1', 's2', 's3', 'only_interesting', 'only_highlight']:
#     log_content_categorize_by_one_reason_path(reason_json_path, dumped_data_base_dir, log_categorize_dir, strategy)

def see_log_categorize():
    base_dir = Path('/host_data/v18_330_rerun')
    reason_path = base_dir / 'reason_summarys' / 'only_exec_summary.json'
    dumped_data_base_dir = base_dir / 'dumped_data'
    modes = ['only_highlight']
    log_category_base_dir = base_dir / 'new_log'
    log_content_categorize(reason_path, log_category_base_dir, dumped_data_base_dir, modes)


def see_stack_categorize():
    base_dir = Path('/host_data/rerun_to_analyze_log/v18_stack_diff')
    reason_path = base_dir / 'reason_summarys' / 'stack_summary.json'
    dumped_data_base_dir = base_dir / 'dumped_data'
    category_stack(reason_path, dumped_data_base_dir, base_dir / 'new_stack')


def renew_summary():
    base_dir = Path('/host_data/rerun_to_analyze_log/tt')
    reason_dir = base_dir / 'reason_summarys'
    reason_dir = check_dir(reason_dir)
    dumped_data_base_dir = base_dir / 'dumped_data'
    full_reason_summary_path = reason_dir / 'full_summary.json'
    full_reason_except_tcs = reason_dir / 'full_except.json'
    only_stack_reason_summary_path = reason_dir / 'only_stack_summary.json'
    only_stack_reason_except_tcs = reason_dir / 'only_stack_except.json'
    dumped_data_base_dir2reason_summary_json(full_reason_summary_path, dumped_data_base_dir, full_reason_except_tcs)
    dumped_data_base_dir2reason_summary_json(only_stack_reason_summary_path, dumped_data_base_dir, only_stack_reason_except_tcs, ['stack_bytes_process_nan'])


def _get_tcs_to_rerun():
    src_dir = Path('/host_data/rerun_to_analyze_log/tt_18std/diff_tcs')
    dst_dir = Path('/host_data/rerun_to_analyze_log/tt_18std/tcs_to_rerun')
    dst_dir = check_dir(dst_dir)
    d = read_json('/host_data/rerun_to_analyze_log/tt_18std/reason_summarys/stack_summary.json')
    tc_names = []
    for k, names in d.items():
        if k != '()':
            tc_names.extend(names)
    for tc_name in tc_names:
        tc_name = f'{tc_name}.wasm'
        cp_file(src_dir / tc_name, dst_dir / tc_name)

def test_all_analysis():
    result_base_dir = '/host_data/rewrite/v19.1_no_mutation'
    exec_paths = get_tester_exec_paths(result_base_dir, None, check_not_exist=False)
    dumped_data_base_dir2reason_base_dir('/host_data/rewrite/v19.1_no_mutation/dumped_data', '/host_data/rewrite/v19.1_no_mutation/reasons')
    analyze(result_base_dir, exec_paths)

# see_log_categorize()
# renew_summary()
# _get_tcs_to_rerun()
test_all_analysis()