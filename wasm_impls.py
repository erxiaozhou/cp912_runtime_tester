from pathlib import Path
from extract_dump import iwasm_classic_interp_dumped_data
from extract_dump import wasmi_dumped_data
from extract_dump import wasm3_dumped_data
from extract_dump import wasmedge_dumped_data
from extract_dump import wasmer_dumped_data
from wasm_imlp_util import Wasm_impl, check_file_mv, common_dump_behavior, single_file_dumped_data
from wasm_imlp_util import check_mv_log


class wasmi_dump(Wasm_impl):
    cmd_format = "/home/zph/DGit/wasm_projects/runtime_test/wasmi_interp/target/debug/wasmi_cli {} to_test 2> dpd_wasmi_err_log"
    name = 'wasmi_dump'

    def move_output(self,
                    tgt_store_path=None,
                    tgt_vstack_path=None,
                    mv_dump_log=False,
                    tgt_log_path=None,
                    **kwads):
        # TODO 暂定这里可以是 文件或者文件夹
        ori_store_path = '/home/zph/DGit/wasm_projects/runtime_test/wasmi_interp/dump_store'
        ori_vstack_path = '/home/zph/DGit/wasm_projects/runtime_test/wasmi_interp/dump_vstack'
        ori_log_path = 'dpd_wasmi_err_log'
        # stack_data_path = 'stack_data/stack_data_0_0'

        # if Path(stack_data_path).exists():
        #     shutil.move(stack_data_path, tgt_vstack_path)
        mv_pairs = {
            ori_store_path: tgt_store_path,
            ori_vstack_path: tgt_vstack_path
        }
        check_mv_log(ori_log_path, tgt_log_path, mv_dump_log)
        # if check_file_mv(mv_pairs, True):
        #     return wasmi_dumped_data(tgt_store_path, tgt_vstack_path)
        check_file_mv(mv_pairs, False)
        return wasmi_dumped_data(tgt_store_path, tgt_vstack_path)


class wasmi_standard(Wasm_impl):
    cmd_format = "/home/zph/DGit/wasm_projects/runtime_test/ori_wasmi/target/debug/wasmi_cli {} to_test 2> standard_wasmi_erro_log"
    name = 'wasmi_standard'

    def move_output(self, tgt_log_path=None, **kwads):
        ori_log_path = 'standard_wasmi_erro_log'
        check_mv_log(ori_log_path, tgt_log_path, True)


class iwasm_classic_interp_dump(Wasm_impl):
    # 讲道理错误什么的会用2>写进，但是这个不大一样，2>好像不会有什么有用信息
    cmd_format = "/home/zph/DGit/wasm_projects/runtime_test/iwasm_interp_classic/product-mini/platforms/linux/build/iwasm --heap-size=0 -f to_test {} > dpd_iwasm_err_log"
    name = 'iwasm_classic_interp_dump'

    def move_output(self,
                    tgt_store_path=None,
                    tgt_vstack_path=None,
                    tgt_stack_path=None,
                    mv_dump_log=False,
                    tgt_log_path=None,
                    **kwads):
        # TODO 还是有点耦合
        ori_store_path = '/home/zph/DGit/wasm_projects/runtime_test/iwasm_interp_classic/dump_store'
        ori_vstack_path = '/home/zph/DGit/wasm_projects/runtime_test/iwasm_interp_classic/dump_vstack'
        ori_log_path = 'dpd_iwasm_err_log'
        dump_extractor_class = iwasm_classic_interp_dumped_data
        return common_dump_behavior(ori_store_path, tgt_store_path,
                                    ori_vstack_path, ori_log_path,
                                    tgt_log_path, tgt_vstack_path, mv_dump_log,
                                    dump_extractor_class)


class iwasm_standard(Wasm_impl):
    cmd_format = "/home/zph/DGit/wasm_projects/runtime_test/ori_iwasm_interp_classic/product-mini/platforms/linux/build/iwasm --heap-size=0 -f to_test {} > standard_iwasm_erro_log"
    name = 'iwasm_standard'

    def move_output(self, tgt_log_path=None, **kwads):
        ori_log_path = 'standard_iwasm_erro_log'
        check_mv_log(ori_log_path, tgt_log_path, True)


class wasm3_dump(Wasm_impl):
    # 讲道理错误什么的会用2>写进，但是这个不大一样，2>好像不会有什么有用信息
    # TODO 拿不到报错信息，具体怎么写再研究吧
    cmd_format = "/home/zph/DGit/wasm_projects/runtime_test/wasm3_default/build/wasm3 --func to_test {} > dpd_wasm3_err_log"
    name = 'wasm3_dump'

    def move_output(self,
                    tgt_store_path=None,
                    tgt_vstack_path=None,
                    mv_dump_log=False,
                    tgt_log_path=None,
                    **kwads):
        ori_store_path = '/home/zph/DGit/wasm_projects/runtime_test/wasm3_default/dump_data'
        ori_vstack_path = '/home/zph/DGit/wasm_projects/runtime_test/wasm3_default/dump_vstack'
        ori_log_path = 'dpd_wasm3_err_log'
        dump_extractor_class = wasm3_dumped_data
        return common_dump_behavior(ori_store_path, tgt_store_path,
                                    ori_vstack_path, ori_log_path,
                                    tgt_log_path, tgt_vstack_path, mv_dump_log,
                                    dump_extractor_class)


class wasmer_dump(Wasm_impl):
    cmd_format = "/home/zph/DGit/wasm_projects/runtime_test/wasmer_default/target/release/wasmer run {} -i to_test 2> dpd_wasmer_err_log"
    name = 'wasmer_dump'

    def move_output(self,
                    tgt_store_path=None,
                    tgt_vstack_path=None,
                    mv_dump_log=False,
                    tgt_log_path=None,
                    **kwads):
        ori_store_path = '/home/zph/DGit/wasm_projects/runtime_test/wasmer_default/dump_data'
        ori_vstack_path = '/home/zph/DGit/wasm_projects/runtime_test/wasmer_default/dump_vstack'
        ori_log_path = 'dpd_wasmer_err_log'
        check_mv_log(ori_log_path, tgt_log_path, mv_dump_log)
        dump_extractor_class = wasmer_dumped_data
        return common_dump_behavior(ori_store_path, tgt_store_path,
                                    ori_vstack_path, ori_log_path,
                                    tgt_log_path, tgt_vstack_path, mv_dump_log,
                                    dump_extractor_class)


class wasmedge_dump(Wasm_impl):
    cmd_format = "/home/zph/DGit/wasm_projects/runtime_test/WasmEdge_disableAOT/build/tools/wasmedge/wasmedge --reactor {} to_test > dpd_wasmer_err_log"
    name = 'wasmedge_dump'

    def move_output(self,
                    tgt_store_path=None,
                    tgt_vstack_path=None,
                    mv_dump_log=False,
                    tgt_log_path=None,
                    **kwads):
        ori_store_path = '/home/zph/DGit/wasm_projects/runtime_test/WasmEdge_disableAOT/dump_data'
        ori_vstack_path = '/home/zph/DGit/wasm_projects/runtime_test/WasmEdge_disableAOT/dump_vstack'
        ori_log_path = 'dpd_wasmer_err_log'
        check_mv_log(ori_log_path, tgt_log_path, mv_dump_log)
        dump_extractor_class = wasmedge_dumped_data
        return common_dump_behavior(ori_store_path, tgt_store_path,
                                    ori_vstack_path, ori_log_path,
                                    tgt_log_path, tgt_vstack_path, mv_dump_log,
                                    dump_extractor_class)
