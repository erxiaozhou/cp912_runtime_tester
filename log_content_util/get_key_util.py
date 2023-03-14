from functools import lru_cache
import re
from pathlib import Path
from .extract_keyword_from_content import extract_keyword_from_content, summary_level2
from .load_log_content_from_one_tc_result import load_log_content_from_one_tc_result


def group_tc_names_by_log_content_key(result_tc_dirs, strategy):
    content_key2tc_names = {}
    i=0
    for tc_result_dir in result_tc_dirs:
        tc_name = Path(tc_result_dir).name
        i+=1
        print(i)
        key = _get_content_key_from_tc_result_dir(tc_result_dir, strategy)
        if key not in content_key2tc_names:
            content_key2tc_names[key] = []
        content_key2tc_names[key].append(tc_name)
    return content_key2tc_names


def _get_content_key_from_tc_result_dir(tc_result_dir, strategy):
    content_dict_obj = content_dict_class.from_tc_result_dir(tc_result_dir)
    key = content_dict_obj.get_key_from_log_content(strategy)
    key = re.sub(r'[\'"]', '', key)
    return key


class content_dict_class:
    def __init__(self, content_dict) -> None:
        self.content_dict = content_dict
        self.processed_log_content = {}
    
    def get_key_from_log_content(self, strategy):
        assert strategy in ['all', 's1', 's2']
        processed_content_dict = _process_content_dict(self.content_dict, strategy)
        key = _get_key_from_log_content(processed_content_dict)
        key = re.sub(r'[\'"]', '', key)
        return key

    @classmethod
    def from_tc_result_dir(cls, tc_result_dir):
        return cls(load_log_content_from_one_tc_result(tc_result_dir))


def _get_key_from_log_content(content_dict):
    sorted_list = []
    for k, v in content_dict.items():
        impl_repr = (k, v)
        sorted_list.append(impl_repr)
    sorted_list = sorted(sorted_list, key= lambda x : x[0])
    key = repr(tuple(sorted_list))
    return key


def _process_content_dict(content_dict, strategy):
    data = {}
    for key, s in content_dict.items():
        obj = one_runtime_log(s,key)
        if strategy == 'all':
            data[key] = obj.shorter
        elif strategy == 's1':
            data[key] = obj.summary_key_s1
        elif strategy == 's2':
            data[key] = obj.summary_key_s2
    return data



class one_runtime_log():
    def __init__(self, s, key) -> None:
        s = filter_normal_output(s, key)
        s = s.strip('\'"\n\\ ')
        self.filter_normal = s
        self.shorter = extract_keyword_from_content(self.filter_normal, strategy='all')
        self.summary_key_s1 = extract_keyword_from_content(self.filter_normal, strategy='s1')
        self.summary_key_s2 = summary_level2(self.shorter)

        # s = extract_keyword_from_content(s, strategy)

@lru_cache(maxsize=1024, typed=False)
def filter_normal_output(s, key):
    hex_p = r'0[xX][0-9a-fA-F]+'
    num_p = r'^[\-\+]?(?:(?:\d+)|(?:[\.\+\d]+e[\-\+]?\d+)|(?:\d+\.\d+)|(?:nan)|(?:inf))\n?$'
    wasm_path_p = r' [^ ]+\.wasm'
    offset_p = r'\(at offset (?:(?:\d+)|(?:0[xX][0-9a-fA-F]+))\)'
    time_p = r'\[[\-0-9]+ [\.:0-9]+\]'
    if key == 'wasm3_dump':
        p = r' *Result: *\-?[0-9\.]+$'
        s = re.sub(p, '', s)
        p = r' *Result: *\-?0[xX][0-9a-fA-F]+$'
        s = re.sub(p, '', s)
        p = r' *Result: *\-?(?:(?:nan)|(?:inf))'
        s = re.sub(p, '', s)
        if 'Empty Stack' in s:
            s = ''
    elif key == 'WasmEdge_disableAOT_newer':
        s = re.sub(time_p, '', s)
        s = re.sub(wasm_path_p, '', s)
        p = r'Bytecode offset: 0[xX][0-9a-fA-F]+'
        s = re.sub(p, '', s)
        p = r' Code: 0[xX][0-9a-fA-F]+'
        s = re.sub(p, '', s)
        s = re.sub(num_p, '', s)
    elif key == 'wasmer_default_dump':
        s = re.sub(offset_p, '', s)
        s = re.sub(wasm_path_p, '', s)
    elif key == 'wasmi_interp':
        s = re.sub(offset_p, '', s)
        s = re.sub(wasm_path_p, '', s)
    elif key in ['iwasm_fast_interp_dump', 'iwasm_classic_interp_dump']:
        s = re.sub(r'^\n*$', '', s)
        p = r'^0x[a-f\d]+:i(?:(?:64)|(?:32))$'
        s = re.sub(p, '', s)
        p = r'^.*:f(?:(?:64)|(?:32))$'
        s = re.sub(p, '', s)
    elif key == 'WAVM_default':
        pass
    else:
        assert 0, print(key)
    s = re.sub('\n', '', s)
    return s
