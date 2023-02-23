#!/home/zph/anaconda3/bin/python
from analyze_reslut_util import result_base_dir2reason_summary


def analyze_main_testing():
    result_json_path = '/media/hdd_xj1/cp910_data/main_testing/summary_from_result.json'
    result_dir = '/media/hdd_xj1/cp910_data/main_testing/result'
    except_log = '/media/hdd_xj1/cp910_data/main_testing/get_reason_exception.json'
    result_base_dir2reason_summary(result_json_path, result_dir, except_log)


def analyze_previous_tca():
    result_json_path = '/media/hdd_xj1/cp910_data/main_testing/summary_from_result.json'
    result_dir = '/media/hdd_xj1/cp910_data/main_testing/result'
    except_log = '/media/hdd_xj1/cp910_data/main_testing/get_reason_exception.json'
    result_base_dir2reason_summary(result_json_path, result_dir, except_log)

if __name__ == '__main__':
    analyze_main_testing()
