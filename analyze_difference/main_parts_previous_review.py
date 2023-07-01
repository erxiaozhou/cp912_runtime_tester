
from debug_util import is_executable_by_impl
from .analyze_data_util import analyzeData
from .std_exec_get_log import get_logs
from debug_util import get_log_by_impl
from debug_util import get_log_by_lastest_impl
from debug_util import is_executable_by_latest_impl


# wams3 can execute =========================================================
def prule1():
    # wasm3，export memory OOB.和 main_parts.rule13差不多，不急着上报。上报后可能也不会计入统计
    # TODO 未上报
    # * 不打算报了
    key = '((WAVM_default, Error loading WebAssembly binary file: Module was invalid: invalid index: exportIt.index must be less than module.memories.size() (exportIt.index=26, module.memories.size()=1)), (WasmEdge_disableAOT_newer, unknown memory), (iwasm_classic_interp_dump, unknown memory), (iwasm_fast_interp_dump, unknown memory), (wasmer_default_dump, unknown memory), (wasmi_interp, unknown memory))'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/1.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    analysis_base.print_first_tc_log(use_lastest=True)

def prule2():
    # wasm3，export table OOB.和 上面那个差不多，不急着上报。上报后可能也不会计入统计
    # TODO 未上报，这个的优先级比上面的高一点
    # * 上报
    key = '((WAVM_default, Error loading WebAssembly binary file: Module was invalid: invalid index: exportIt.index must be less than module.tables.size() (exportIt.index=0, module.tables.size()=0)), (WasmEdge_disableAOT_newer, unknown table), (iwasm_classic_interp_dump, unknown table), (iwasm_fast_interp_dump, unknown table), (wasmer_default_dump, table OOB), (wasmi_interp, table OOB))'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/1.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    analysis_base.print_first_tc_log(use_lastest=True)

def prule3():
    # wasm3，感觉还是memory OOB的问题，，
    # TODO 未上报，但不打算上报，因为觉得root cause和前面的是重复的
    key = '((WAVM_default, Error loading WebAssembly binary file: Module was malformed: invalid initializer expression opcode), (WasmEdge_disableAOT_newer, unknown memory), (iwasm_classic_interp_dump, unknown memory), (iwasm_fast_interp_dump, unknown memory), (wasmer_default_dump, unknown memory), (wasmi_interp, unknown memory))'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/1.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    analysis_base.print_first_tc_log(use_lastest=True)

# ((iwasm_classic_interp_dump, (CannotExecute,)), (iwasm_fast_interp_dump, (CannotExecute,)), (wasm3_dump, (CannotExecute,)), (wasmi_interp, (CannotExecute,))) ==========================================
def prule4():
    # * 被修了
    key = '((iwasm_classic_interp_dump, WASM module load failed: invalid section id), (iwasm_fast_interp_dump, WASM module load failed: invalid section id))'
    # 下面的path本来应当是2，但是2里面有simd什么的，iwasm还是不支持，所以就用3
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/3.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    analysis_base.print_first_tc_log(use_lastest=True)

def prule5():
    # * iwasm bug被修了.但wasm3还在报错
    # TODO 这个报的有点奇怪。转成Wat再转回wasm后的wasm和原tc是不同的
    key = '((iwasm_classic_interp_dump, unknown memory), (iwasm_fast_interp_dump, unknown memory), (wasm3_dump, Error: [Fatal] repl_load: restricted opcodeError: restricted opcode))'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/9.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    analysis_base.print_first_tc_log(use_lastest=True)


# ((iwasm_classic_interp_dump, (CanExecute,)), (iwasm_fast_interp_dump, (CanExecute,))
# * "((WAVM_default, <function or section size mismatch>), (WasmEdge_disableAOT_newer, <function or section size mismatch>), (wasm3_dump, <function or section size mismatch>), (wasmer_default_dump, <function or section size mismatch>), (wasmi_interp, <function or section size mismatch>))  
# TODO 这个应该很早就上报过了，看看有没有测出来
# some log没有测出来



def prule6():
    # ! 研究下为什么可能没触发出来
    # * 已上报
    # TODO 但新版好像没测出来
    key = '((WAVM_default, <function or section size mismatch>), (WasmEdge_disableAOT_newer, <function or section size mismatch>), (wasm3_dump, <function or section size mismatch>), (wasmer_default_dump, <function or section size mismatch>), (wasmi_interp, <function or section size mismatch>))'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/10.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    analysis_base.print_first_tc_log(use_lastest=True)


# ((wasmi_interp, (CanExecute,)),)
def prule7():
    # 也是wrong alignment
    key = '((WAVM_default, <masked because of <function or section size mismatch>>), (WasmEdge_disableAOT_newer, <masked because of <function or section size mismatch>>), (iwasm_classic_interp_dump, <masked because of <function or section size mismatch>>), (iwasm_fast_interp_dump, <masked because of <function or section size mismatch>>), (wasm3_dump, <masked because of <function or section size mismatch>>), (wasmer_default_dump, <masked because of <function or section size mismatch>>))'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/15.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    analysis_base.print_first_tc_log(use_lastest=True)

