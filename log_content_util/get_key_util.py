from collections import Counter
from pathlib import Path
from .extract_keyword_from_content_util import func_sec_size_mismatch, runtime_self_unsupport
from .load_log_from_one_tc_result_util import load_log_from_one_tc_result
from .extract_keyword_from_content_util import fd_opcode, SIMD_unsupport, illegal_type, reference_unsupport
from .log_dict2key_util import log_dict2key
from .one_runtime_log_util import get_one_runtime_log, oneRuntimeLog


supported_modes = ['all', 's1', 's2', 's3', 'only_interesting', 'only_highlight']


def group_tc_names_by_log_key(tc_result_dirs, strategy):
    runtime_logs2tc_names = {}
    for tc_result_dir in tc_result_dirs:
        tc_name = Path(tc_result_dir).name
        runtime_logs = get_runtime_logs(tc_result_dir, strategy)
        runtime_logs2tc_names.setdefault(runtime_logs, []).append(tc_name)
    if strategy == 'only_highlight':
        # ! rewrite_dict 还没改
        log_key2tc_names = rewrite_dict(runtime_logs2tc_names)
        log_key2tc_names = {log_dict2key(k):v for k, v in log_key2tc_names.items()}
        return log_key2tc_names
    else:
        log_key2tc_names = {runtime_logs.processed_key: v for runtime_logs, v in runtime_logs2tc_names.items()}
        return log_key2tc_names


def get_runtime_logs(tc_result_dir, strategy):
    strategy2class = {
        'all': rawRuntimeLogs,
        's1': s1RuntimeLogs,
        's2': s2RuntimeLogs,
        's3': s3RuntimeLogs,
        'only_interesting': onlyInterestingRuntimeLogs,
        'only_highlight': onlyHighlightRuntimeLogs
    }
    assert strategy in strategy2class
    return strategy2class[strategy].from_tc_result_dir(tc_result_dir, strategy)


class runtimeLogs:
    def __init__(self, log_dict, strategy) -> None:
        self.log_dict = log_dict
        self.strategy = strategy
        self._processed_log_dict = None
        self._has_processed = False

    def _get_processed_log_dict(self, strategy):
        assert not self._has_processed
        assert strategy in supported_modes
        processed_log_dict = self._process_log_dict(self.log_dict)
        self._has_processed = True
        return processed_log_dict
    
    def _process_log_dict(self, log_dict):
        raise NotImplementedError

    # ! 写的不好，因为这个的key长的不直观，后面也很难根据原有的数据
    # ! 或许写成个 hash 比较好
    # ! 还有一个问题，就是和strategy的耦合，目前认为， strategy 可以写进 __init__ , 作为 self.xxxx
    @property
    def get_key(self):
        if self._processed_log_dict is None:
            self._processed_log_dict = self._get_processed_log_dict(self.strategy)
        return repr(self._processed_log_dict)
    
    @property
    def processed_key(self):
        return log_dict2key(self.get_key)

    def __hash__(self) -> int:
        return hash((self.get_key, self.strategy))
    
    def __eq__(self, o) -> bool:
        return self.get_key == o.get_key

    @classmethod
    def from_tc_result_dir(cls, tc_result_dir, strategy):
        return cls(load_log_from_one_tc_result(tc_result_dir), strategy)

def _no_cross_process_log_dict(one_runtime_log_process_func, log_dict):
    processed_log_dict = {}
    for runtime_name, s in log_dict.items():
        one_runtime_log = get_one_runtime_log(s,runtime_name)
        processed_log = one_runtime_log_process_func(one_runtime_log)
        if processed_log:
            processed_log_dict[runtime_name] = processed_log
    return processed_log_dict

class rawRuntimeLogs(runtimeLogs):
    def _process_log_dict(self, log_dict):
        return _no_cross_process_log_dict(oneRuntimeLog.keyword_part, log_dict)

class s1RuntimeLogs(runtimeLogs):
    def _process_log_dict(self, log_dict):
        return _no_cross_process_log_dict(oneRuntimeLog.summary_key_s1, log_dict)

class s2RuntimeLogs(runtimeLogs):
    def _process_log_dict(self, log_dict):
        return _no_cross_process_log_dict(oneRuntimeLog.summary_key_s2, log_dict)

class s3RuntimeLogs(runtimeLogs):
    def _process_log_dict(self, log_dict):
        return _no_cross_process_log_dict(oneRuntimeLog.summary_key_s3, log_dict)


class onlyInterestingRuntimeLogs(runtimeLogs):
    def _process_log_dict(self, log_dict):
        processed_log_dict = _no_cross_process_log_dict(oneRuntimeLog.summary_key_s3, log_dict)
        vals = list(processed_log_dict.values())
        # func_sec_size_mismatch 是所有runtime都不支持的
        if 0 < vals.count(func_sec_size_mismatch) < len(vals):
            for runtime_name in processed_log_dict.keys():
                processed_log_dict[runtime_name] = f'<masked because of {func_sec_size_mismatch}>'
        # 先把一些模糊的log通过其他runtime的报错推出来
        runtime_names = list(processed_log_dict.keys())
        has_fd = False
        # rule1: fd_opcode
        for v in processed_log_dict.values():
            if v == fd_opcode:
                has_fd = True
        # rule2: SIMD_unsupport
        if not has_fd:
            for processed_log in processed_log_dict.values():
                if processed_log == SIMD_unsupport:
                    has_fd = True
        # rule3: special runtimes
        if not has_fd:
            for runtime_name in ['iwasm_classic_interp_dump', 'iwasm_fast_interp_dump']:
                if processed_log_dict.get(runtime_name) == fd_opcode:
                    has_fd = True
        if has_fd:
            for runtime_name in runtime_names:
                if processed_log_dict[runtime_name] == illegal_type:
                    processed_log_dict[runtime_name] = runtime_self_unsupport
            for runtime_name in ['wasm3_dump', 'wasmi_interp', 'iwasm_classic_interp_dump', 'iwasm_fast_interp_dump']:
                if processed_log_dict.get(runtime_name) == fd_opcode:
                    processed_log_dict[runtime_name] = runtime_self_unsupport
        # reference
        has_ref = False
        for processed_log in processed_log_dict.values():
            if processed_log == reference_unsupport:
                has_ref = True
                break
        if has_ref:
            for runtime_name in runtime_names:
                if processed_log_dict[runtime_name] == illegal_type:
                    processed_log_dict[runtime_name] = runtime_self_unsupport

        # 某些runtime理应不支持的
        for runtime_name in runtime_names:
            if processed_log_dict[runtime_name] == runtime_self_unsupport:
                processed_log_dict.pop(runtime_name)
        return processed_log_dict

class onlyHighlightRuntimeLogs(onlyInterestingRuntimeLogs):
    pass

def rewrite_dict(log_key2tc_names):
    log_key2tc_names = {k.get_key:v for k, v in log_key2tc_names.items()}
    log_keywords = set()
    log_key_dict_reprs = list(log_key2tc_names.keys())
    repr2log_keyword_freq = {}

    for log_key_dict_repr in log_key_dict_reprs:
        log_key_dict =eval(log_key_dict_repr)
        values = list(log_key_dict.values())
        log_keywords.update(values)
        repr2log_keyword_freq[log_key_dict_repr] = {k:v/len(values) for k, v in Counter(values).items()}

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
        for log_key_dict_repr, c in repr2log_keyword_freq.items():
            if c.get(keyword, -5) == max_v:
                to_save_reprs.add(log_key_dict_repr)
    log_key2tc_names = {k:log_key2tc_names[k] for k in to_save_reprs}
    return log_key2tc_names
