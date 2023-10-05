from .dump_data_util import dumpData, get_diff_attr_names


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
    assert isinstance(base, dumpData)
    # ! 下面这行检查features只是权宜之计，暂时没有更好的办法
    assert base.features['support_ref'] and base.features['support_v128'] and True  # multiple memory
    if base.failed_exec:
        if base.log_has_failed_content:
            # compare_result[base.name] = ["CannotExecute"]
            pass
        elif base.has_timeout:
            compare_result[base.name] = ["has_timeout"]
        elif base.has_crash:
            compare_result[base.name] = ["has_crash"]
        re_compare_runtimes = []
        for to_compare in dumped_results[1:]:
            assert isinstance(to_compare, dumpData)
            if not to_compare.log_has_failed_content:
                if to_compare.has_timeout:
                    compare_result[to_compare.name] = ["has_timeout"]
                elif to_compare.has_crash:
                    compare_result[to_compare.name] = ["has_crash"]
                else:
                    compare_result[to_compare.name] = ["CanExecute"]
                    re_compare_runtimes.append(to_compare)
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
            assert isinstance(to_compare, dumpData)
            if to_compare.log_has_failed_content:
                compare_result[to_compare.name] = ["CannotExecute"]
            elif to_compare.has_timeout:
                compare_result[to_compare.name] = ["has_timeout"]
            elif to_compare.has_crash:
                compare_result[to_compare.name] = ["has_crash"]
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
        if (not result.failed_exec) and (
                not result.can_initialize):
            if result.name not in compare_result:
                compare_result[result.name] = []
            compare_result[result.name].append('CanRun_CannotDump')
    # log whether timeout
    for result in dumped_results:
        # ! 这个再观察下，看着很奇怪，好像有has_timeout就够了，这个准备删掉
        if result.has_timeout:
            compare_result.setdefault(result.name, [])
            if 'has_timeout' not in compare_result[result.name]:
                compare_result[result.name].append('has_timeout')
        if result.has_crash:
            compare_result.setdefault(result.name, [])
            if 'has_crash' not in compare_result[result.name]:
                compare_result[result.name].append('has_crash')
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
