from extract_dump import dump_data, get_diff_attr_names


def are_different(dumped_results):
    # 如果全部报错，不算difference
    # 如果存在报错，报错由于 simd / reference / multi memory相关且runtime不支持该特性，不算difference (这个就要在更后端处理了)
    # 能run，不能dump的情况存在，就要记录，主要是自用
    # 所有Timeout都做记录

    # all runtimes fail to run
    dumped_results = _sort_dump_results(dumped_results)
    runtimes_failed = [1 for r in dumped_results if r.log_has_failed_content]
    if len(runtimes_failed) == len(dumped_results):
        return False
    # some runtimes can run, but the base cannot run
    base = dumped_results[0]
    compare_result = {}
    assert isinstance(base, dump_data)
    assert base.features['support_ref'] and base.features['support_v128'] and True  # multiple memory
    if base.log_has_failed_content:
        re_compare_runtimes = []
        for to_compare in dumped_results[1:]:
            assert isinstance(to_compare, dump_data)
            if not to_compare.log_has_failed_content:
                if not to_compare.has_timeout:
                    compare_result[to_compare.name] = ["CanExecute"]
                    re_compare_runtimes.append(to_compare)
                else:
                    compare_result[to_compare.name] = ["has_timeout"]
        # 这个时候应该换个base继续跑
        # re compare
        if len(re_compare_runtimes) > 1:
            base = re_compare_runtimes[0]
            for to_compare in re_compare_runtimes[1:]:
                cur_different_attrs = get_diff_attr_names(base, to_compare)
                # ! 这里是不是有问题
                if len(cur_different_attrs):
                    compare_result[to_compare.name].extend(cur_different_attrs)
                    compare_result[base.name].extend(cur_different_attrs)
            if base.name in compare_result:
                compare_result[base.name] = list(set(compare_result[base.name]))
        return compare_result
    # some runtimes can run, and the base can run
    else:
        for to_compare in dumped_results[1:]:
            assert isinstance(to_compare, dump_data)
            if to_compare.log_has_failed_content:
                compare_result[to_compare.name] = ["CannotExecute"]
            else:
                cur_different_attrs = get_diff_attr_names(base, to_compare)
                # ! 这里是不是有问题
                if len(cur_different_attrs):
                    compare_result[to_compare.name] = cur_different_attrs
                    if base.name not in compare_result:
                        compare_result[base.name] = []
                    compare_result[base.name].extend(cur_different_attrs)
                if base.name in compare_result:
                    compare_result[base.name] = list(set(compare_result[base.name]))
    # * can run ; cannot dump是自己代码的问题
    # log whether can dump
    for result in dumped_results:
        # 下面检查下逻辑
        # print(result.log_has_failed_content, result.name)
        if (not result.log_has_failed_content) and (
                not result.can_initialize):
            if result.name not in compare_result:
                compare_result[result.name] = []
            compare_result[result.name].append('CanRun_CannotDump')
    # log whether timeout
    # ! 这个再观察下，看着很奇怪，好像有has_timeout就够了，这个准备删掉
    for result in dumped_results:
        if result.has_timeout:
            if result.name not in compare_result:
                compare_result[result.name] = []
            compare_result[result.name].append('has_timeout')
    if len(compare_result):
        return compare_result
    else:
        return False

def _sort_dump_results(results):
    for i, r in enumerate(results):
        if 'wasmer' in r.name:
            wasmer_idx = i
    results = [results[wasmer_idx]] + [results[i] for i in range(len(results)) if i != wasmer_idx]

    return results


def at_least_one_can_execute(dumped_results):
    return _get_can_execute_num(dumped_results) > 0


def at_least_one_can_instantiate(dumped_results):
    return _get_can_instantiate(dumped_results) > 0


def _get_can_execute_num(dumped_results):
    can_exec_num = 0
    for result in dumped_results:
        assert isinstance(result, dump_data)
        if not result.failed_exec:
            can_exec_num += 1
    return can_exec_num


def _get_can_instantiate(dumped_results):
    can_inst_num = 0
    for result in dumped_results:
        assert isinstance(result, dump_data)
        if result.has_instance:
            can_inst_num += 1
    return can_inst_num
