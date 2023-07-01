from file_util import combine_path
from extract_dump import dumpData
from .util import exec_impl_and_collect_log
from .wasm_impl_abc import WasmImpl
from extract_dump import uninstResultInitializer
from .wasm_impls import get_features_from_dict


class collectLogExecutor:
    def __init__(self, timeout_th, cmd_fmt, err_channel) -> None:
        self.timeout = timeout_th
        self.cmd_fmt = cmd_fmt
        assert err_channel in ['stdout', 'stderr']
        self.err_channel = err_channel

    def execute(self, wasm_path):
        paras = {
            'cmd_fmt': self.cmd_fmt,
            'timeout_th': self.timeout,
            'wasm_path': wasm_path,
            'err_channel': self.err_channel
        }
        has_timeout, log = exec_impl_and_collect_log(**paras)
        return has_timeout, log


class logResultGenerator:
    def __init__(self, features, name):
        self.features = features
        self.name = name
        self.has_timeout = None
        self.log_content = None
    
    @property
    def result_obj_paras(self):
        return {
            'name': self.name,
            'features': self.features,
            'has_timeout': self.has_timeout,
            'log_content': self.log_content
        }
    
    def get_result_obj(self):
        return uninstResultInitializer(**self.result_obj_paras)


class uninstRuntime(WasmImpl):
    def __init__(self, name, executor, result_generator) -> None:
        self.name = name
        self.executor = executor
        self.result_generator = result_generator

    def execute_and_collect_txt(self, wasm_path):
        # ! To rewrite 
        has_timeout, log = self.executor.execute(wasm_path)
        if has_timeout:
            return 'From uninstRuntime: Timeout'
        return log
    
    def execute_and_collect(self, wasm_path, *args, **kwargs):
        has_timeout, log = self.executor.execute(wasm_path)
        self.result_generator.has_timeout = has_timeout
        self.result_generator.log_content = log
        result = self.result_generator.get_result_obj()
        assert isinstance(result, dumpData)
        return result
    
    @classmethod
    def from_std_dict(cls, name, dict_, thmeout_th=20):
        return cls._from_dict_core(name, dict_, 'standard_dir', thmeout_th)
    
    @classmethod
    def from_lastest_dict(cls, name, dict_, thmeout_th=20):
        return cls._from_dict_core(name, dict_, 'lastest_dir', thmeout_th)
 
    @classmethod
    def _from_dict_core(cls, name, dict_, dict_type, thmeout_th=20):
        assert dict_type in ['standard_dir', 'lastest_dir']
        cmd_fmt, err_channel = _get_paras_from_dict(dict_, dict_type)
        executor = collectLogExecutor(thmeout_th, cmd_fmt, err_channel)
        
        features = get_features_from_dict(dict_)
        result_generator = logResultGenerator(features, name)
        return cls(name, executor, result_generator)


def _get_paras_from_dict(dict_, runtime_dir_name):
    assert runtime_dir_name in ['standard_dir', 'lastest_dir']
    bin_path = combine_path(dict_[runtime_dir_name], dict_['bin_relative_path'])
    if runtime_dir_name == 'standard_dir':
        cmd_fmt = dict_['std_cmd'].format(bin_path, '{}')
    else:
        cmd_fmt = dict_['lastest_cmd'].format(bin_path, '{}')
    err_channel = dict_['err_channel']
    assert err_channel in ['stdout', 'stderr']
    return cmd_fmt, err_channel
