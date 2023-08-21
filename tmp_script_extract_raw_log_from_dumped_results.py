from pathlib import Path
from file_util import save_json, read_json
from log_content_util.load_log_from_one_tc_result_util import load_log_from_one_tc_result
from log_content_util.get_key_util import rawRuntimeLogs
from tqdm import tqdm


def extract_log_content():
    base_dir = Path('/host_data/main_testing_v18_330_9811_2/dumped_data')
    data = []
    for one_tc_result_dir in tqdm(base_dir.iterdir(), total=130673):
        assert one_tc_result_dir.is_dir()
        log = load_log_from_one_tc_result(one_tc_result_dir)
        data.append(log)
    save_json('/host_data/tuning/main_testing_v18_330_9811_2_raw_log_content.json', data)


def see_log_num():
    data = read_json('/host_data/tuning/main_testing_v18_330_9811_2_raw_log_content.json')
    logs_ = set()
    for log_dict in tqdm(data):
        logs_.add(rawRuntimeLogs(log_dict))
    print(len(logs_))

see_log_num()
