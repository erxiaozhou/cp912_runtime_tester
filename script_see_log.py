from debug_util import get_log_by_impl
from pathlib import Path
from file_util import save_json


def get_runtime_log_from_dir(wasm_dir, result_path, impl_name='wasmer_default_dump'):
    wasm_dir = Path(wasm_dir)
    # result = {}
    result = []
    for p in wasm_dir.iterdir():
        log = get_log_by_impl(impl_name, p)
        result.append(log)
    result = list(set(result))
    save_json(result_path, result)


if __name__ == '__main__':
    get_runtime_log_from_dir('./ori_tcs/memory_init', 'tt/wasmer_memory_init_output.json')
    get_runtime_log_from_dir('./ori_tcs/data_drop', 'tt/wasmer_data_drop_output.json')
