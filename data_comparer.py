from extract_dump import dump_data_extractor, get_diff_attr_names

reasons = {
    # "NoneResult": "Some results are not dumped",
    "CanExecute": "CanExecute",
    "CannotExecute": "CannotExecute"
}

def common_difference(compare_result, tc_name, all_compare_names):
    is_common_difference = False

    if compare_result == {
            "iwasm_classic_interp": ["default_mem_page_num"],
            "iwasm_fast_interp": ["default_mem_page_num"]
    }:
        is_common_difference = True
    # multiple memory support
    if not is_common_difference:
        expected_canrun_runtimes = ['wasm3', 'wasmer', 'wavm_default', 'wasmedge_default']
        expected_canrun_runtimes = [name for name in all_compare_names if name in expected_canrun_runtimes]
        actual_canrun_runtimes = [k for k,v in compare_result.items() if v==["CanExecute"]]
        if (expected_canrun_runtimes==actual_canrun_runtimes) and 'memory' in tc_name:
            return True
    return False
    

def sort_dump_results(results):
    
    for i, r in enumerate(results):
        if 'wasmer' in r.name:
            wasmer_idx = i
    results = [results[wasmer_idx]] + [results[i] for i in range(len(results)) if i != wasmer_idx]
    return results

def are_different(dumped_results, tc_name=None):
    # 如果全部报错，不算difference
    # 如果存在报错，报错由于 simd / reference / multi memory相关且runtime不支持该特性，不算difference
    # 能run，不能dump的情况存在，就要记录，主要是自用
    # 所有Timeout都做记录

    # all runtimes fail to run
    dumped_results = sort_dump_results(dumped_results)
    runtimes_failed = [1 for r in dumped_results if r.log_has_failed_content]
    # print(len(runtimes_failed), len(dumped_results))
    # assert 0
    if len(runtimes_failed) == len(dumped_results):
        return False
    # assert 0, print(runtimes_failed)
    # some runtimes can run, but the base cannot run
    base = dumped_results[0]
    compare_result = {}
    assert isinstance(base, dump_data_extractor)
    assert base.support_ref and base.support_v128 and True  # multiple memory
    if base.log_has_failed_content:
        for to_compare in dumped_results[1:]:
            assert isinstance(to_compare, dump_data_extractor)
            if (not to_compare.log_has_failed_content):
                compare_result[to_compare.name] = [reasons["CanExecute"]]
        return compare_result
    # some runtimes can run, and the base can run
    else:
        for to_compare in dumped_results[1:]:
            assert isinstance(to_compare, dump_data_extractor)
            if to_compare.log_has_failed_content:
                if not to_compare.expected_error:
                    compare_result[to_compare.name] = [reasons["CannotExecute"]]
                else:
                    continue
            else:
                cur_different_attrs = get_diff_attr_names(base, to_compare)
                if len(cur_different_attrs):
                    compare_result[to_compare.name] = cur_different_attrs
    # * can run ; cannot dump是自己代码的问题
    # log whether can dump
    for result in dumped_results:
        if (not result.log_has_failed_content) and (
                not result.can_initialized):
            if result.name not in compare_result:
                compare_result[result.name] = []
            compare_result[result.name].append('CanRun_CannotDump')
    # log whether timeout
    for result in dumped_results:
        if result.has_timeout:
            if result.name not in compare_result:
                compare_result[result.name] = []
            compare_result[result.name].append('Timeout')
    all_compare_names = [r.name for r in dumped_results]
    if common_difference(compare_result, tc_name, all_compare_names):
        return False
    if len(compare_result):
        return compare_result
    else:
        return False


def all_can_dump(dumped_results):
    can_init_num = 0
    for result in dumped_results:
        assert isinstance(result, dump_data_extractor)
        if result.can_initialized:
            can_init_num += 1
    return can_init_num == len(dumped_results)


def at_least_one_can_dump(dumped_results):
    can_init_num = 0
    for result in dumped_results:
        assert isinstance(result, dump_data_extractor)
        if result.can_initialized:
            can_init_num += 1
    return can_init_num > 0
