from pathlib import Path
from data_comparer import are_different
from extract_dump.extractor import dump_data_extractor
from file_util import check_dir, save_json, read_json
from test_a_dir import exec_one_tc, get_imlps
import os
import re


def get_names():
    data = read_json('rewrite_tc_reason.json')
    names = data["{'wasmedge_default': ['CanExecute']}"]
    return names

def get_log_content(tc_name):
    tc_path = 'diff_tcs/{}.wasm'.format(tc_name)
    result_dir = 'one_tc_result'
    os.system('rm -rf {}'.format(result_dir))
    compare_result_base_dir = check_dir(result_dir)
    tc_result_dir = check_dir(compare_result_base_dir / tc_name)
    imlps = get_imlps()
    dumped_results = exec_one_tc(imlps, tc_name, tc_path, tc_result_dir)
    difference_reason = are_different(dumped_results, tc_name)
    all_content = ''
    for result in dumped_results:
        assert isinstance(result, dump_data_extractor)
        log_content = result.log_content
        log_content = re.sub(r'0[xX][^ ]*', '', log_content)
        log_content = re.sub(r'[^ ]*.wasm', '', log_content)
        log_content = re.sub(r'\d', '', log_content)
        all_content += log_content
        all_content += '==='
    return all_content

# data = read_json('diff_tcs4_wasmi_interp---iwasm_classic_interp_dump---iwasm_fast_interp_dump---wasm3_dump---wasmer_default_dump---WasmEdge_disableAOT---WAVM_default_processed_reasons.json')
# rewrite_data = {}
# for tc, reason in data.items():
#     reason = repr(reason)
#     if reason not in rewrite_data:
#         rewrite_data[reason] = []
#     rewrite_data[reason].append(tc)
# save_json('rewrite_tc_reason.json', rewrite_data)


if __name__ == '__main__':
    new_log = {}
    for name in get_names():
        log_content = get_log_content(name)
        if log_content not in new_log:
            new_log[log_content] = []
        new_log[log_content].append(name)
    save_json('log_content2tcnames.json', new_log)
