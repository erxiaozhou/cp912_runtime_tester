from collections import Counter
import os
import re
from pathlib import Path
import random
import struct
from exec_util import exec_one_tc
from extract_dump import is_failed_content
from extract_dump.data_comparer import are_different
from file_util import bytes2f32, pickle_dump, pickle_load, print_ba, read_bytes, read_json, uint2bytes
from get_impls_util.get_impls_util import get_std_impls
from get_impls_util.impl_paras_std import impl_paras_std
from load_results_util import load_results_from_one_dumped_data_dir
from retrive_diff_num_from_reason_summary import analyze_a_tc
from run_dir_testing.tester_util import testerExecInfo
from log_content_util.one_runtime_log_util import oneRuntimeLog
from get_impls_util import get_lastest_halfdump_impls, get_lastest_uninst_impls

class test_base:
    def __init__(self) -> None:
        self.a = 1
        self.b = 2
        self.c = 3
        self.init_d()
    
    def to_dict(self, path=None):
        # TODO
        data = {}
        data.update(self.__dict__)
        if path is not None:
            pickle_dump(path, data)
        return data
    
    def init_d(self):
        self.d = 10
    
    def print(self, s):
        print('12345' + s)


class test_class(test_base):
    def __init__(self) -> None:
        super().__init__()
        self.e = 4
    def to_dict(self, path=None):
        # return super().to_dict(path)
        new_obj = test_base()
        for k in new_obj.__dict__.keys():
            new_obj.__dict__[k] = self.__dict__[k]
        return new_obj.__dict__

    def init_d(self):
        self.d = 15


def process_a_key(key):
    data = eval(key)
    assert isinstance(data, tuple)


def copy_dirs_and_renamed_filename_start_with_ld():
    base_dir = '/home/std_runtime_test/lastest_runtimes'
    base_dir = Path(base_dir)
    names = [p.name for p in base_dir.iterdir()]
    for name in names:
        assert name.startswith('ori')
        new_name = re.sub(r'^ori', 'ld', name)
        os.system(f'cp -r {base_dir/name} {base_dir/new_name}')



if __name__ == '__main__':
    # print(analyze_a_tc('/host_data/rewrite/v19.1_no_mutation/dumped_data//memory.init_757'))
    dumped_tc_dir = '/host_data/rewrite/v19.1_no_mutation/dumped_data/v128.bitselect_221'
    rs = load_results_from_one_dumped_data_dir(dumped_tc_dir)
    print(are_different(rs))

        

