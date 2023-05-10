from .wasm_impl_abc import Wasm_impl
from file_util import combine_path
from extract_dump import dump_data
from .util import move_based_executor
from .util import resultGenerator
from path_group_util import imlp_ori_path_group
from path_group_util import imlp_result_path_group
from pathlib import Path


class common_runtime(Wasm_impl):
    def __init__(self, name, executor, result_generator):
        super().__init__()
        self.name = name
        self.executor = executor
        self.result_generator = result_generator

    @classmethod
    def from_dict(cls, name, dict_, timeout_th=20):
        dump_dir = dict_['dump_dir']
        store_path = combine_path(dump_dir, dict_['dump_store_rpath'])
        ori_vstack_path = combine_path(dump_dir, dict_['dump_vstack_rpath'])
        ori_inst_path = combine_path(dump_dir, dict_['dump_instante_rpath'])
        ori_paths = imlp_ori_path_group(store_path, ori_vstack_path, ori_inst_path)
        bin_path = combine_path(dump_dir, dict_['bin_relative_path'])
        assert Path(bin_path).exists()
        dump_cmd_fmt = dict_['std_cmd'].format(bin_path, '{}')
        features = _get_features_from_dict(dict_)
        err_channel = dict_['err_channel']
        executor = move_based_executor(ori_paths, timeout_th, dump_cmd_fmt, err_channel)
        result_generator = resultGenerator(dict_['dump_extractor'], features)
        return cls(name, executor, result_generator)

    def execute_and_collect(self, tc_path, result_paths):
        assert isinstance(result_paths, imlp_result_path_group)
        self.executor.set_result_paths(result_paths)
        has_timeout, content = self.executor.execute(tc_path)
        self.result_generator.set_result_paths(result_paths)
        self.result_generator.has_timeout = has_timeout
        self.result_generator.log_content = content
        dumped_data = self._return_extracted_data()
        return dumped_data

    def _return_extracted_data(self):
        result = self.result_generator.get_result_obj()
        assert isinstance(result, dump_data)
        return result


def _get_features_from_dict(dict_):
    features = {}
    for k in ['support_multi_mem', 'support_v128', 'support_ref']:
        features[k] = dict_[k]
    return features