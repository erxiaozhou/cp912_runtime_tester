from analyze_reslut_util import get_reason_summary
from test_a_dir_std import test_with_mutation


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
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing_v8.1'
    tested_dir = './tcs_v8'
    paras, reason_dir, reason_summary_path = get_paras(tested_dir, result_base_dir, one_tc_limit=50, mutate_num=5)
    print(paras)
    print('-' * 10)
    print(reason_dir)
    print('-' * 10)
    print(reason_summary_path)
    # assert 0
    test_with_mutation(**paras)
    get_reason_summary(reason_dir, reason_summary_path)
