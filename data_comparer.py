from extract_dump import dump_data_extractor, get_diff_attr_names


reasons = {
    "NoneResult": "Some results are not dumped",
    "CanDumpDifference": "CanDumpDifference",
    "CannotDumpDifference": "CannotDumpDifference"
}

def are_different(dumped_results):
    # None_result_num = len([r for r in dumped_results if r is None])
    # if None_result_num == len(dumped_results):
    #     return False
    # elif None_result_num > 0:
    #     return reasons["NoneResult"]
    base = dumped_results[0]
    compare_result = {}
    assert isinstance(base, dump_data_extractor)
    for i in range(1, len(dumped_results)):
        to_compare = dumped_results[i]
        assert isinstance(to_compare, dump_data_extractor)
        if base.can_initialized and to_compare.can_initialized:
            cur_different_attrs = get_diff_attr_names(base, to_compare)
            if len(cur_different_attrs):
                compare_result[to_compare.name] = cur_different_attrs
                # assert 0
        elif base.can_initialized !=to_compare.can_initialized:
            if to_compare.can_initialized:
                compare_result[to_compare.name] = reasons["CanDumpDifference"]
            else:
                compare_result[to_compare.name] = reasons["CannotDumpDifference"]
            # assert 0, print(compare_result)
        # else:
            # print('====={}=========={}====='.format(base.can_initialized, to_compare.can_initialized))
    if len(compare_result):
        return compare_result
    else:
        return False