# ((WasmEdge_disableAOT_newer, (has_timeout,)),)
def prule8():
    # local太多
    key = '((WAVM_default, Error loading WebAssembly binary file: Module was malformed: invalid initializer expression opcode),)'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/16.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    analysis_base.print_first_tc_log(use_lastest=True)


# ((WasmEdge_disableAOT_newer, (CannotExecute,)), (iwasm_classic_interp_dump, (CannotExecute,)), (iwasm_fast_interp_dump, (CannotExecute,)), (wasm3_dump, (CannotExecute,)), (wasmi_interp, (CannotExecute,)))
def prule9():
    # TODO 。。。。只能查一查了
    # TODO 这个不是很好查,可能和store alignment有关
    key = '((WasmEdge_disableAOT_newer, illegal/unknown opcode),)'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/19.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'

    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    analysis_base.print_first_tc_log(use_lastest=True)


# ((wasm3_dump, (CannotExecute,)),)
def prule10():
    # * 隔壁里的一样，wasm3 bug被修了
    key = '((wasm3_dump, Aborted),)'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/20.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'

    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    analysis_base.print_first_tc_log(use_lastest=True)


# ((iwasm_classic_interp_dump, (CanExecute,)), (iwasm_fast_interp_dump, (CanExecute,)), (wasm3_dump, (CanExecute,)))
def prule11():
    # 0xc5， wasm3又恰好漏掉了。
    # 总的来说是两个bug的组合，不用理
    key = '((WAVM_default, illegal/unknown opcode), (WasmEdge_disableAOT_newer, illegal/unknown opcode), (wasmer_default_dump, illegal/unknown opcode), (wasmi_interp, illegal/unknown opcode))'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/24.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'

    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    analysis_base.print_first_tc_log(use_lastest=True)
    print(analysis_base.illegal_wasmer_opcodes())


# ((WAVM_default, (has_timeout,)), (WasmEdge_disableAOT_newer, (has_timeout,)), (wasm3_dump, (CanExecute,)))
def prule12():
    # 重新运行就没有timeout了
    key = '((iwasm_classic_interp_dump, type mismatch), (iwasm_fast_interp_dump, type mismatch), (wasmer_default_dump, type mismatch), (wasmi_interp, type mismatch))'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/25.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'

    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_logs()

# ((iwasm_classic_interp_dump, (has_timeout,)), (iwasm_fast_interp_dump, (has_timeout,)))
def prule13():
    # 重新运行就没有timeout了
    key = '((WasmEdge_disableAOT_newer, illegal/unknown type),)'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/26.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'

    analysis_base = analyzeData(path, key, tcs_base_dir)
    runtimes = ['iwasm_classic_interp_dump', 'iwasm_fast_interp_dump']
    analysis_base.print_logs(keys=runtimes)


# TODO 记得上报 wasmer现在应该还没修。还有注意下unreachable的位置
#     "/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/27.json<-->((WasmEdge_disableAOT_newer, (CannotExecute,)), (iwasm_classic_interp_dump, (CannotExecute,)), (iwasm_fast_interp_dump, (CannotExecute,)), (wasm3_dump, (CannotExecute,)))": [
        # "((WasmEdge_disableAOT_newer, <wrong alignment>), (iwasm_classic_interp_dump, <wrong alignment>), (iwasm_fast_interp_dump, <wrong alignment>), (wasm3_dump, unreachable))"
    # ],



def prule14():
    #  TODO 确实在屏幕上输出timeout了，目前的实捕捉不到屏幕上的timeout
    key = '()'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/29.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    runtimes = ['iwasm_classic_interp_dump', 'iwasm_fast_interp_dump', 'WasmEdge_disableAOT_newer']
    analysis_base.print_logs(keys=runtimes)


def prule15():
    # 重新运行就没有timeout了
    key = '((WasmEdge_disableAOT_newer, memory OOB), (wasm3_dump, illegal/unknown opcode), (wasmer_default_dump, memory OOB))'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/38.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    runtimes = ['iwasm_classic_interp_dump', 'iwasm_fast_interp_dump', 'WAVM_default']
    analysis_base.print_logs(keys=runtimes)


def prule15():
    # 重新运行就没有timeout了
    key = '((iwasm_classic_interp_dump, <masked because of <function or section size mismatch>>), (iwasm_fast_interp_dump, <masked because of <function or section size mismatch>>), (wasm3_dump, <masked because of <function or section size mismatch>>), (wasmer_default_dump, <masked because of <function or section size mismatch>>))'
    path = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/log_category_base/only_highlight_log_category/40.json'
    tcs_base_dir = '/media/hdd_xj1/cp910_data/existing_diff_tcs_result_0331/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    runtimes = ['WasmEdge_disableAOT_newer', 'wasmi_interp', 'WAVM_default']
    analysis_base.print_logs(keys=runtimes)
