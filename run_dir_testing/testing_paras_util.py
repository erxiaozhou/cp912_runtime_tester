from get_impls_util import get_std_impls
from get_impls_util import get_std_release_impls
from pathlib import Path
from file_util import save_json
from time import time
from .tester import Tester
from .tester_util import testerExecInfo
from .tester_util import testerExecPaths
from .tester import noMutationTester, randomByteMutationTester


class testingInfoSaver:
    def __init__(self, paras):
        assert isinstance(paras, mutationParas)
        self.paras = paras
        self.start_time = None
        self.end_time = None
    
    def save_config(self, exec_info, config_path=None):
        assert isinstance(exec_info, testerExecInfo)
        if config_path is None:
            config_path = self.paras.tester_exec_paths.config_log_path
        d = {}
        d['config'] = self.paras.to_dict_for_save
        d['exec_info'] = exec_info.to_dict
        d['time'] = self.exec_time
        save_json(config_path, d)
    
    def init_start_time(self):
        self.start_time = time()
    
    def init_end_time(self):
        self.end_time = time()
    
    @property
    def exec_time(self):
        assert self.start_time is not None
        assert self.end_time is not None
        return self.end_time - self.start_time


class mutationParas:
    def __init__(self, tester, tester_exec_paths, tested_dir, use_release) -> None:
        self.tester = tester
        assert isinstance(tester_exec_paths, testerExecPaths)
        self.tester_exec_paths = tester_exec_paths
        self.tested_dir = tested_dir
        # ! use_release写的不好，耦合太重，准备改
        self.use_release = use_release
        # ! 在这里获取impls是好的，但是这个写法有点凑合，还要再想想
        if use_release:
            impls = get_std_release_impls()
        else:
            impls = get_std_impls()
        self.impls = impls
    
    @classmethod
    def get_paras_with_mutation(cls, tested_dir, result_base_dir, one_tc_limit=50, mutate_num=5, mutate_prob=1, use_release=False, tester_exec_paths=None):
        paras = {
            'tested_dir': tested_dir,
            'use_release': use_release,
            'tester_exec_paths': get_tester_exec_paths(result_base_dir, tester_exec_paths),
            'tester': randomByteMutationTester(one_tc_limit=one_tc_limit, mutate_num=mutate_num, mutate_prob=mutate_prob)
        }
    
        return cls(**paras)
    
    @classmethod
    def get_no_mutation_paras(cls, result_base_dir, tested_dir, tester_exec_paths=None):
        paras = {
            'tested_dir': tested_dir,
            'tester': noMutationTester(),
            'use_release': False,
            'tester_exec_paths': get_tester_exec_paths(result_base_dir, tester_exec_paths)
        }
        return cls(**paras)
    
    @property
    def to_dict_for_save(self):
        d = {}
        for name, attr in self.__dict__.items():
            if isinstance(attr, Path):
                d[name] = str(attr)
            elif isinstance(attr, testerExecPaths):
                d[name] = attr.to_str_dict
            # ! 下面这行最好是写成基于类型检查的
            elif name == 'impls':
                impls = attr
                d['runtimes'] = [impl.name for impl in impls]
            elif isinstance(attr, Tester):
                d[name] = repr(attr)
            else:
                d[name] = attr
        return d


def get_tester_exec_paths(result_base_dir, tester_exec_paths=None):
    if tester_exec_paths is None:
        tester_exec_paths = testerExecPaths.from_result_base_dir(result_base_dir)
    return tester_exec_paths
