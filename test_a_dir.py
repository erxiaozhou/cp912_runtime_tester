import os
from pathlib import Path
from data_comparer import are_same
from file_util import check_dir, save_json
from wasm_impl import wasmi_dump
from wasm_impl import wasmi_standard
from wasm_impl import iwasm_dump
from wasm_impl import iwasm_standard
from wasm_impl import wasm3_dump
from wasm_impl import wasmer_dump
from wasm_impl import wasmedge_dump


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
    iwasm_dump_imlp = iwasm_dump()
    # wasmer vs wasmedge: f64.lt_16
    # wasmer vs wasmi: 
    imlps = [
        # wasm3_dump_imlp,
        wasmer_dump_imlp,
        wasmedge_dump_imlp,
        # wasmi_dump_imlp,
        # iwasm_dump_imlp
    ]

    tc_paths = get_wasms_from_a_path(tested_dir)
    os.system('rm -rf result_only2')
    compare_result_base_dir = check_dir('./result_only2')
    summary_result_base_dir = check_dir('./summary_result')
    i=10
    for tc_name, tc_path in tc_paths:
        print(tc_path)
        tc_result_dir = check_dir(compare_result_base_dir/tc_name)
        # tc_summary_dir = check_dir(summary_result_base_dir/tc_name)
        dumped_results = []
        for imlp in imlps:
            store_append_name = '-'.join((tc_name, 'store-part'))
            store_path = str(imlp.name_generator(tc_result_dir, store_append_name))
            stack_append_name = '-'.join((tc_name, 'stack-part'))
            stack_path = str(imlp.name_generator(tc_result_dir, stack_append_name))
            paras = {
                'tgt_stack_path': stack_path,
                'tgt_store_path': store_path,
                'tgt_data_path': store_path
            }
            result = imlp.execute_and_collect(tc_path, **paras)
            dumped_results.append(result)
            # print(are_same(dumped_results))
        # print(dumped_results)
        if not are_same(dumped_results):
            different_tc_names.append(tc_name)
        i+=1
        # if i>30:
        #     break
    save_json('different_tc_names_iwasm_vs_wasmi.json', different_tc_names)



if __name__ == '__main__':
    test_env('./tcs')
