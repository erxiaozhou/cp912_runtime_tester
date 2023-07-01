from pathlib import Path
from file_util import get_time_string
from .testing_paras_util import mutationParas
from .testing_paras_util import testingInfoSaver
import time


def test_with_mutation(paras):
    assert isinstance(paras, mutationParas)
    tester = paras.tester
    impls = paras.impls
    # print('tester', repr(tester))
    # assert 0
    
    tc_paths_iterator = _get_tcs_name_and_path(paras.tested_dir)
    saver = testingInfoSaver(paras)
    saver.init_start_time()
    exec_info = tester.run_testing(paras.tester_exec_paths, impls, tc_paths_iterator)
    saver.init_end_time()
    print('tester', repr(tester))

    saver.save_config(exec_info)
    time.sleep(1)
    config_backup_path = _get_backup_config_filename(paras.tester_exec_paths.config_log_path)
    saver.save_config(exec_info, config_backup_path)


def _get_backup_config_filename(config_log_path):
    config_stem = Path(config_log_path).stem
    config_base_dir = Path(config_log_path).parent
    config_backup_name = f'{config_stem}{get_time_string()}.json'
    config_backup_path = config_base_dir / config_backup_name
    return config_backup_path


def _get_tcs_name_and_path(dir_):
    dir_ = Path(dir_)
    for p in dir_.iterdir():
        if p.suffix == '.wasm':
            path = str(p)
            tc_name = p.stem
            yield (tc_name, path)
