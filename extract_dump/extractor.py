class dump_data_extractor:
    name = None
    def __init__(self) -> None:
        pass


_to_compare_attrs = [
    'global_bytes',
    'global_types',
    'global_infered_vals',
    # 'global_muts',
    # 'table_num',
    'mem_num',
    'default_mem_length',
    'default_mem_page_num',
    'default_mem_data',
    'global_num',
    'stack_num',
    'stack_types',
    'stack_infered_vals'
]


def get_diff_attr_names(data1: dump_data_extractor,
                        data2: dump_data_extractor,
                        to_compare_attrs=None):
    assert isinstance(data1, dump_data_extractor)
    assert isinstance(data2, dump_data_extractor)
    if to_compare_attrs is None:
        to_compare_attrs = _to_compare_attrs
    different_attr_names = []
    for attr_name in to_compare_attrs:
        attr1 = getattr(data1, attr_name)
        attr2 = getattr(data2, attr_name)
        if attr1 != attr2:
            different_attr_names.append(attr_name)
    return different_attr_names
