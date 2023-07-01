from load_results_util import load_results_from_one_dumped_data_dir


def load_log_from_one_tc_result(one_tc_result_dir):
    results = load_results_from_one_dumped_data_dir(one_tc_result_dir)
    name_log = {}
    for r in results:
        name_log[r.name] = r.log_content
    return name_log
