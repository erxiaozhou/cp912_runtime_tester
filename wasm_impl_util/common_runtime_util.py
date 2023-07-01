from file_util import byte2str, remove_file_without_exception
import subprocess
from pathlib import Path
import shutil
from .util import exec_impl_and_collect_log
from path_group_util import cmnImplResultPathGroup


class moveBasedExecutor:
    # TODO executor class 之间应该是有可以合并的地方的，后面可以考虑合并
    def __init__(self, ori_paths,
                timeout_th,
                dump_cmd_fmt, err_channel):
        assert isinstance(ori_paths, fullDumpOriPathGroup)
        self._ori_paths = ori_paths
        self.timeout = timeout_th
        self.dump_cmd_fmt = dump_cmd_fmt
        self._result_paths = None
        assert err_channel in ['stdout', 'stderr']
        self.err_channel = err_channel

    def execute(self, tc_path):
        self._clean_previous_dumped_data()
        has_timeout, content = self._execute(tc_path, self.err_channel)
        self._move_output()
        return has_timeout, content
    
    def _clean_previous_dumped_data(self):
        for p in self._ori_paths.paths:
            remove_file_without_exception(p)
        for p in self._result_paths.paths:
            remove_file_without_exception(p)
    
    def _execute(self, wasm_path, err_channel):
        # 把这部分放进函数_execute而不是直接放进上面的executre是考虑到后面可能会修改cmd所需要的参数，比如 cmd 可能会需要更多参数
        has_timeout, content = exec_impl_and_collect_log(self.dump_cmd_fmt, self.timeout, wasm_path, err_channel)
        return has_timeout, content

    def _move_output(self):
        mv_pairs = {
            self.ori_store_path: self.tgt_store_path,
            self.ori_vstack_path: self.tgt_vstack_path,
            self.ori_inst_path: self.tgt_inst_path
        }
        # ! 这个False要不要改成 True
        _check_file_mv(mv_pairs, False)
    
    def set_result_paths(self, result_paths):
        assert isinstance(result_paths, cmnImplResultPathGroup)
        self._result_paths = result_paths

    @property
    def tgt_vstack_path(self):
        return self._result_paths.vstack_path
    
    @property
    def tgt_store_path(self):
        return self._result_paths.store_path
    
    @property
    def tgt_inst_path(self):
        return self._result_paths.inst_path
    
    @property
    def ori_store_path(self):
        return self._ori_paths.store_path
    
    @property
    def ori_vstack_path(self):
        return self._ori_paths.vstack_path
    
    @property
    def ori_inst_path(self):
        return self._ori_paths.inst_path


class dumpedResultGenerator:
    def __init__(self, dump_extractor_class, features=None):
        self.dump_extractor_class = dump_extractor_class
        assert isinstance(features, dict)
        self.features = features
        self._result_paths = None
        self.has_timeout = None
        self.log_content = None

    def set_result_paths(self, result_paths):
        assert isinstance(result_paths, cmnImplResultPathGroup)
        self._result_paths = result_paths

    @property
    def result_obj_paras(self):
        # name 好像不用设置
        data = {}
        data['paths'] = self._result_paths
        data['features'] = self.features
        assert self.has_timeout is not None
        data['has_timeout'] = self.has_timeout
        data['log_content'] = self.log_content
        return data

    def check_all_paras_are_initialized(self):
        all_initialized = True
        for v in self.result_obj_paras.values():
            if v is None:
                all_initialized = False
        assert all_initialized

    def get_result_obj(self):
        self.check_all_paras_are_initialized()
        paras = self.result_obj_paras
        result = self.dump_extractor_class(**paras)
        return result


class fullDumpOriPathGroup:
    def __init__(self, ori_store_path, ori_vstack_path, ori_inst_path):
        self.store_path = ori_store_path
        self.vstack_path = ori_vstack_path
        self.inst_path = ori_inst_path
    
    @property
    def paths(self):
        return [
            self.store_path,
            self.vstack_path,
            self.inst_path
        ]


def _check_file_mv(path_pairs, both_exist_check=True):
    assert isinstance(path_pairs, dict)
    if both_exist_check:
        _check_all_exist(path_pairs.keys())

    for src_path, tgt_path in path_pairs.items():
        if Path(src_path).exists():
            shutil.move(src_path, tgt_path)


def _check_all_exist(paths):
    first_exist = None
    for path in paths:
        if first_exist is None:
            first_exist = Path(path).exists()
        else:
            assert first_exist == Path(path).exists()
