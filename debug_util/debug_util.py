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


# wasmer ===========================================================
# def is_executable_by_wasmerlog(wasm_wat_path):
#     out_content, err_content = _std_wasmer_execute_core(wasm_wat_path)
#     if is_failed_content(err_content) or is_failed_content(out_content):
#         return False
#     else:
#         return True


# def print_execute_wasmer_result(wasm_wat_path):
#     out_content, err_content = _std_wasmer_execute_core(wasm_wat_path)
#     print('err_content:-')
#     print(err_content)
#     print('out_content:-')
#     print(out_content)


# def _std_wasmer_execute_core(wasm_wat_path):
#     fmt = '/home/zph/DGit/wasm_projects/std_runtime_test/ori_wasmer_default/target/release/wasmer {} -i to_test'
#     cmd = fmt.format(wasm_wat_path)
#     p = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, timeout=10)
#     out_content = p.stdout.read()
#     err_content = p.stderr.read()
#     out_content = str(out_content)
#     err_content = str(err_content)
#     return out_content, err_content


# iwasm ===========================================================
# def is_executable_by_iwasmlog(wasm_wat_path):
#     out_content, err_content = _std_iwasm_execute_core(wasm_wat_path)
#     if is_failed_content(err_content) or is_failed_content(out_content):
#         return False
#     else:
#         return True


# def print_execute_iwasm_result(wasm_wat_path):
#     out_content, err_content = _std_iwasm_execute_core(wasm_wat_path)
#     print('err_content:-')
#     print(err_content)
#     print('out_content:-')
#     print(out_content)


# def _std_iwasm_execute_core(wasm_wat_path):
#     fmt = '/home/zph/DGit/wasm_projects/std_runtime_test/ori_iwasm_interp_classic/product-mini/platforms/linux/build/iwasm  --heap-size=0 -f to_test {}'
#     cmd = fmt.format(wasm_wat_path)
#     p = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, timeout=10)
#     out_content = p.stdout.read()
#     err_content = p.stderr.read()
#     out_content = str(out_content)
#     err_content = str(err_content)
#     return out_content, err_content
