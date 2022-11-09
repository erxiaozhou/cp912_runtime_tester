from pathlib import Path
from data_comparer import are_different
from file_util import check_dir, save_json
from wasm_impls import wasmi_dump
from wasm_impls import wasmi_standard
from wasm_impls import iwasm_classic_interp_dump
from wasm_impls import iwasm_standard
from wasm_impls import wasm3_dump
from wasm_impls import wasmer_dump
from wasm_impls import wasmedge_dump


def test_env(tested_dir):
    different_tc_names = []
    wasmer_dump_imlp = wasmer_dump()
    wasm3_dump_imlp = wasm3_dump()
    wasmedge_dump_imlp = wasmedge_dump()
    wasmi_dump_imlp = wasmi_dump()
    iwasm_classic_interp_dump_imlp = iwasm_classic_interp_dump()
    imlps = [
        # wasm3_dump_imlp,
        wasmer_dump_imlp,
        wasmedge_dump_imlp,
        # wasmi_dump_imlp,
        # iwasm_classic_interp_dump_imlp
    ]
    tc_name = 'f64.lt_15'
    tc_path = './tcs/{}.wasm'.format(tc_name)
    tc_path = 'f64.lt_16_m.wasm'
    compare_result_base_dir = check_dir('./result')
    tc_result_dir = check_dir(compare_result_base_dir/tc_name)
    dumped_results = []
    for imlp in imlps:
        store_append_name = '-'.join((tc_name, 'store-part'))
        store_path = str(imlp.name_generator(tc_result_dir, store_append_name))
        stack_append_name = '-'.join((tc_name, 'stack-part'))
        stack_path = str(imlp.name_generator(tc_result_dir, stack_append_name))
        paras = {
            'tgt_vstack_path': stack_path,
            'tgt_store_path': store_path,
            'tgt_data_path': store_path
        }
        result = imlp.execute_and_collect(tc_path, **paras)
        dumped_results.append(result)

        # print(are_same(dumped_results))
    print(dumped_results, store_path)
    if not are_different(dumped_results):
        different_tc_names.append(tc_name)



if __name__ == '__main__':
    test_env('./tcs')
