from nan_detect_util import process_f32_64
from .process_dump_data_util import get_int, get_u64
from .process_dump_data_util import get_f32
from .process_dump_data_util import get_f64
from .util import fullDumpResultInitializer
from pathlib import Path


class iwasmFastInterpDumpedResult(fullDumpResultInitializer):
    def __init__(self, paths, has_timeout, features=None, log_content=None):
        name = 'iwasm_fast_interp_dump'
        super().__init__(paths, has_timeout, features, log_content, name)
        if Path(self.vstack_path).exists():
            self._init_stack(self.vstack_path)

        if Path(self.store_path).exists():
            self._init_store(self.store_path)

    def _init_store(self, store_path):
        with open(store_path, 'rb') as f:
            global_count_bytes = f.read(4)
            self.global_num = get_int(global_count_bytes)
            for i in range(self.global_num):
                ty = f.read(1)
                if ty == b'\x7F':
                    self.global_types.append('i32')
                    cur_bytes = f.read(4)
                    self.global_bytes.append(cur_bytes)
                    self.global_infered_vals.append(get_int(cur_bytes))
                elif ty == b'\x7E':
                    self.global_types.append('i64')
                    cur_bytes = f.read(8)
                    self.global_bytes.append(cur_bytes)
                    self.global_infered_vals.append(get_int(cur_bytes))
                elif ty == b'\x7D':
                    self.global_types.append('f32')
                    cur_bytes = f.read(4)
                    self.global_bytes.append(cur_bytes)
                    self.global_infered_vals.append(get_f32(cur_bytes))
                elif ty == b'\x7C':
                    self.global_types.append('f64')
                    cur_bytes = f.read(8)
                    self.global_bytes.append(cur_bytes)
                    self.global_infered_vals.append(get_f64(cur_bytes))
                elif ty == b'\x7B':
                    assert 0
                    self.global_types.append('v128')
                    cur_bytes = f.read(16)
                    self.global_bytes.append(cur_bytes)
                    self.global_infered_vals.append([x for x in bytearray(cur_bytes)])
                    # if get_int(f.read(1)):
                    #     self.global_muts.append(True)
                    # else:
                    #     self.global_muts.append(False)
            self.table_num = get_int(f.read(4))
            if self.table_num > 0:
                self.default_table_len = get_int(f.read(4))
                self.default_table_func_idxs = []
                for i in range(self.default_table_len):
                    self.default_table_func_idxs.append(get_int(f.read(4)))
            else:
                self.default_table_len = 0
               
            self.mem_num = get_int(f.read(4)) 
            if self.mem_num > 0:
                self.default_mem_length = get_u64(f.read(8))
                self.default_mem_page_num = get_int(f.read(4))
                self.default_mem_data = f.read(self.default_mem_length)


    def _init_stack(self, stack_path):
        with open(stack_path, 'rb') as f:
            self.stack_num = get_int(f.read(8))
            for i in range(self.stack_num):
                ty = f.read(1)
                processed_ba = None
                if ty == b'\x7F':
                    self.stack_types.append('i32')
                    cur_bytes = f.read(4)
                    self.stack_infered_vals.append(get_int(cur_bytes))
                elif ty == b'\x7E':
                    self.stack_types.append('i64')
                    cur_bytes = f.read(8)
                    self.stack_infered_vals.append(get_int(cur_bytes))
                elif ty == b'\x7D':
                    self.stack_types.append('f32')
                    cur_bytes = f.read(4)
                    self.stack_infered_vals.append(get_f32(cur_bytes))
                    processed_ba = process_f32_64(cur_bytes)
                elif ty == b'\x7C':
                    self.stack_types.append('f64')
                    cur_bytes = f.read(8)
                    self.stack_infered_vals.append(get_f64(cur_bytes))
                    processed_ba = process_f32_64(cur_bytes)
                elif ty == b'\x7B':
                    self.stack_types.append('v128')
                    cur_bytes = f.read(16)
                    self.stack_infered_vals.append([x for x in bytearray(cur_bytes)])
                elif ty == b'\x70':
                    cur_bytes = bytearray([])
                    self.stack_infered_vals.append([])
                    self.stack_types.append('funcref')
                    # cur_bytes = f.read(4)
                    # func_idx = get_int(cur_bytes)
                    # is_null_bytes = f.read(4)
                    # is_null = get_int(is_null_bytes)
                    # processed_ba = bytearray(cur_bytes) + bytearray(is_null_bytes)
                    # self.stack_infered_vals.append((func_idx, is_null))
                elif ty == b'\x6F':
                    cur_bytes = bytearray([])
                    self.stack_infered_vals.append([])
                    self.stack_types.append('externref')
                    # cur_bytes = f.read(4)
                    # content_as_int = get_int(cur_bytes)
                    # is_null_bytes = f.read(4)
                    # is_null = get_int(is_null_bytes)
                    # processed_ba = bytearray(cur_bytes) + bytearray(is_null_bytes)
                    # self.stack_infered_vals.append((content_as_int, is_null))
                else:
                    assert 0
                self.stack_bytes.append(cur_bytes)
                if processed_ba is None:
                    processed_ba = bytearray(cur_bytes)
                self.stack_bytes_process_nan.append(processed_ba)
