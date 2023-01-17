import os
from pathlib import Path
from data_comparer import are_different
from exec_util import exec_one_tc_mth, get_reason_path_to_save, load_results
from file_util import check_dir, rm_dir, save_json
from exec_util import get_wasms_from_a_path
from get_imlps_util import get_newer_imlps

def exec_a_dir(tested_dir, result_dir):
    imlps = get_newer_imlps()
    os.system('rm -rf {}'.format(result_dir))
    compare_result_base_dir = check_dir(result_dir)
    #
    reasons = {}
    tc_paths = get_wasms_from_a_path(tested_dir)
    for tc_name, tc_path in tc_paths:
        print(tc_path)
        tc_name = Path(tc_path).stem
        tc_result_dir = check_dir(compare_result_base_dir / tc_name)
        dumped_results = exec_one_tc_mth(imlps, tc_name, tc_path, tc_result_dir, tc_result_dir)
        # dumped_results = exec_one_tc(imlps, tc_name, tc_path, tc_result_dir, tc_result_dir)
        difference_reason = are_different(dumped_results, tc_name)
        if difference_reason:
            reasons[tc_name] = difference_reason
        else:
            rm_dir(tc_result_dir)
    path = get_reason_path_to_save(tested_dir, imlps)
    save_json(path, reasons)

def load_a_dir(tested_dir, result_dir):
    imlps = get_newer_imlps()
    reasons = {}
    for tc_result_dir in Path(result_dir).iterdir():
        tc_name = tc_result_dir.name
        dumped_results = load_results(tc_result_dir)
        difference_reason = are_different(dumped_results, tc_name)
        # assert 0, print(difference_reason)
        if difference_reason:
            reasons[tc_name] = difference_reason
    path = get_reason_path_to_save(tested_dir, imlps, 'load')
    save_json(path, reasons)


if __name__ == '__main__':
    # exec_a_dir('./tcs_v2', 'result')
    # load_a_dir('./tcs_v2', 'result')
    # test_env('./diff_tcs4')
    # test_env('./diff_tcs5')
    # test_env('./tcs')
    # load_a_dir('diff_tcs6', 'result6')
    # exec_a_dir('diff_tcs6', 'result_6_retry')
    # load_a_dir('test_load_data', 'test_load_data/')
    # exec_a_dir('diff_tcs7', 'result_7_retry')
    # load_a_dir('./one_tc_result', './one_tc_result')
    pass
