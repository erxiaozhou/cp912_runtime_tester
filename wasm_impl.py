import os
from abc import ABC
from abc import abstractclassmethod
from pathlib import Path
import shutil
# from pathlib import
from file_util import check_dir
from iwasm_extract_dump import iwasm_dumped_data
from wasmi_extract_dump import wasmi_dumped_data
from wasm3_extract_dump import wasm3_dumped_data
from wasmedge_extract_dump import wasmedge_dumped_data
from wasmer_extract_dump import wasmer_dumped_data


# def _execute(fmt, tc_path):


class Wasm_impl(ABC):

    @abstractclassmethod
    def move_output(self, *args, **kwads):
        pass

    def execute_and_collect(self, tc_path, **args_for_collect):
        self.execute(tc_path)
        return self.move_output(**args_for_collect)

    def execute(self, tc_path):
        cmd = self.cmd_format.format(tc_path)
        os.system(cmd)
    
    def name_generator(self, base_dir, appended_part):
        base_dir = Path(base_dir)
        filename = '{}_{}'.format(self.name, appended_part)
        return base_dir/filename



class wasmi_dump(Wasm_impl):
    cmd_format = "/home/zph/DGit/wasm_projects/wasmi/target/debug/wasmi_cli {} _start 2> dpd_wasmi_err_log"
    name = 'wasmi_dump'

    def move_output(self, tgt_store_path, tgt_stack_path, mv_dump_log=False, tgt_log_path=None, **kwads):
        # TODO 暂定这里可以是 文件或者文件夹
        store_data_path = '/home/zph/DGit/wasm_projects/wasmi/memory_data'
        stack_data_path = 'stack_data/stack_data_0_0'
        if mv_dump_log and (tgt_log_path is not None):
            shutil.move('dpd_wasmi_err_log', tgt_log_path)
        # if Path(stack_data_path).exists():
        #     shutil.move(stack_data_path, tgt_stack_path)
        if Path(store_data_path).exists():
            assert Path(stack_data_path).exists()
        if Path(store_data_path).exists():
            shutil.move(store_data_path, tgt_store_path)
            return wasmi_dumped_data(tgt_store_path)


class wasmi_standard(Wasm_impl):
    cmd_format = "/home/zph/DGit/wasm_projects/standard_wasmi/wasmi/target/debug/wasmi_cli {} _start 2> standard_wasmi_erro_log"
    name = 'wasmi_standard'

    def move_output(self, tgt_log_path=None, **kwads):
        shutil.move('standard_wasmi_erro_log', tgt_log_path)


class iwasm_dump(Wasm_impl):
    # 讲道理错误什么的会用2>写进，但是这个不大一样，2>好像不会有什么有用信息
    cmd_format = "/home/zph/DGit/wasm_projects/iwasm_projects/wmrm_911/product-mini/platforms/linux/build/iwasm --heap-size=0 -f _start {} > dpd_iwasm_err_log"
    name = 'iwasm_dump'

    def move_output(self, tgt_data_path, mv_dump_log=False, tgt_log_path=None, **kwads):
        # TODO 还是有点耦合
        ori_data_path = '/home/zph/DGit/wasm_projects/wasm-micro-runtime/data_path'
        if mv_dump_log and (tgt_log_path is not None):
            shutil.move('dpd_iwasm_err_log', tgt_log_path)
        if Path(ori_data_path).exists():
            shutil.move(ori_data_path, tgt_data_path)
            return iwasm_dumped_data(tgt_data_path)


class iwasm_standard(Wasm_impl):
    cmd_format = "/home/zph/DGit/wasm_projects/standard_iwasm/wasm-micro-runtime/product-mini/platforms/linux/build/iwasm --heap-size=0 -f _start {} > standard_iwasm_erro_log"
    name = 'iwasm_standard'

    def move_output(self, tgt_log_path=None, **kwads):
        shutil.move('standard_iwasm_erro_log', tgt_log_path)


class wasm3_dump(Wasm_impl):
    # 讲道理错误什么的会用2>写进，但是这个不大一样，2>好像不会有什么有用信息
    # TODO 拿不到报错信息，具体怎么写再研究吧
    cmd_format = "/home/zph/DGit/wasm_projects/runtime_test/wasm3/build/wasm3 --func _start {} > dpd_wasm3_err_log"
    name = 'wasm3_dump'

    def move_output(self, tgt_data_path=None, mv_dump_log=False, tgt_log_path=None, **kwads):
        ori_data_path = '/home/zph/DGit/wasm_projects/runtime_test/wasm3/dump_data'
        if mv_dump_log and (tgt_log_path is not None):
            shutil.move('dpd_wasm3_err_log', tgt_log_path)
        if Path(ori_data_path).exists():
            shutil.move(ori_data_path, tgt_data_path)
            return wasm3_dumped_data(tgt_data_path)


class wasmer_dump(Wasm_impl):
    cmd_format = "/home/zph/DGit/wasm_projects/runtime_test/wasmer/target/debug/wasmer run {} -i _start 2> dpd_wasmer_err_log"
    name = 'wasmer_dump'

    def move_output(self, tgt_data_path, mv_dump_log=False, tgt_log_path=None, **kwads):
        ori_data_path = '/home/zph/DGit/wasm_projects/runtime_test/wasmer/dump_data'
        if mv_dump_log and (tgt_log_path is not None):
            shutil.move('dpd_wasmer_err_log', tgt_log_path)
        if Path(ori_data_path).exists():
            shutil.move(ori_data_path, tgt_data_path)
            return wasmer_dumped_data(tgt_data_path)


class wasmedge_dump(Wasm_impl):
    cmd_format = "/home/zph/DGit/wasm_projects/runtime_test/WasmEdge/build/tools/wasmedge/wasmedge --reactor {} _start > dpd_wasmer_err_log"
    name = 'wasmedge_dump'

    def move_output(self, tgt_data_path, mv_dump_log=False, tgt_log_path=None, **kwads):
        ori_data_path = '/home/zph/DGit/wasm_projects/runtime_test/WasmEdge/dump_data'
        if mv_dump_log and (tgt_log_path is not None):
            shutil.move('dpd_wasmer_err_log', tgt_log_path)
        if Path(ori_data_path).exists():
            shutil.move(ori_data_path, tgt_data_path)
            return wasmedge_dumped_data(tgt_data_path)

