def are_same(dumped_results):
    None_result_num = len([r for r in dumped_results if r is None])
    if None_result_num == len(dumped_results):
        return True
    elif None_result_num > 0:
        return False
    base = dumped_results[0]
    for i in range(1, len(dumped_results)):
        to_compare = dumped_results[i]
        if base.global_num != to_compare.global_num:
            return False
        if base.global_bytes != to_compare.global_bytes:
            print(base, to_compare)
            print(base.global_bytes)
            print(to_compare.global_bytes)
            print(base.global_infered_vals)
            print(to_compare.global_infered_vals)
            # assert 0
            return False
        if base.default_mem_page_num != to_compare.default_mem_page_num:
            return False
        if base.default_mem_length != to_compare.default_mem_length:
            return False
        if base.default_mem_data != to_compare.default_mem_data:
            return False
    return True