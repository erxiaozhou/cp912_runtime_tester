from .wasm_impl_abc import WasmImpl
from file_util import combine_path
from extract_dump import dumpData
from .common_runtime_util import moveBasedExecutor
from .common_runtime_util import dumpedResultGenerator
from .common_runtime_util import fullDumpOriPathGroup
from path_group_util import cmnImplResultPathGroup
from pathlib import Path


class fullDumpRuntime(WasmImpl):
    def __init__(self, name, executor, result_generator):
        self.name = name
        self.executor = executor
        self.result_generator = result_generator

    @classmethod
    def from_dict(cls, name, dict_, timeout_th=20):
        dump_dir = dict_['dump_dir']
        store_path = combine_path(dump_dir, dict_['dump_store_rpath'])
        ori_vstack_path = combine_path(dump_dir, dict_['dump_vstack_rpath'])
        ori_inst_path = combine_path(dump_dir, dict_['dump_instante_rpath'])
        ori_paths = fullDumpOriPathGroup(store_path, ori_vstack_path, ori_inst_path)
        bin_path = combine_path(dump_dir, dict_['bin_relative_path'])
        assert Path(bin_path).exists(), print(bin_path)
        dump_cmd_fmt = dict_['std_cmd'].format(bin_path, '{}')
        err_channel = dict_['err_channel']
        executor = moveBasedExecutor(ori_paths, timeout_th, dump_cmd_fmt, err_channel)

        features = get_features_from_dict(dict_)
        result_generator = dumpedResultGenerator(dict_['dump_extractor'], features)
        return cls(name, executor, result_generator)

    def execute_and_collect(self, tc_path, result_paths):
        assert isinstance(result_paths, cmnImplResultPathGroup)
        self.executor.set_result_paths(result_paths)
        has_timeout, content = self.executor.execute(tc_path)

        self.result_generator.set_result_paths(result_paths)
        self.result_generator.has_timeout = has_timeout
        self.result_generator.log_content = content
        result = self.result_generator.get_result_obj()
        assert isinstance(result, dumpData)
        return result


def get_features_from_dict(dict_):
    features = {}
    for k in ['support_multi_mem', 'support_v128', 'support_ref']:
        features[k] = dict_[k]
    return features