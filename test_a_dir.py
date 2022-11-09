import os
from pathlib import Path
from data_comparer import are_different
from file_util import check_dir, remove_file_without_exception, save_json
from wasm_impls import wasmi_dump
from wasm_impls import wasmi_standard
from wasm_impls import iwasm_classic_interp_dump
from wasm_impls import iwasm_standard
from wasm_impls import wasm3_dump
from wasm_impls import wasmer_dump
from wasm_impls import wasmedge_dump


def get_wasms_from_a_path(dir_):
    tc_paths = []
    dir_ = Path(dir_)
    for p in dir_.iterdir():
        if p.suffix == '.wasm':
            path = str(p)
            tc_name = p.stem
            tc_paths.append((tc_name, path))
    return tc_paths


def test_env(tested_dir):
    different_tc_names = []
    wasmer_dump_imlp = wasmer_dump()
    wasm3_dump_imlp = wasm3_dump()
    wasmedge_dump_imlp = wasmedge_dump()
    wasmi_dump_imlp = wasmi_dump()
    iwasm_classic_interp_dump_imlp = iwasm_classic_interp_dump()
    # wasmer vs wasmedge: f64.lt_16
    # wasmer vs wasmi: 
    imlps = [
        wasmer_dump_imlp,
        wasm3_dump_imlp,
        wasmedge_dump_imlp,
        wasmi_dump_imlp,
        iwasm_classic_interp_dump_imlp
    ]
    result_dir = 'result'
    os.system('rm -rf {}'.format(result_dir))
    compare_result_base_dir = check_dir(result_dir)
    # summary_result_base_dir = check_dir('./summary_result')
    i=10
    reasons = {}
    tc_paths = get_wasms_from_a_path(tested_dir)
    to_remove_paths = []
    for tc_name, tc_path in tc_paths:
        print(tc_path)
        tc_result_dir = check_dir(compare_result_base_dir/tc_name)
        # tc_summary_dir = check_dir(summary_result_base_dir/tc_name)
        dumped_results = []
        for imlp in imlps:
            store_append_name = '-'.join((tc_name, 'store-part'))
            store_path = str(imlp.name_generator(tc_result_dir, store_append_name))
            vstack_append_name = '-'.join((tc_name, 'vstack-part'))
            vstack_path = str(imlp.name_generator(tc_result_dir, vstack_append_name))
            paras = {
                'tgt_vstack_path': vstack_path,
                'tgt_store_path': store_path
            }
            to_remove_paths.append(vstack_path)
            to_remove_paths.append(store_path)
            result = imlp.execute_and_collect(tc_path, **paras)
            dumped_results.append(result)
            # rm_paths(vstack_path, store_path)
            # print(are_same(dumped_results))
        # print(dumped_results)
        difference_reason = are_different(dumped_results)
        print(difference_reason)
        if difference_reason:
            # assert 0
            different_tc_names.append(tc_name)
            reasons[tc_name] = difference_reason
        i+=1
        # if i>500:
        #     break
        # rm_paths(*to_remove_paths)
    save_json('different_tc_names.json', different_tc_names)
    save_json('different_reason.json', reasons)


def rm_paths(*paths):
    for p in paths:
        remove_file_without_exception(p)


if __name__ == '__main__':
    test_env('./tcs')
    # test_env('./tcs')
