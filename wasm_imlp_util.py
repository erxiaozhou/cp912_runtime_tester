import subprocess
from abc import ABC
from abc import abstractclassmethod
from pathlib import Path
import shutil


class Wasm_impl(ABC):
    @abstractclassmethod
    def move_output(self, *args, **kwads):
        pass

    def clean(self):
        pass

    def execute_and_collect(self, tc_path, **args_for_collect):
        self.clean()
        append_info = self.execute(tc_path)
        return self.move_output(**args_for_collect, append_info=append_info)

    def execute(self, tc_path):
        cmd = self.cmd_format.format(tc_path)
        try:
            subprocess.run(cmd,timeout=self.timeout, shell=True)
        except subprocess.TimeoutExpired:
            return ['Timeout']

def check_mv_log(ori_log_path, tgt_log_path, need_mv):
    if need_mv and (tgt_log_path is not None):
        shutil.move(ori_log_path, tgt_log_path)


def single_file_dumped_data(ori_data_path, tgt_data_path, extractor_class):
    if Path(ori_data_path).exists():
        shutil.move(ori_data_path, tgt_data_path)
        return extractor_class(tgt_data_path)


def _check_all_exist(paths):
    first_exist = None
    for path in paths:
        if first_exist is None:
            first_exist = Path(path).exists()
        else:
            assert first_exist == Path(path).exists()


def check_file_mv(path_pairs, both_exist_check=True):
    assert isinstance(path_pairs, dict)
    if both_exist_check:
        _check_all_exist(path_pairs.keys())

    for src_path, tgt_path in path_pairs.items():
        if Path(src_path).exists():
            shutil.move(src_path, tgt_path)
        else:
            return False
    return True


def common_dump_behavior(ori_store_path,
                        tgt_store_path,
                        ori_vstack_path,
                        ori_log_path,
                        tgt_log_path,
                        tgt_vstack_path,
                        mv_dump_log,
                        dump_extractor_class):
    mv_pairs = {
        ori_store_path: tgt_store_path,
        ori_vstack_path: tgt_vstack_path
    }
    check_mv_log(ori_log_path, tgt_log_path, mv_dump_log)
    check_file_mv(mv_pairs, False)
    return dump_extractor_class(tgt_store_path, tgt_vstack_path)
