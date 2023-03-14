
from exec_util import load_results_from_one_tc_result


def load_log_content_from_one_tc_result(one_tc_result_dir):
    results = load_results_from_one_tc_result(one_tc_result_dir)
    name_log = {}
    for r in results:
        name_log[r.name] = r.log_content
    return name_log
