from collections import Counter
from functools import lru_cache
import re
from pathlib import Path
from .extract_keyword_from_content_util import extract_keyword_from_content, keyword_part2possible_common_reason, get_categorize_info_coarse_summary, get_categorize_info_fine_summary
from .extract_keyword_from_content_util import func_sec_size_mismatch, runtime_self_unsupport
from .load_log_from_one_tc_result_util import load_log_from_one_tc_result
from concurrent import futures
from .extract_keyword_from_content_util import fd_opcode, SIMD_unsupport, illegal_type, reference_unsupport



supported_modes = ['all', 's1', 's2', 's3', 'only_interesting', 'only_highlight']


def group_tc_names_by_log_key(tc_result_dirs, strategy):
    log_key2tc_names = _group_tc_names_by_log_key_core(tc_result_dirs, strategy)
    # 
    if strategy == 'only_highlight':
        rewritten_content_key2tc_names = rewrite_dict(log_key2tc_names)
    else:
        rewritten_content_key2tc_names = log_key2tc_names
    rewritten_content_key2tc_names = {_dict2key(k):v for k,v in rewritten_content_key2tc_names.items()}
    return rewritten_content_key2tc_names


def rewrite_dict(log_key2tc_names):
    log_keywords = set()
    log_key_dict_reprs = list(log_key2tc_names.keys())
    repr2log_keyword_freq = {}

    for log_key_dict_repr in log_key_dict_reprs:
        # print('log_key_dict_repr', log_key_dict_repr)
        log_key_dict =eval(log_key_dict_repr)
        values = list(log_key_dict.values())
        log_keywords.update(values)
        repr2log_keyword_freq[log_key_dict_repr] = {k:v/len(values) for k, v in Counter(values).items()}
    # print('log_keywords', log_keywords)
    # log_keywords = list(log_keywords)

    to_save_reprs = set()
    if '{}' in repr2log_keyword_freq:
        to_save_reprs.add('{}')
    for keyword in log_keywords:
        max_v = -1
        for log_key_dict_repr, c in repr2log_keyword_freq.items():
            if c.get(keyword, -5) >= max_v:
                max_v = c[keyword]
        if max_v < 0.5:
            continue
        # print('max_v', max_v, keyword)
        for log_key_dict_repr, c in repr2log_keyword_freq.items():
            if c.get(keyword, -5) == max_v:
                # print(keyword, max_v, c, log_key_dict_repr)
                to_save_reprs.add(log_key_dict_repr)
                # to_save_reprs.add(log_key_dict_repr)
    log_key2tc_names = {k:log_key2tc_names[k] for k in to_save_reprs}
    # assert 0, print(len(log_key2tc_names))

    return log_key2tc_names


def _group_tc_names_by_log_key_core(tc_result_dirs, strategy):
    log_key2tc_names = {}
    for tc_name, key in _tc_name_key_pair_generator(tc_result_dirs, strategy):
        # print(tc_name)
        if key not in log_key2tc_names:
            log_key2tc_names[key] = []
        log_key2tc_names[key].append(tc_name)
    return log_key2tc_names


def _tc_name_key_pair_generator(tc_result_dirs, strategy):
    for tc_result_dir in tc_result_dirs:
        tc_name = Path(tc_result_dir).name
        key = _get_log_dict_repr_key_from_tc_result_dir(tc_result_dir, strategy)
        yield (tc_name, key)


def _get_log_dict_repr_key_from_tc_result_dir(tc_result_dir, strategy):
    log_dict_obj = logDict.from_tc_result_dir(tc_result_dir)
    dict_ = log_dict_obj.get_processed_log_dict(strategy)
    # key =_dict2key(dict_)
    return repr(dict_)


class logDict:
    def __init__(self, log_dict) -> None:
        self.log_dict = log_dict
    
    # def get_processed_log_dict()

    def get_processed_log_dict(self, strategy):
        assert strategy in supported_modes
        processed_log_dict = _process_log_dict(self.log_dict, strategy)
        return processed_log_dict

    @classmethod
    def from_tc_result_dir(cls, tc_result_dir):
        return cls(load_log_from_one_tc_result(tc_result_dir))


def _dict2key(dict_data_repr):
    processed_log_dict_repr = dict_data_repr
    key = _get_key_from_processed_log_dict_repr(processed_log_dict_repr)
    key = re.sub(r'[\'"]', '', key)
    return key


@lru_cache(maxsize=4096 * 4, typed=False)
def _get_key_from_processed_log_dict_repr(processed_log_dict_repr):
    processed_log_dict = eval(processed_log_dict_repr)
    sorted_list = []
    for k, v in processed_log_dict.items():
        impl_repr = (k, v)
        sorted_list.append(impl_repr)
    sorted_list = sorted(sorted_list, key= lambda x : x[0])
    key = repr(tuple(sorted_list))
    return key


