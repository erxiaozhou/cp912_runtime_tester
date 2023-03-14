import re
from pathlib import Path
from tqdm import tqdm
from file_util import check_dir, read_json, save_json
from log_content_util.get_key_util import group_tc_names_by_log_content_key


def log_content_categorize_reason_path(reason_json_path, dumped_data_base_dir, log_categorize_dir, strategy):
    assert strategy in ['all', 's1', 's2']
    reason2tc_result_dirs = _get_reason2result_dirs_from_reason_json(reason_json_path, dumped_data_base_dir)
    assert isinstance(reason2tc_result_dirs, dict)
    log_categorize_dir = check_dir(log_categorize_dir)
    reason_content_pair2path = {}
    path2reason_content_pair = {}
    for i, reason_key in enumerate(reason2tc_result_dirs, start=1):
        # save content_key2tc_names
        content_key2tc_names_path = log_categorize_dir / '{}.json'.format(i)
        tc_result_dirs = reason2tc_result_dirs[reason_key]
        content_key2tc_names = group_tc_names_by_log_content_key(tc_result_dirs, strategy)
        assert isinstance(content_key2tc_names, dict)
        save_json(content_key2tc_names_path, content_key2tc_names)
        # save content_key and reason_key
        content_key2tc_names_path = str(content_key2tc_names_path)
        path2reason_content_pair[content_key2tc_names_path] = []
        num = len(content_key2tc_names)

        for content_key in tqdm(content_key2tc_names.keys(), total=num):
            # print(content_key)
            reason_key = re.sub(r'[\'"]', '', reason_key)
            reason_content_pair = (reason_key, '===', content_key)
            reason_content_pair = repr(reason_content_pair)
            reason_content_pair2path[reason_content_pair] = content_key2tc_names_path
            path2reason_content_pair[content_key2tc_names_path].append(reason_content_pair)

    reason_content_pair_log_path = log_categorize_dir / '0_reason_content_pair_log.json'
    save_json(reason_content_pair_log_path, reason_content_pair2path)
    reason_content_pair_log_inv_path = log_categorize_dir / '0_reason_content_pair_inv_log.json'
    save_json(reason_content_pair_log_inv_path, path2reason_content_pair)


def _get_reason2result_dirs_from_reason_json(reason_json_path, result_base_dir):
    result_base_dir = Path(result_base_dir)
    reason2tc_result_dirs = {}
    reason_tc_names = read_json(reason_json_path)
    num = len(reason_tc_names)
    for k, v in tqdm(reason_tc_names.items(),total=num):
        paths = [result_base_dir/name for name in v]
        reason2tc_result_dirs[k] = paths
    return reason2tc_result_dirs
