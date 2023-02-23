#!/home/zph/anaconda3/bin/python
from file_util import save_json
from log_content_util import get_paths_from_reason_json, group_paths_by_log_content


def analyze_main_testing_reasons():
    reason_json_path = '/media/hdd_xj1/cp910_data/main_testing/config_log.json'
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing/result'
    reason_paths = get_paths_from_reason_json(reason_json_path, result_base_dir)
    paths = reason_paths["(('wasm3_dump', ('CannotExecute',)), ('wasmi_interp', ('CannotExecute',)))"]
    print(len(paths))
    content_paths_dict = group_paths_by_log_content(paths)
    save_json('tt.json', content_paths_dict)
    print('Len:', len(content_paths_dict))

def analyze_previous_tcs_reasons():
    reason_json_path = '/media/hdd_xj1/cp910_data/previous_tcs/result_previous_tcs_in_one/reason.json'
    result_base_dir = '/media/hdd_xj1/cp910_data/previous_tcs/result_previous_tcs_in_one/result'
    reason_paths = get_paths_from_reason_json(reason_json_path, result_base_dir)
    paths = reason_paths["(('WasmEdge_disableAOT_newer', ('CanExecute',)),)"]
    print(len(paths))
    content_paths_dict = group_paths_by_log_content(paths)
    save_json('tt.json', content_paths_dict)
    print('Len:', len(content_paths_dict))


if __name__ == '__main__':
    analyze_previous_tcs_reasons()
