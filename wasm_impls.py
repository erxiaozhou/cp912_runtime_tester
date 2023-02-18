from pathlib import Path
import shutil
from extract_dump import iwasm_classic_interp_dumped_data
from extract_dump import wasmi_dumped_data
from extract_dump import wasm3_dumped_data
from extract_dump import wasmedge_dumped_data
from extract_dump import wasmer_dumped_data
from wasm_imlp_util import Wasm_impl, check_file_mv
from file_util import combine_path, remove_file_without_exception


class common_runtime(Wasm_impl):
    def __init__(self, name, dump_cmd_fmt, ori_store_path, ori_vstack_path,
                 ori_log_path, dump_extractor_class, ori_cmd,
                 support_multi_mem= False,
                 support_v128=False, support_ref=False) -> None:
        super().__init__()
        self.dump_cmd_fmt = dump_cmd_fmt
        self.name = name
        self.ori_store_path = ori_store_path
        self.ori_vstack_path = ori_vstack_path
        self.ori_log_path = ori_log_path
        self.dump_extractor_class = dump_extractor_class
        self.ori_cmd = ori_cmd
        self.timeout = 10
        # default value
        self.support_multi_mem = support_multi_mem
        self.support_v128 = support_v128
        self.support_ref = support_ref

    @classmethod
    def from_dict(cls, name, dict_):
        ori_store_path = combine_path(dict_['dump_dir'],
                                      dict_['dump_store_relative_path'])
        ori_vstack_path = combine_path(dict_['dump_dir'],
                                       dict_['dump_vstack_relative_path'])
        bin_path = combine_path(dict_['dump_dir'], dict_['bin_relative_path'])
        ori_bin_path = combine_path(dict_['standard_dir'],
                                    dict_['bin_relative_path'])
        ori_log_path = dict_['ori_log_path']
        dump_cmd = dict_['dump_cmd'].format(bin_path, '{}', '{}')
        ori_cmd = dict_['dump_cmd'].format(ori_bin_path, '{}', ori_log_path)
        dump_extractor_class = dict_['dump_extractor']
        support_multi_mem = dict_['support_multi_mem']
        support_v128 = dict_['support_v128']
        support_ref = dict_['support_ref']
        return cls(name, dump_cmd, ori_store_path, ori_vstack_path,
                   ori_log_path, dump_extractor_class, ori_cmd, 
                   support_multi_mem, support_v128, support_ref)

    def clean(self):
        remove_file_without_exception(self.ori_store_path)
        remove_file_without_exception(self.ori_vstack_path)
        remove_file_without_exception(self.ori_log_path)

    def move_output(self,
                    tgt_store_path=None,
                    tgt_vstack_path=None,
                    tgt_log_path=None,
                    **kwads):
        mv_pairs = {
            self.ori_store_path: tgt_store_path,
            self.ori_vstack_path: tgt_vstack_path
        }
        check_file_mv(mv_pairs, False)
        # execute_and_collect
        if 'append_info' in kwads:
            append_info = kwads['append_info']
        else:
            append_info = {}
        # set supput_v128 and support_ref
        result = self.dump_extractor_class(tgt_store_path, tgt_vstack_path, tgt_log_path, append_info)
        result.support_v128 = self.support_v128
        result.support_ref = self.support_ref
        result.support_multi_mem = self.support_multi_mem
        result.name = self.name
        return result