def _process_log_dict(log_dict, strategy):
    log_objs = {}
    for runtime_name, s in log_dict.items():
        obj = oneRuntimeLog(s,runtime_name)
        log_objs[runtime_name] = obj
    # 
    data = {}
    for runtime_name, obj in log_objs.items():
        if strategy == 'all':
            processed_log = obj.keyword_part
        elif strategy == 's1':
            processed_log = obj.summary_key_s1
        elif strategy == 's2':
            processed_log = obj.summary_key_s2
        elif strategy == 's3':
            processed_log = obj.summary_key_s3
        elif strategy in ['only_interesting', 'only_highlight']:
            processed_log = obj.summary_key_s3
        if processed_log:
            data[runtime_name] = processed_log
    if strategy in ['only_interesting', 'only_highlight']:
        for runtime_name, obj in log_objs.items():
            processed_log = obj.summary_key_s3
            if processed_log:
                data[runtime_name] = processed_log
        # 
        vals = list(data.values())
        # func_sec_size_mismatch 是所有runtime都不支持的
        if 0 < vals.count(func_sec_size_mismatch) < len(vals):
            for runtime_name in data.keys():
                data[runtime_name] = '<masked because of {}>'.format(func_sec_size_mismatch)
        # 先把一些模糊的log通过其他runtime的报错推出来
        runtime_names = list(data.keys())
        has_fd = False
        # rule1: fd_opcode
        for v in data.values():
            if v == fd_opcode:
                has_fd = True
        # rule2: SIMD_unsupport
        if not has_fd:
            for obj in log_objs.values():
                if obj.summary_key_s2 == SIMD_unsupport:
                    has_fd = True
        # rule3: special runtimes
        if not has_fd:
            for runtime_name in ['iwasm_classic_interp_dump', 'iwasm_fast_interp_dump']:
                if data.get(runtime_name) == fd_opcode:
                    # assert 0
                    has_fd = True
        if has_fd:
            for runtime_name in runtime_names:
                if data[runtime_name] == illegal_type:
                    # assert 0
                    data[runtime_name] = runtime_self_unsupport
            for runtime_name in ['wasm3_dump', 'wasmi_interp', 'iwasm_classic_interp_dump', 'iwasm_fast_interp_dump']:
                if data.get(runtime_name) == fd_opcode:
                    # assert 0
                    data[runtime_name] = runtime_self_unsupport
        # reference
        has_ref = False
        for obj in log_objs.values():
            if obj.summary_key_s2 == reference_unsupport:
                has_ref = True
                break
        if has_ref:
            for runtime_name in runtime_names:
                if data[runtime_name] == illegal_type:
                    data[runtime_name] = runtime_self_unsupport

        # 某些runtime理应不支持的
        for runtime_name in runtime_names:
            if data[runtime_name] == runtime_self_unsupport:
                data.pop(runtime_name)
    return data


class oneRuntimeLog():
    def __init__(self, s, runtime_name) -> None:
        s = filter_normal_output(s, runtime_name)
        s = s.strip('\'"\n\\ ')
        self.filter_normal = s

    @property
    def keyword_part(self):
        return extract_keyword_from_content(self.filter_normal)

    @property
    def summary_key_s1(self):
        # set some as 
        return keyword_part2possible_common_reason(self.keyword_part)

    @property
    def summary_key_s2(self):
        return get_categorize_info_coarse_summary(self.keyword_part)

    @property
    def summary_key_s3(self):
        return get_categorize_info_fine_summary(self.keyword_part)


@lru_cache(maxsize=4096 * 4, typed=False)
def filter_normal_output(s, runtime_name):
    hex_p = r'0[xX][0-9a-fA-F]+'
    num_p = r'^[\-\+]?(?:(?:\d+)|(?:[\.\+\d]+e[\-\+]?\d+)|(?:\d+\.\d+)|(?:nan)|(?:inf))\n?$'
    wasm_path_p = r' [^ ]+\.wasm'
    offset_p = r'\(at offset (?:(?:\d+)|(?:0[xX][0-9a-fA-F]+))\)'
    time_p = r'\[[\-0-9]+ [\.:0-9]+\]'
    if runtime_name == 'wasm3_dump':
        p = r' *Result: *\-?[0-9\.]+$'
        s = re.sub(p, '', s)
        p = r' *Result: *\-?0[xX][0-9a-fA-F]+$'
        s = re.sub(p, '', s)
        p = r' *Result: *\-?(?:(?:nan)|(?:inf))'
        s = re.sub(p, '', s)
        if 'Empty Stack' in s:
            s = ''
    elif runtime_name == 'WasmEdge_disableAOT_newer':
        s = re.sub(time_p, '', s)
        s = re.sub(wasm_path_p, '', s)
        p = r'Bytecode offset: 0[xX][0-9a-fA-F]+'
        s = re.sub(p, '', s)
        p = r' Code: 0[xX][0-9a-fA-F]+'
        s = re.sub(p, '', s)
        s = re.sub(num_p, '', s)
    elif runtime_name == 'wasmer_default_dump':
        s = re.sub(offset_p, '', s)
        s = re.sub(wasm_path_p, '', s)
    elif runtime_name == 'wasmi_interp':
        s = re.sub(offset_p, '', s)
        s = re.sub(wasm_path_p, '', s)
    elif runtime_name in ['iwasm_fast_interp_dump', 'iwasm_classic_interp_dump']:
        s = re.sub(r'^\n*$', '', s)
        p = r'^0x[a-f\d]+:i(?:(?:64)|(?:32))$'
        s = re.sub(p, '', s)
        p = r'^.*:f(?:(?:64)|(?:32))$'
        s = re.sub(p, '', s)
        p = r'^\d:ref\.func$'
        s = re.sub(p, '', s)
        p = r'^(?:(?:func)|(?:extern)):ref\.null$'
        s = re.sub(p, '', s)
    elif runtime_name == 'WAVM_default':
        pass
    else:
        assert 0, print(runtime_name)
    s = re.sub('\n', '', s)
    return s
