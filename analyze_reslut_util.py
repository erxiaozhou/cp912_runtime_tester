from data_comparer import are_different
from exec_util import load_results_from_one_tc_result
from file_util import read_json, save_json
from pathlib import Path


def _get_key_from_reason_content(content):
    assert isinstance(content, dict)
    sorted_list = []
    for k, v in content.items():
        impl_repr = (k, tuple(sorted(v)))
        sorted_list.append(impl_repr)
    sorted_list = sorted(sorted_list, key= lambda x : x[0])
    sorted_tuple_str = repr(tuple(sorted_list))
    return sorted_tuple_str


def _get_key_from_diff_result_p(p):
    content = read_json(p)
    sorted_tuple_str = _get_key_from_reason_content(content)
    return sorted_tuple_str


def reason_base_dir2reason_summary(reason_base_dir):
    reason_summary = {}
    dir_path = Path(reason_base_dir)
    for p in dir_path.iterdir():
        stem = p.stem
        reason_key = _get_key_from_diff_result_p(p)
        if reason_key not in reason_summary:
            reason_summary[reason_key] = []
        reason_summary[reason_key].append(stem)
    return reason_summary

def reason_base_dir2reason_summary_json(reason_base_dir, save_path=None):
    assert save_path is not None
    reason_summary = reason_base_dir2reason_summary(reason_base_dir)
    save_json(save_path, reason_summary)


def result_base_dir2reason_summary(result_json_path, result_dir, except_log):
    reason_summary = {}
    except_tc_names = []
    for tc_result_dir in Path(result_dir).iterdir():
        tc_name = tc_result_dir.name
        try:
            dumped_results = load_results_from_one_tc_result(tc_result_dir)
            difference_reason = are_different(dumped_results, tc_name)
            if difference_reason:
                reason_key = _get_key_from_reason_content(difference_reason)
                if reason_key not in reason_summary:
                    reason_summary[reason_key] = []
                reason_summary[reason_key].append(tc_name)
        except Exception:
            except_tc_names.append(tc_name)
    save_json(result_json_path, reason_summary)
    save_json(except_log, except_tc_names)
