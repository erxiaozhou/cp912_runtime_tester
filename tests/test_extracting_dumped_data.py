import pytest
from get_imlps_util import get_std_imlps  # may error; should check the name again
# a path to a .wasm file which is executable; there is no local, global, memory within it
executable_wasm_path1 = None
# a path to a .wasm file which is executable; there exist local, global, memory ...
executable_wasm_path2 = None

# a path to a .wasm file which is unexecutable; there is no local, global, memory within it
unexecutable_wasm_path1 = None
# a path to a .wasm file which is unexecutable; there exist local, global, memory ...
unexecutable_wasm_path2 = None


paras = [
    [executable_wasm_path1, {
        'log_has_failed_content': False,
        'can_initialize': True,
        'has_timeout': False,
        'has_instance': True,
        'global_bytes': [],
        'global_types': [],
        'table_num': 0,
        'mem_num': 0,
        'default_mem_length': 0,
        'default_mem_page_num': 0,
        'stack_num': 1,
        'stack_types': 0,  # to rewrite
        'stack_bytes_process_nan':0,  # to rewrite
    }],
    [executable_wasm_path2, {
        'log_has_failed_content': False,
        'can_initialize': True,
        'has_timeout': False,
        'has_instance': True,
        'global_bytes': [],  # to rewrite
        'global_types': [],  # to rewrite
        'table_num': 1,
        'mem_num': 1,
        'default_mem_length': 64 * 1024,
        'default_mem_page_num': 1,
        'stack_num': 1,  # to rewrite
        'stack_types': 0,  # to rewrite
        'stack_bytes_process_nan':0,  # to rewrite
    }]
]


# @pytest.mark.parametrize('wasm_path, expected_data_dict', paras)
# def test_executable_paths(wasm_path, expected_data_dict):
#     impls = get_std_imlps()
#     for impl in impls:
#         for attr_name, value in expected_data_dict.items():
#             assert getattr(impl, attr_name) == value
