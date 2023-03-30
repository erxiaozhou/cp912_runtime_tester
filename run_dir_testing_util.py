from pathlib import Path
from path_group_util import tester_exec_paths
from run_dir_std_testing import test_with_mutation
from file_util import check_dir, read_json, rm_dir
from log_content_util import log_content_categorize_by_one_reason_path


def set_paras_with_mutation(tested_dir, result_base_dir, one_tc_limit=50, mutate_num=5):
    result_base_dir = Path(result_base_dir)
    paths = tester_exec_paths.from_result_base_dir(result_base_dir)
    paras = {
        'tested_dir': tested_dir,  # 输入
        'one_tc_limit': one_tc_limit,
        'mutate_num': mutate_num,
        'skip_common_diff': False
    }
    paras.update(paths.to_dict)
    return paras, paths


def get_no_mutation_paras(result_base_dir, tested_dir):
    paras, paths = set_paras_with_mutation(tested_dir, result_base_dir, one_tc_limit=0, mutate_num=0)
    # 
    result_base_dir = Path(result_base_dir)
    paras_append = {
        'skip_common_diff': False,
        'add_mutation': False
    }
    paras.update(paras_append)
    return paras, paths


def detect_canrun_cannotdump(exec_paths, result_base_dir):
    assert isinstance(exec_paths, tester_exec_paths)
    canrun_cannotdump_tc_names = []
    # init canrun_cannotdump_tc_names
    for reason_file in exec_paths.reason_dir.iterdir():
        assert reason_file.suffix == '.json'
        data = read_json(reason_file)
        if 'CanRun_CannotDump' in repr(data):
            tc_name = reason_file.stem
            canrun_cannotdump_tc_names.append(tc_name)
    # copy the tcs in canrun_cannotdump_tc_names to a tmp dir
    diff_tcs_base_dir = exec_paths.diff_tc_dir
    diff_tcs_base_dir = Path(diff_tcs_base_dir)
    new_dir = check_dir(diff_tcs_base_dir.parent / 'tmp_tcs')
    for tc_name in canrun_cannotdump_tc_names:
        assert not tc_name.endswith('.wasm')
        tc_path = diff_tcs_base_dir / f'{tc_name}.wasm'
        new_dir_tc_path = new_dir / f'{tc_name}.wasm'
        tc_path.rename(new_dir_tc_path)
    # remove existing results in each result dir
    for tc_name in canrun_cannotdump_tc_names:
        tc_dumped_data_dir = Path(exec_paths.dumped_data_base_dir) / tc_name
        if tc_dumped_data_dir.exists():
            rm_dir(tc_dumped_data_dir)
        tc_reason_path = Path(exec_paths.reason_dir) / f'{tc_name}.json'
        if tc_reason_path.exists():
            tc_reason_path.unlink()
    paras, new_paths = get_no_mutation_paras(result_base_dir, new_dir)
    paras['check_result_dir_not_exist'] = False
    test_with_mutation(**paras)


def log_content_categorize(reason_summary_path, log_category_base_dir, dumped_data_base_dir, modes=None):
    if modes is None:
        modes = ['all', 's1', 's2', 's3', 'only_interesting', 'only_highlight']
    log_category_base_dir = check_dir(log_category_base_dir)
    for mode in modes:
        sub_log_category_dir = log_category_base_dir / '{}_log_category'.format(mode)
        log_content_categorize_by_one_reason_path(reason_summary_path, dumped_data_base_dir, sub_log_category_dir, mode)
        print('a log_category_dir:', sub_log_category_dir)

