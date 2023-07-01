from pathlib import Path
from get_impls_util import get_lastest_uninst_impls, get_std_uninst_impls
from wasm_impl_util import uninstRuntime

from log_content_util.get_key_util import filter_normal_output

def check_whether_failed():
    pass

def get_logs(tc_paths, keys=None, process=False, use_lastest=False):
    pass
    if use_lastest:
        runtimes = get_lastest_uninst_impls()
    else:
        runtimes = get_std_uninst_impls()
    if keys is not None:
        runtimes = [r for r in runtimes if r.name in keys]
    logs = {}
    for runtime in runtimes:
        assert isinstance(runtime, uninstRuntime)
        logs[runtime.name] = set()
        for tc_path in tc_paths:
            assert Path(tc_path).exists()
            log = runtime.execute_and_collect_txt(tc_path)
            if process:
                log = filter_normal_output(log, runtime.name)
            logs[runtime.name].add(log)
    return logs


