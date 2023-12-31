import subprocess
from pathlib import Path
from file_util import check_dir
from extract_dump import is_failed_content
from get_impls_util import get_std_uninst_impls
from get_impls_util import get_lastest_uninst_impls
from wasm_impl_util import uninstRuntime


uninst_impls = get_std_uninst_impls()
uninst_impls_dict = {impl.name: impl for impl in uninst_impls}

latest_impls = get_lastest_uninst_impls()
latest_impls_dict = {impl.name: impl for impl in latest_impls}


def wasm2wat(wasm_path, wat_path):
    cmd = 'wasm2wat {} -o {}'.format(wasm_path, wat_path)
    subprocess.run(cmd, timeout=20, shell=True)


def wasms_dir2wats(base_dir, result_dir):
    base_dir = Path(base_dir)
    result_dir = check_dir(result_dir)
    for wasm_path in base_dir.iterdir():
        if wasm_path.name[-5:] != '.wasm':
            continue
        print(wasm_path)
        stem = wasm_path.name[:-5]
        wat_path = result_dir / (stem+'.wat')
        wasm2wat(wasm_path, wat_path)


# lastest ===========================================================


def get_log_by_lastest_impl(impl, wasm_wat_path):
    if isinstance(impl, str):
        impl_name = impl
        impl = latest_impls_dict[impl_name]
    assert isinstance(impl, uninstRuntime)
    log = impl.execute_and_collect_txt(wasm_wat_path)
    return log


def is_executable_by_latest_impl(impl, wasm_wat_path):
    log = get_log_by_lastest_impl(impl, wasm_wat_path)
    if is_failed_content(log):
        return False
    else:
        return True


# common ===========================================================


def get_log_by_impl(impl, wasm_wat_path):
    if isinstance(impl, str):
        impl_name = impl
        impl = uninst_impls_dict[impl_name]
    assert isinstance(impl, uninstRuntime)
    log = impl.execute_and_collect_txt(wasm_wat_path)
    return log


def is_executable_by_impl(impl, wasm_wat_path):
    log = get_log_by_impl(impl, wasm_wat_path)
    if is_failed_content(log):
        return False
    else:
        return True
