from file_util import path_read, pickle_dump, pickle_load


def is_failed_content(content):
    assert isinstance(content, str)
    content = content.lower()
    if 'error' in content:
        return True
    elif 'failed' in content:
        return True
    elif 'exception' in content:
        return True
    elif 'aborted' in content:
        return True
    else:
        return False


_to_store_attrs = [
    'name',
    'global_bytes',
    'global_types',
    # 'global_infered_vals',
    # 'global_muts',
    # 'table_num',
    'mem_num',
    'default_mem_length',
    'default_mem_page_num',
    'default_mem_data',
    # 'global_num',
    'stack_num',
    'stack_types',
    # 'stack_infered_vals',
    'stack_bytes',
    'log_has_failed_content',
    'has_timeout',
    'stack_bytes_process_nan',
    'log_content'
]



class data_payload:
    def __init__(self, data) -> None:
        for k, v in data.items():
            setattr(self, k, v)
            self.k = v
    @classmethod
    def from_pickle_file(cls, path):
        data = pickle_load(path)
        return cls(data)


class dump_data_extractor(data_payload):
    name = None

    def __init__(self,
                 store_path=None,
                 vstack_path=None,
                 log_path=None,
                 append_info=None):
        self.store_path = store_path
        self.vstack_path = vstack_path
        self.log_path = log_path
        self.support_multi_mem = None
        self.support_v128 = None
        self.support_ref = None
        self.log_content =None

        self.has_timeout = False
        if append_info is None:
            pass
        else:
            if 'Timeout' in append_info:
                self.has_timeout = True

    def _init_log(self):
        if self.log_content is None:
            content = path_read(self.log_path)
            self.log_content = content
    
    @property
    def log_has_failed_content(self):
        return is_failed_content(self.log_content)
    @property
    def related_to_reference(self):
        related_to_reference = False
        if 'unsupport reference type' in self.log_content:
            related_to_reference = True
        return related_to_reference
        
    @property
    def related_to_SIMD(self):
        related_to_SIMD = False
        if 'SIMD support is not enabled' in self.log_content:
            related_to_SIMD = True
        elif 'unsupported opcode fd' in self.log_content:
            related_to_SIMD = True
        return related_to_SIMD
    @property
    def related_to_unknown_tyupe(self):
        related_to_unknown_tyupe = False
        content = self.log_content
        if 'unknown value type' in content or 'unknown value_type' in content:
            related_to_unknown_tyupe = True
        elif 'no operation found for opcode' in self.log_content:
            related_to_unknown_tyupe = True
        return related_to_unknown_tyupe
    @property
    def related_to_bulk_mem(self):
        related_to_bulk_mem = False
        content = self.log_content
        if 'bulk memory support is not enabled' in content:
            related_to_bulk_mem = True
        elif 'unsupported opcode fc 0a' in content:
            related_to_bulk_mem = True
        elif 'unsupported opcode fc 0b' in content:
            related_to_bulk_mem = True
        return related_to_bulk_mem

    @property
    def expected_error(self):
        expected_error = False
        if not self.support_ref:
            if self.related_to_reference or self.related_to_unknown_tyupe:
                expected_error = True
        if not self.support_v128:
            if self.related_to_SIMD or self.related_to_unknown_tyupe:
                expected_error = True
        if not self.support_multi_mem:
            if self.related_to_bulk_mem:
                expected_error = True
        return expected_error

    @property
    def default_mem_sum(self):
        return sum(self.default_mem_data)

    def to_dict(self, path=None):
        # if store_attrs is None:
        #     store_attrs = _to_store_attrs
        data = {}
        data.update(self.__dict__)
        data['can_initialized'] = self.can_initialized
        data['log_content'] = self.log_content
        if path is not None:
            pickle_dump(path, data)
        return data

    def to_pkl(self, path=None):
        pickle_dump(path, self)

def get_extractor_from_pkl(path):
    obj = pickle_load(path)
    # print(repr(obj), type(obj))
    result_obj = dump_data_extractor()
    if isinstance(obj, dict):
        result_obj.__dict__.update(obj)
    else:
        result_obj.__dict__.update(obj.__dict__)
    return result_obj


_to_compare_attrs = [
    'global_bytes',
    'global_types',
    # 'global_infered_vals',
    # 'global_muts',
    # 'table_num',
    'mem_num',
    'default_mem_length',
    'default_mem_page_num',
    'default_mem_data',
    # 'global_num',
    'stack_num',
    'stack_types',
    # 'stack_infered_vals',
    # 'stack_bytes',
    'log_has_failed_content',
    'has_timeout',
    'stack_bytes_process_nan'
]


def get_diff_attr_names(data1: data_payload,
                        data2: data_payload,
                        to_compare_attrs=None):
    assert isinstance(data1, data_payload)
    assert isinstance(data2, data_payload)
    if to_compare_attrs is None:
        to_compare_attrs = _to_compare_attrs
    different_attr_names = []
    for attr_name in to_compare_attrs:
        attr1 = getattr(data1, attr_name)
        attr2 = getattr(data2, attr_name)
        if attr1 != attr2:
            different_attr_names.append(attr_name)
    return different_attr_names
