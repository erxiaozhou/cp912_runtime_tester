from file_util import pickle_dump, pickle_load


class dump_data:
    def __init__(self):
        self.log_content = None
        self.log_has_failed_content = None
        self.features = None
        self.name = None
        self.can_initialize = None
        self.has_timeout = None
        self.has_instance = None

        self.global_bytes = []
        self.global_types = []
        self.global_infered_vals = []
        self.global_muts = []
        self.global_num = -1
        self.table_num = -1
        self.default_table_len = -1
        self.mem_num = -1
        self.default_mem_length = -1
        self.default_mem_page_num = -1
        self.default_mem_data = None
        # stack
        self.stack_num = -1
        self.stack_types = []
        self.stack_infered_vals = []
        self.stack_bytes = []
        self.stack_bytes_process_nan = []

    def to_dict(self, path=None):
        # TODO
        data = {}
        data.update(self.__dict__)
        if path is not None:
            pickle_dump(path, data)
        return data
    
    def __repr__(self) -> str:
        return str(self.__dict__)


def get_extractor_from_pkl(path):
    obj = pickle_load(path)
    result_obj = dump_data()
    assert isinstance(obj, dict)
    if isinstance(obj, dict):
        result_obj.__dict__.update(obj)
    else:
        result_obj.__dict__.update(obj.__dict__)
    return result_obj


_to_compare_attrs = [
    'global_bytes',
    'global_types',
    'global_num',
    # 'global_infered_vals',
    # 'global_muts',
    'default_table_len',
    'table_num',
    'mem_num',
    'default_mem_length',
    'default_mem_page_num',
    'default_mem_data',
    'stack_num',
    'stack_types',
    'stack_bytes_process_nan',
    # 'stack_bytes',
    # 'stack_infered_vals',
    'log_has_failed_content',
    'has_timeout',
]


def get_diff_attr_names(data1, data2,
                        to_compare_attrs=None):
    assert isinstance(data1, dump_data)
    assert isinstance(data2, dump_data)
    if to_compare_attrs is None:
        to_compare_attrs = _to_compare_attrs
    different_attr_names = []
    for attr_name in to_compare_attrs:
        attr1 = getattr(data1, attr_name)
        attr2 = getattr(data2, attr_name)
        if attr1 != attr2:
            different_attr_names.append(attr_name)
    return different_attr_names
