from analyze_reslut_util import reason_base_dir2reason_summary_json
from run_dir_std_testing import test_with_mutation


def get_paras(tested_dir, result_base_dir, one_tc_limit=50, mutate_num=5):
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
        'skip_common_diff': False
    }
    return paras, reason_dir, reason_summary_path


if __name__ == '__main__':
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing'
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing2'
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_10_200'
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v4.6'
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v6.2'
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v8.3'
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v9.0'
    tested_dir = './ori_tcs/tcs_v9'

    # result_base_dir = '/media/hdd_xj1/cp910_data/f32_add_executable_v3'
    # tested_dir = './ori_tcs/f32_add/executable'
    paras, reason_dir, reason_summary_path = get_paras(tested_dir, result_base_dir, one_tc_limit=50, mutate_num=2)
    print(paras)
    print('-' * 10)
    print(reason_dir)
    print('-' * 10)
    print(reason_summary_path)
    # assert 0
    test_with_mutation(**paras)
    reason_base_dir2reason_summary_json(reason_dir, reason_summary_path)
