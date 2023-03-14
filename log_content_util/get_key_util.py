from functools import lru_cache
import re
from pathlib import Path
from .extract_keyword_from_content import extract_keyword_from_content, summary_level2
from .load_log_content_from_one_tc_result import load_log_content_from_one_tc_result
from concurrent import futures


def group_tc_names_by_log_content_key(tc_result_dirs, strategy):
    content_key2tc_names = {}
    for tc_name, key in _tc_name_key_pair_generator_mtx(tc_result_dirs, strategy):
        if key not in content_key2tc_names:
            content_key2tc_names[key] = []
        content_key2tc_names[key].append(tc_name)
    return content_key2tc_names


def _tc_name_key_pair_generator(tc_result_dirs, strategy):
    for tc_result_dir in tc_result_dirs:
        yield _get_tc_name_key_pair(tc_result_dir, strategy)


def _tc_name_key_pair_generator_mtx(tc_result_dirs, strategy):
    tc_name_key_pairs = []
    with futures.ProcessPoolExecutor(max_workers=30) as executor:
        for tc_result_dir in tc_result_dirs:
            future = executor.submit(_get_tc_name_key_pair, tc_result_dir, strategy)
            tc_name_key_pairs.append(future)
        for future in futures.as_completed(tc_name_key_pairs):
            yield future.result()


def _get_tc_name_key_pair(tc_result_dir, strategy):
    tc_name = Path(tc_result_dir).name
    key = _get_content_key_from_tc_result_dir(tc_result_dir, strategy)
    return (tc_name, key)


def _get_content_key_from_tc_result_dir(tc_result_dir, strategy):
    content_dict_obj = content_dict_class.from_tc_result_dir(tc_result_dir)
    key = content_dict_obj.get_key_from_log_content(strategy)
    key = re.sub(r'[\'"]', '', key)
    return key


class content_dict_class:
    def __init__(self, content_dict) -> None:
        self.content_dict = content_dict

    def get_key_from_log_content(self, strategy):
        assert strategy in ['all', 's1', 's2']
        processed_log_dict = _process_content_dict(self.content_dict, strategy)
        processed_log_dict_repr = repr(processed_log_dict)
        key = _get_key_from_processed_log_dict_repr(processed_log_dict_repr)
        key = re.sub(r'[\'"]', '', key)
        return key

    @classmethod
    def from_tc_result_dir(cls, tc_result_dir):
        return cls(load_log_content_from_one_tc_result(tc_result_dir))


@lru_cache(maxsize=4096, typed=False)
def _get_key_from_processed_log_dict_repr(processed_log_dict_repr):
    processed_log_dict = eval(processed_log_dict_repr)
    sorted_list = []
    for k, v in processed_log_dict.items():
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

    @property
    def shorter(self):
        return extract_keyword_from_content(self.filter_normal, strategy='all')

    @property
    def summary_key_s1(self):
        return extract_keyword_from_content(self.filter_normal, strategy='s1')

    @property
    def summary_key_s2(self):
        return summary_level2(self.shorter)


@lru_cache(maxsize=4096, typed=False)
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
