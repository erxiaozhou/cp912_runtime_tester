from analyze_reslut_util import reason_base_dir2reason_summary_json
from run_dir_std_testing import test_with_mutation


def get_paras(result_base_dir, tested_dir):
    one_tc_limit=00
    mutate_num=0
    reason_dir = result_base_dir +  '/reasons'
    reason_summary_path = result_base_dir +  '/reason.json'
    paras = {
        'tested_dir': tested_dir,  # 输入
        'new_tc_dir': result_base_dir + '/test_std_new_tcs',  # 生成的所有 test case
        'result_dir': result_base_dir + '/result',  # 有difference的数据， pkl, log什么的
        'diff_tc_dir': result_base_dir + '/diff_tcs',  # 有difference 的tc
        'except_dir': result_base_dir + '/except_dir',
        'config_log_path': result_base_dir + '/config_log.json',
        'reason_dir': reason_dir,
        'one_tc_limit': one_tc_limit,
        'mutate_num': mutate_num,
        'skip_common_diff': False,
        'add_mutation': False
    }
    return paras, reason_dir, reason_summary_path


def general_main():
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing/rerun_diff'
    tested_dir = '/media/hdd_xj1/cp910_data/main_testing/diff_tcs'
    paras, reason_dir, reason_summary_path = get_paras(result_base_dir, tested_dir)
    test_with_mutation(**paras)
    reason_base_dir2reason_summary_json(reason_dir, reason_summary_path)


def test_f32():
    result_base_dir = 'results/to_test_wasm'
    tested_dir = 'to_test_wasm'
    paras, reason_dir, reason_summary_path = get_paras(result_base_dir, tested_dir)
    test_with_mutation(**paras)
    reason_base_dir2reason_summary_json(reason_dir, reason_summary_path)


def test_findings():
    result_base_dir = 'results/CP910_findings'
    tested_dir = 'CP910_findings/wasms'
    paras, reason_dir, reason_summary_path = get_paras(result_base_dir, tested_dir)
    test_with_mutation(**paras)
    reason_base_dir2reason_summary_json(reason_dir, reason_summary_path)


def test_previous_tcs():
    # result_base_dir = '/media/hdd_xj1/cp910_data/previous_tcs/result_previous_tcs_in_one'
    result_base_dir = '/media/hdd_xj1/cp910_data/previous_tcs/previous_tcs_in_one_result'
    tested_dir = '/media/hdd_xj1/cp910_data/previous_tcs/previous_tcs_in_one'
    paras, reason_dir, reason_summary_path = get_paras(result_base_dir, tested_dir)
    # assert 0, print( reason_dir, reason_summary_path)
    test_with_mutation(**paras)
    reason_base_dir2reason_summary_json(reason_dir, reason_summary_path)


if __name__ == '__main__':
    test_findings()
