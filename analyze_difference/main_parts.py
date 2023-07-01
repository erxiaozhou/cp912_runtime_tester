from debug_util import is_executable_by_impl
from .analyze_data_util import analyzeData
from .std_exec_get_log import get_logs
from debug_util import get_log_by_impl
from debug_util import get_log_by_lastest_impl
from debug_util import is_executable_by_latest_impl


# ======================================================
# # ((iwasm_classic_interp_dump, (CannotExecute,)), (iwasm_fast_interp_dump, (CannotExecute,)), (wasm3_dump, (CannotExecute,)), (wasmi_interp, (CannotExecute,)))
# TODO 
def rule1():
    # not bug: WASM module load failed: unsupported opcode fc 0a
    # fc 0a: memory.copy
    # {'wasmer_default_dump': [''], 'wasmi_interp': ['Error: failed to parse and validate Wasm module /media/ssd_wd1/cp910_data/main_testing_v125_250_9811/diff_tcs/memory.copy_1743_4_16793367358983462.wasm: bulk memory support is not enabled (at offset 0xf0)\n'], 'iwasm_classic_interp_dump': ['WASM module load failed: unsupported opcode fc 0a\n'], 'iwasm_fast_interp_dump': ['WASM module load failed: fast interpreter offset overflow\n'], 'wasm3_dump': ['Error: compiling function overran its stack height limit\n'], 'WasmEdge_disableAOT_newer': [''], 'WAVM_default': ['']}
    key = '((iwasm_classic_interp_dump, illegal/unknown opcode),)'
    path = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811/only_execution_log_category/log_category_only_highlight/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_logs()


# TODO 启示： SIMD unsupport + illegal type可以滤掉不分析
def rule2():
    # not bug: WASM module load failed: unsupported opcode fc 0a
    # fc 0a: memory.copy
    # {'wasmer_default_dump': [''], 'wasmi_interp': ['Error: failed to parse and validate Wasm module /media/ssd_wd1/cp910_data/main_testing_v125_250_9811/diff_tcs/v128.load16_splat_106_1_16793451806163344.wasm: SIMD support is not enabled (at offset 0x1e)\n'], 'iwasm_classic_interp_dump': ['WASM module load failed: unknown value type\n'], 'iwasm_fast_interp_dump': ['WASM module load failed: unknown value type\n'], 'wasm3_dump': ['Error: [Fatal] repl_load: unknown value_type\nError: unknown value_type\n'], 'WasmEdge_disableAOT_newer': ['0\n'], 'WAVM_default': ['']}
    key = '((iwasm_classic_interp_dump, illegal/unknown type), (iwasm_fast_interp_dump, illegal/unknown type), (wasm3_dump, illegal/unknown type))'
    path = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811/only_execution_log_category/log_category_only_highlight/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()


def rule3():
    # ref.func 0在iwasm里会引发报错
    # * 新bug，确认，已上报
    # {'wasmer_default_dump': [''], 'wasmi_interp': ['Error: failed to parse and validate Wasm module /media/ssd_wd1/cp910_data/main_testing_v125_250_9811/diff_tcs/table.fill_266_2_16793527045334868.wasm: reference types support is not enabled (at offset 0xe8)\n'], 'iwasm_classic_interp_dump': ['WASM module load failed: undeclared function reference\n'], 'iwasm_fast_interp_dump': ['WASM module load failed: undeclared function reference\n'], 'wasm3_dump': ['Error: compiling function overran its stack height limit\n'], 'WasmEdge_disableAOT_newer': [''], 'WAVM_default': ['']}
    key = '((iwasm_classic_interp_dump, undeclared function reference), (iwasm_fast_interp_dump, undeclared function reference))'
    path = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811/only_execution_log_category/log_category_only_highlight/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_logs(use_lastest=True)

def rule4():
    # no bug SIMD + illegal type
    # {'wasmer_default_dump': [''], 'wasmi_interp': ['Error: failed to parse and validate Wasm module /media/ssd_wd1/cp910_data/main_testing_v125_250_9811/diff_tcs/i32.shr_s_101_1_16793343842004454.wasm: SIMD support is not enabled (at offset 0x33)\n'], 'iwasm_classic_interp_dump': ['WASM module load failed: v128 value type requires simd feature\n'], 'iwasm_fast_interp_dump': ['WASM module load failed: v128 value type requires simd feature\n'], 'wasm3_dump': ['Error: unknown value_type\n'], 'WasmEdge_disableAOT_newer': ['1\n'], 'WAVM_default': ['']}
    key = '((wasm3_dump, illegal/unknown type),)'
    path = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811/only_execution_log_category/log_category_only_highlight/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()


def rule5():
    # nobug: illegal op 都是fd
    #
    key = '((iwasm_classic_interp_dump, illegal/unknown opcode), (iwasm_fast_interp_dump, illegal/unknown opcode), (wasm3_dump, illegal/unknown opcode))'
    path = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811/only_execution_log_category/log_category_only_highlight/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    print(analysis_base.illegal_iwasm_opcodes('iwasm_fast_interp_dump'))
    print(analysis_base.illegal_iwasm_opcodes('iwasm_classic_interp_dump'))

def rule6():
    # * known bug: local number
    key = '((iwasm_classic_interp_dump, invalid local count), (iwasm_fast_interp_dump, invalid local count), (wasm3_dump, Aborted))'
    path = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811/only_execution_log_category/log_category_only_highlight/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_250_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()


# wams3 can execute =========================================================
def rule7():
    # not bug / wasm3
    # {'fc 0a', 'fc 0b'}这两个指令对应 memory.copy memory.fill
    key = '((WAVM_default, zero byte expected), (WasmEdge_disableAOT_newer, zero byte expected), (iwasm_classic_interp_dump, unsupported opcode fc), (iwasm_fast_interp_dump, unsupported opcode fc))'
    path = 'useful_results/some_logs/only_highlight_log_category/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    print(analysis_base.illegal_iwasm_opcodes('iwasm_fast_interp_dump'))  # {'fc 0a', 'fc 0b'}

def rule8():
    # wrong alignment
    # * 已上报bug ; wasm3 bug; *应该在第一轮报过了
    key = '((WAVM_default, <wrong alignment>), (WasmEdge_disableAOT_newer, <wrong alignment>), (iwasm_classic_interp_dump, <wrong alignment>), (iwasm_fast_interp_dump, <wrong alignment>), (wasmi_interp, <wrong alignment>))'
    path = 'useful_results/some_logs/only_highlight_log_category/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()

def rule9():
    # wrong local type 0x40
    # * 新上报 ; wasm3 bug
    key = '((WAVM_default, illegal/unknown type), (WasmEdge_disableAOT_newer, illegal/unknown type), (iwasm_classic_interp_dump, illegal/unknown type), (iwasm_fast_interp_dump, illegal/unknown type), (wasmer_default_dump, illegal/unknown type), (wasmi_interp, illegal/unknown type))'
    path = 'useful_results/some_logs/only_highlight_log_category/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()

    illegal_types = analysis_base.illegal_iwasm_local_types()
    print(illegal_types)  # {'local type 0x40'}

def rule10():
    # * 新上报 ; wasm3 bug
    key = '((WAVM_default, zero byte expected), (WasmEdge_disableAOT_newer, zero byte expected), (iwasm_classic_interp_dump, zero byte expected), (iwasm_fast_interp_dump, zero byte expected))'
    path = 'useful_results/some_logs/only_highlight_log_category/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log(process=True)
    # {'wasmer_default_dump': {'error: failed to run`│   1: module instantiation failed (compiler: cranelift)╰─▶ 2: Validation error: multi-memory not enabled '}, 'wasmi_interp': {'Error: failed to parse and validate Wasm module: multi-memory not enabled: zero byte expected '}, 'iwasm_classic_interp_dump': {'WASM module load failed: zero byte expected'}, 'iwasm_fast_interp_dump': {'WASM module load failed: zero byte expected'}, 'wasm3_dump': {''}, 'WasmEdge_disableAOT_newer': {' [error] loading failed: zero byte expected, [error]      [error]     At AST node: instruction [error]     At AST node: expression [error]     At AST node: code segment [error]     At AST node: code section [error]     At AST node: module [error]     File name:"'}, 'WAVM_default': {'Error loading WebAssembly binary file: Module was malformed: memory index reserved byte must be zero: loaded 32 but was expecting 0'}}

def rule11():
    # bug / wasm3
    # * 都是仅在debug模式下报错，只上报了ef
    key = '((WAVM_default, illegal/unknown opcode), (WasmEdge_disableAOT_newer, illegal/unknown opcode), (iwasm_classic_interp_dump, illegal/unknown opcode), (iwasm_fast_interp_dump, illegal/unknown opcode), (wasmer_default_dump, illegal/unknown opcode), (wasmi_interp, illegal/unknown opcode))'
    path = 'useful_results/some_logs/only_highlight_log_category/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    opcodes = analysis_base.illegal_iwasm_opcodes('iwasm_fast_interp_dump')
    print(opcodes)  #  {'c7', 'f0', 'e1', 'ef', 'dd', 'ec'}
    print(get_logs(analysis_base.tc_paths, 'wasm3_dump', process=False, use_lastest=True))

def rule12():
    # bug / wasm3
    # too large int (illegal int)
    # * 新上报 ; wasm3 bug
    key = '((WAVM_default, illegal int encoding), (WasmEdge_disableAOT_newer, illegal int encoding), (iwasm_classic_interp_dump, illegal int encoding), (iwasm_fast_interp_dump, illegal int encoding), (wasmer_default_dump, illegal int encoding), (wasmi_interp, illegal int encoding))'
    path = 'useful_results/some_logs/only_highlight_log_category/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()

def rule13():
    # bug / wasm3
    # unkniwn memory
    # * 新上报 ; wasm3 bug
    key = '((WAVM_default, memory OOB), (WasmEdge_disableAOT_newer, unknown memory), (iwasm_classic_interp_dump, unknown memory), (iwasm_fast_interp_dump, unknown memory), (wasmer_default_dump, unknown memory), (wasmi_interp, unknown memory))'
    path = 'useful_results/some_logs/only_highlight_log_category/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()


# ((WAVM_default, type mismatch), (WasmEdge_disableAOT_newer, type mismatch), (iwasm_classic_interp_dump, type mismatch), (iwasm_fast_interp_dump, type mismatch), (wasmer_default_dump, type mismatch), (wasmi_interp, type mismatch))
# * type mismatch算很典型了，第一批报的


# * function / section mismatch 典型
def rule13_2():
    # * new bug / wasm3
    # section mismatch
    # * 新上报  ; wasm3 bug
    key = '((WAVM_default, <function or section size mismatch>), (WasmEdge_disableAOT_newer, <function or section size mismatch>), (iwasm_classic_interp_dump, <function or section size mismatch>), (iwasm_fast_interp_dump, <function or section size mismatch>), (wasmer_default_dump, <function or section size mismatch>), (wasmi_interp, <function or section size mismatch>))'
    path = 'useful_results/some_logs/only_highlight_log_category/1.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    
    analysis_base.print_first_tc_log()
    print(analysis_base.first_tc_path)

# ==================================================================
# ((iwasm_classic_interp_dump, (CannotExecute,)), (iwasm_fast_interp_dump, (CannotExecute,)), (wasmi_interp, (CannotExecute,))
def rule14():
    # no bug ; 真的不支持
    # TODO {'fc 0a', 'fc 0b'}
    # {'fc 0a', 'fc 0b'}这两个指令对应 memory.copy memory.fill
    # not bug
    key = '((iwasm_classic_interp_dump, unsupported opcode fc), (iwasm_fast_interp_dump, unsupported opcode fc))'
    path = 'useful_results/some_logs/only_highlight_log_category/4.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    opcodes = analysis_base.illegal_iwasm_opcodes('iwasm_fast_interp_dump')
    print(opcodes)
# =========================================================
# * 下面这个也典型，报了
# ((iwasm_classic_interp_dump, invalid local count), (iwasm_fast_interp_dump, invalid local count))
# 
# =========================================================
# * 下面这个也典型

# "only_highlight_log_category/5.json<-->((WasmEdge_disableAOT_newer, (has_timeout,)),)": [
#     "((WAVM_default, unknown function), (wasm3_dump, wasm3 stack overflow), (wasmer_default_dump, call stack exhausted), (wasmi_interp, call stack exhausted))",
#     "()",
#     "((WAVM_default, unknown function), (wasmer_default_dump, call stack exhausted))"
# ],


def rule15():
    # TODO 应该没上报。。报了吧，，？ wasmedge timeout
    keys = [
        '((WAVM_default, unknown function), (wasm3_dump, wasm3 stack overflow), (wasmer_default_dump, call stack exhausted), (wasmi_interp, call stack exhausted))',
        '((WAVM_default, unknown function), (wasmer_default_dump, call stack exhausted))'
    ]
    path = 'useful_results/some_logs/only_highlight_log_category/5.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, keys, tcs_base_dir)
    analysis_base.check_call_0()
    analysis_base.print_first_tc_log()

# =========================================================
# * 下面这个也典型
# ((WasmEdge_disableAOT_newer, (CanExecute,)),)
# ((WAVM_default, <function or section size mismatch>), (iwasm_classic_interp_dump, <function or section size mismatch>), (iwasm_fast_interp_dump, <function or section size mismatch>), (wasm3_dump, <function or section size mismatch>), (wasmer_default_dump, <function or section size mismatch>), (wasmi_interp, <function or section size mismatch>))"


def rule16():
    # wasmedge的{'0xd6 ', '0xcb ', '0xda ', '0xcd ', '0xd5 ', '0xd7 ', '0xcc ', '0xdf ', '0xce '} opcode能运行，，
    # * 决定不报了，认为这个是secntion  size的问题
    # * 好像被修复了。。。。。。也可能是section size造成的，新版上会报loading failed: unexpected content after last section
    key = '((WAVM_default, illegal/unknown opcode), (wasm3_dump, illegal/unknown opcode), (wasmer_default_dump, illegal/unknown opcode))'
    path = 'useful_results/some_logs/only_highlight_log_category/6.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    opcodes = analysis_base.illegal_wasmer_opcodes()
    print(opcodes)
    print(get_logs(analysis_base.tc_paths, 'WasmEdge_disableAOT_newer', process=False, use_lastest=True))



def rule17():
    # wasmedge的{'0xdb ', '0xd6 ', '0xc8 ', '0xcf ', '0xc6 ', '0xdf ', '0xcd ', '0xcc ', '0xcb ', '0xde ', '0xd3 ', '0xce ', '0xd8 ', '0xd7 '} opcode能运行，，
    # * 同上
    key = '((WAVM_default, illegal/unknown opcode), (wasmer_default_dump, illegal/unknown opcode))'
    path = 'useful_results/some_logs/only_highlight_log_category/6.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    opcodes = analysis_base.illegal_wasmer_opcodes()
    print(opcodes)
    print(len(analysis_base.tc_paths))
    # for content in get_logs(analysis_base.tc_paths, 'wasmer_default_dump', process=True, use_lastest=True):
    #     print(content)
    #     print('-'*30)
    print(get_logs(analysis_base.tc_paths, 'wasmer_default_dump', process=True, use_lastest=True))
    for p in analysis_base.tc_paths:
        print(p, get_log_by_lastest_impl('WasmEdge_disableAOT_newer', p))
        if is_executable_by_latest_impl('WasmEdge_disableAOT_newer', p):
            print(p, get_log_by_lastest_impl('WasmEdge_disableAOT_newer', p))
            print('-'*30)


# =========================================================
# * 下面这个典型
# ((WAVM_default, (CanExecute,)),)": 
# "((WasmEdge_disableAOT_newer, <wrong alignment>), (wasmer_default_dump, <wrong alignment>))",


def rule18():
    # wavm的{'0xe5 ', '0xf5 ', '0xec ', '0xf1 ', '0xe4 ', '0xed '}opcode能运行，，
    # TODO 看wasmedge实现
    # * 报了ec, 
    key = '((WasmEdge_disableAOT_newer, illegal/unknown opcode), (wasmer_default_dump, illegal/unknown opcode))'
    path = 'useful_results/some_logs/only_highlight_log_category/7.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    opcodes = analysis_base.illegal_wasmer_opcodes()
    print(opcodes)
    for p in analysis_base.tc_paths:
        print(p, get_log_by_lastest_impl('WasmEdge_disableAOT_newer', p))


def rule19():
    # wavm 的bug，
    '''
    {'Unknown 0xfd subopcode: 0x1c87 ', 'Unknown 0xfd subopcode: 0x1d39 ', 'Unknown 0xfd subopcode: 0x2891 ', 'Unknown 0xfd subopcode: 0x83a ', 'Unknown 0xfd subopcode: 0x2c8e ', 'Unknown 0xfd subopcode: 0x29e4 ', 'Unknown 0xfd subopcode: 0x15bc ', 'Unknown 0xfd subopcode: 0x2c82 ', 'Unknown 0xfd subopcode: 0x24e6 ', 'Unknown 0xfd subopcode: 0x2935 ', 'Unknown 0xfd subopcode: 0x536 ', 'Unknown 0xfd subopcode: 0x61f4 ', 'Unknown 0xfd subopcode: 0x3d70 ', 'Unknown 0xfd subopcode: 0x158e ', 'Unknown 0xfd subopcode: 0x3d95 ', 'Unknown 0xfd subopcode: 0xcd1 ', 'Unknown 0xfd subopcode: 0x19da ', 'Unknown 0xfd subopcode: 0x3e0dd1 ', 'Unknown 0xfd subopcode: 0x15ce ', 'Unknown 0xfd subopcode: 0x6038 ', 'Unknown 0xfd subopcode: 0x65cd ', 'Unknown 0xfd subopcode: 0x6c43 ', 'Unknown 0xfd subopcode: 0x158b ', 'Unknown 0xfd subopcode: 0x1dcd ', 'Unknown 0xfd subopcode: 0x3729f5 ', 'Unknown 0xfd subopcode: 0x259b ', 'Unknown 0xfd subopcode: 0x7924 ', 'Unknown 0xfd subopcode: 0x70ba ', 'Unknown 0xfd subopcode: 0x1d79 ', 'Unknown 0xfd subopcode: 0x11f5 ', 'Unknown 0xfd subopcode: 0x74d7 ', 'Unknown 0xfd subopcode: 0x508e ', 'Unknown 0xfd subopcode: 0x6c70 ', 'Unknown 0xfd subopcode: 0x48ae ', 'Unknown 0xfd subopcode: 0x15ab ', 'Unknown 0xfd subopcode: 0x59b9 ', 'Unknown 0xfd subopcode: 0x439 ', 'Unknown 0xfd subopcode: 0x4ad ', 'Unknown 0xfd subopcode: 0x499b ', 'Unknown 0xfd subopcode: 0x1cd5 ', 'Unknown 0xfd subopcode: 0x2d73 ', 'Unknown 0xfd subopcode: 0x1c82 ', 'Unknown 0xfd subopcode: 0x404e ', 'Unknown 0xfd subopcode: 0xc31 ', 'Unknown 0xfd subopcode: 0xcb1 ', 'Unknown 0xfd subopcode: 0x11d1 ', 'Unknown 0xfd subopcode: 0x5cb6 ', 'Unknown 0xfd subopcode: 0x58eb ', 'Unknown 0xfd subopcode: 0x4dab ', 'Unknown 0xfd subopcode: 0xddf ', 'Unknown 0xfd subopcode: 0x431 ', 'Unknown 0xfd subopcode: 0x119c ', 'Unknown 0xfd subopcode: 0x42e ', 'Unknown 0xfd subopcode: 0x11dd ', 'Unknown 0xfd subopcode: 0x1d8b ', 'Unknown 0xfd subopcode: 0x2151 ', 'Unknown 0xfd subopcode: 0x20d7 ', 'Unknown 0xfd subopcode: 0x6c82 ', 'Unknown 0xfd subopcode: 0x392d ', 'Unknown 0xfd subopcode: 0x28f0 ', 'Unknown 0xfd subopcode: 0x28de ', 'Unknown 0xfd subopcode: 0x1cdb ', 'Unknown 0xfd subopcode: 0x2571 ', 'Unknown 0xfd subopcode: 0x200e ', 'Unknown 0xfd subopcode: 0x88e ', 'Unknown 0xfd subopcode: 0x3cb7 ', 'Unknown 0xfd subopcode: 0xd31 ', 'Unknown 0xfd subopcode: 0x79ce ', 'Unknown 0xfd subopcode: 0x1c51 ', 'Unknown 0xfd subopcode: 0x4993 ', 'Unknown 0xfd subopcode: 0x2c51 ', 'Unknown 0xfd subopcode: 0x831 ', 'Unknown 0xfd subopcode: 0x872 ', 'Unknown 0xfd subopcode: 0x44d5 ', 'Unknown 0xfd subopcode: 0x1cf9 ', 'Unknown 0xfd subopcode: 0x49d6 ', 'Unknown 0xfd subopcode: 0x49bc ', 'Unknown 0xfd subopcode: 0x7cde ', 'Unknown 0xfd subopcode: 0x10f4 ', 'Unknown 0xfd subopcode: 0xd91 ', 'Unknown 0xfd subopcode: 0x3591 ', 'Unknown 0xfd subopcode: 0x15e9 ', 'Unknown 0xfd subopcode: 0x1de8 ', 'Unknown 0xfd subopcode: 0x14b1 ', 'Unknown 0xfd subopcode: 0x1185 ', 'Unknown 0xfd subopcode: 0x16c8ef ', 'Unknown 0xfd subopcode: 0x55ab ', 'Unknown 0xfd subopcode: 0x58fd ', 'Unknown 0xfd subopcode: 0x21cc ', 'Unknown 0xfd subopcode: 0x21f5 ', 'Unknown 0xfd subopcode: 0x2cd1 ', 'Unknown 0xfd subopcode: 0x4e3099b ', 'Unknown 0xfd subopcode: 0x1c78 ', 'Unknown 0xfd subopcode: 0x5835 ', 'Unknown 0xfd subopcode: 0x3dda ', 'Unknown 0xfd subopcode: 0x349f ', 'Unknown 0xfd subopcode: 0x1c50 ', 'Unknown 0xfd subopcode: 0x1c76 ', 'Unknown 0xfd subopcode: 0x21e6 ', 'Unknown 0xfd subopcode: 0x15fe ', 'Unknown 0xfd subopcode: 0x78ac ', 'Unknown 0xfd subopcode: 0x11ab ', 'Unknown 0xfd subopcode: 0x6877 ', 'Unknown 0xfd subopcode: 0xd1c ', 'Unknown 0xfd subopcode: 0x553c ', 'Unknown 0xfd subopcode: 0x35ba ', 'Unknown 0xfd subopcode: 0x11dc ', 'Unknown 0xfd subopcode: 0x1ceb ', 'Unknown 0xfd subopcode: 0x2149 ', 'Unknown 0xfd subopcode: 0x14ba ', 'Unknown 0xfd subopcode: 0x109f ', 'Unknown 0xfd subopcode: 0x19e1 ', 'Unknown 0xfd subopcode: 0x1de7 ', 'Unknown 0xfd subopcode: 0x608c ', 'Unknown 0xfd subopcode: 0x3490 ', 'Unknown 0xfd subopcode: 0x1573 ', 'Unknown 0xfd subopcode: 0x7c71 ', 'Unknown 0xfd subopcode: 0x39de ', 'Unknown 0xfd subopcode: 0x35b8 ', 'Unknown 0xfd subopcode: 0x3071 ', 'Unknown 0xfd subopcode: 0x1198 ', 'Unknown 0xfd subopcode: 0x6d96 ', 'Unknown 0xfd subopcode: 0x75b7 ', 'Unknown 0xfd subopcode: 0x4dd1 ', 'Unknown 0xfd subopcode: 0x3b3d98 ', 'Unknown 0xfd subopcode: 0x2839 ', 'Unknown 0xfd subopcode: 0x3586 ', 'Unknown 0xfd subopcode: 0x3cb9f2 ', 'Unknown 0xfd subopcode: 0x40f2 ', 'Unknown 0xfd subopcode: 0x38f5 ', 'Unknown 0xfd subopcode: 0x1051 ', 'Unknown 0xfd subopcode: 0x2def ', 'Unknown 0xfd subopcode: 0x149e ', 'Unknown 0xfd subopcode: 0x38b5 ', 'Unknown 0xfd subopcode: 0x49e9 ', 'Unknown 0xfd subopcode: 0x2cf7 ', 'Unknown 0xfd subopcode: 0x1173 ', 'Unknown 0xfd subopcode: 0x5435 ', 'Unknown 0xfd subopcode: 0x1c4cb ', 'Unknown 0xfd subopcode: 0x7948 ', 'Unknown 0xfd subopcode: 0x1c4e ', 'Unknown 0xfd subopcode: 0x588d ', 'Unknown 0xfd subopcode: 0x3839 ', 'Unknown 0xfd subopcode: 0x1448 ', 'Unknown 0xfd subopcode: 0x2c9d ', 'Unknown 0xfd subopcode: 0x44cb ', 'Unknown 0xfd subopcode: 0x7092 ', 'Unknown 0xfd subopcode: 0x148f ', 'Unknown 0xfd subopcode: 0x3934 ', 'Unknown 0xfd subopcode: 0x5d95 ', 'Unknown 0xfd subopcode: 0x75ce ', 'Unknown 0xfd subopcode: 0x1d65 ', 'Unknown 0xfd subopcode: 0x4823 ', 'Unknown 0xfd subopcode: 0x3d93 ', 'Unknown 0xfd subopcode: 0x1020 ', 'Unknown 0xfd subopcode: 0x21cb ', 'Unknown 0xfd subopcode: 0x1190 ', 'Unknown 0xfd subopcode: 0x6995 ', 'Unknown 0xfd subopcode: 0x4571 ', 'Unknown 0xfd subopcode: 0x2967 ', 'Unknown 0xfd subopcode: 0x69f5 ', 'Unknown 0xfd subopcode: 0x50ce ', 'Unknown 0xfd subopcode: 0x1dbc ', 'Unknown 0xfd subopcode: 0x1df4 ', 'Unknown 0xfd subopcode: 0x5c9e ', 'Unknown 0xfd subopcode: 0xdad ', 'Unknown 0xfd subopcode: 0x1c46 ', 'Unknown 0xfd subopcode: 0xc3e ', 'Unknown 0xfd subopcode: 0x34cb ', 'Unknown 0xfd subopcode: 0x742d ', 'Unknown 0xfd subopcode: 0x11d9 ', 'Unknown 0xfd subopcode: 0x416c ', 'Unknown 0xfd subopcode: 0xd72 ', 'Unknown 0xfd subopcode: 0x7439 ', 'Unknown 0xfd subopcode: 0x4e1 ', 'Unknown 0xfd subopcode: 0x4490 ', 'Unknown 0xfd subopcode: 0x6de8 ', 'Unknown 0xfd subopcode: 0x19bf ', 'Unknown 0xfd subopcode: 0x2cd7 ', 'Unknown 0xfd subopcode: 0x2db6 ', 'Unknown 0xfd subopcode: 0x7999 ', 'Unknown 0xfd subopcode: 0x2ccb ', 'Unknown 0xfd subopcode: 0x7944 ', 'Unknown 0xfd subopcode: 0x2551 ', 'Unknown 0xfd subopcode: 0x59f9 ', 'Unknown 0xfd subopcode: 0x1d2c ', 'Unknown 0xfd subopcode: 0x492e ', 'Unknown 0xfd subopcode: 0x199c ', 'Unknown 0xfd subopcode: 0x243f ', 'Unknown 0xfd subopcode: 0x31b6 ', 'Unknown 0xfd subopcode: 0x2dd1 ', 'Unknown 0xfd subopcode: 0x7c99 ', 'Unknown 0xfd subopcode: 0x5d7b ', 'Unknown 0xfd subopcode: 0x793c ', 'Unknown 0xfd subopcode: 0x7893 ', 'Unknown 0xfd subopcode: 0x5cbd ', 'Unknown 0xfd subopcode: 0x6993 ', 'Unknown 0xfd subopcode: 0x10d1 ', 'Unknown 0xfd subopcode: 0x9c99b ', 'Unknown 0xfd subopcode: 0x991 ', 'Unknown 0xfd subopcode: 0x5e4 ', 'Unknown 0xfd subopcode: 0x997 ', 'Unknown 0xfd subopcode: 0x1088 ', 'Unknown 0xfd subopcode: 0x1995 ', 'Unknown 0xfd subopcode: 0x1465 ', 'Unknown 0xfd subopcode: 0x6531 ', 'Unknown 0xfd subopcode: 0x26dc51 ', 'Unknown 0xfd subopcode: 0x11cd ', 'Unknown 0xfd subopcode: 0x3171 ', 'Unknown 0xfd subopcode: 0x799e ', 'Unknown 0xfd subopcode: 0x5cd8 ', 'Unknown 0xfd subopcode: 0x3572 ', 'Unknown 0xfd subopcode: 0x146b ', 'Unknown 0xfd subopcode: 0x2dea ', 'Unknown 0xfd subopcode: 0xd0e ', 'Unknown 0xfd subopcode: 0xc82 ', 'Unknown 0xfd subopcode: 0x2485 ', 'Unknown 0xfd subopcode: 0x7d98 ', 'Unknown 0xfd subopcode: 0x58ad ', 'Unknown 0xfd subopcode: 0x313d ', 'Unknown 0xfd subopcode: 0x3ddd ', 'Unknown 0xfd subopcode: 0x399d ', 'Unknown 0xfd subopcode: 0x28b6 ', 'Unknown 0xfd subopcode: 0x2c8b ', 'Unknown 0xfd subopcode: 0x19fe ', 'Unknown 0xfd subopcode: 0x2dac ', 'Unknown 0xfd subopcode: 0x157f ', 'Unknown 0xfd subopcode: 0x24cb ', 'Unknown 0xfd subopcode: 0x398a ', 'Unknown 0xfd subopcode: 0x118d ', 'Unknown 0xfd subopcode: 0x5d70 ', 'Unknown 0xfd subopcode: 0x1931 ', 'Unknown 0xfd subopcode: 0x25c8 ', 'Unknown 0xfd subopcode: 0x6831 ', 'Unknown 0xfd subopcode: 0x25ac ', 'Unknown 0xfd subopcode: 0x1abd98 ', 'Unknown 0xfd subopcode: 0x5dae ', 'Unknown 0xfd subopcode: 0x1899 ', 'Unknown 0xfd subopcode: 0x2dec ', 'Unknown 0xfd subopcode: 0x449c '}
    '''
    # ? 最后也没有分析出结果，wasm2wat也没跑题。有时间再分析吧，现上报了
    key = '((WasmEdge_disableAOT_newer, illegal/unknown opcode), (wasmer_default_dump, unsupported opcode fd))'
    path = 'useful_results/some_logs/only_highlight_log_category/7.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    analysis_base.print_first_tc_log(use_lastest=True)
    print(analysis_base.first_tc_path)
    assert 0
    opcodes = analysis_base.illegal_wasmer_opcodes()
    # print(opcodes)
    print('-' * 30)
    for p in analysis_base.tc_paths:
        # print(p, get_log_by_lastest_impl('WAVM_default', p))
        # if is_executable_by_latest_impl('WAVM_default', p):
        #     print(p, 'is executable')
        assert is_executable_by_latest_impl('WAVM_default', p)



# =========================================================
#  ((wasm3_dump, (CannotExecute,)), (wasmi_interp, (CannotExecute,)))
# 没有bug


def rule20():
    # 无bug，主要是不支持reference
    key = '((wasm3_dump, Aborted),)'
    path = 'useful_results/some_logs/only_highlight_log_category/8.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v125_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()



# =========================================================
# * 下面这个典型
    # "only_highlight_log_category/11.json<-->((wasmi_interp, (CanExecute,)),)": [
    #     "((WAVM_default, memory OOB), (WasmEdge_disableAOT_newer, <wrong alignment>), (iwasm_classic_interp_dump, <wrong alignment>), (iwasm_fast_interp_dump, <wrong alignment>), (wasm3_dump, illegal/unknown opcode))"


# =========================================================
# * 下面这个典型
#     "only_highlight_log_category/15.json<-->((WasmEdge_disableAOT_newer, (CannotExecute,)), (iwasm_classic_interp_dump, (CannotExecute,)), (iwasm_fast_interp_dump, (CannotExecute,)), (wasm3_dump, (CannotExecute,)))": [
        # "((WasmEdge_disableAOT_newer, <wrong alignment>), (iwasm_classic_interp_dump, <wrong alignment>), (iwasm_fast_interp_dump, <wrong alignment>), (wasm3_dump, unreachable))"
# wasmer, wasmi



# ==================================
# ((iwasm_classic_interp_dump, (CanExecute,)), (iwasm_fast_interp_dump, (CanExecute,)))
def rule21():
    # * illegal opcode: 0xc5 (at offset 68) 经典，已上报
    #  可能不加mutation无法触发，要观察下有没有其他的触发条件 ==> 也能触发，报错略有差别
    key = '((WAVM_default, illegal/unknown opcode), (WasmEdge_disableAOT_newer, illegal/unknown opcode), (wasmer_default_dump, illegal/unknown opcode))'
    path = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/log_category_base/only_highlight_log_category/7.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    opcodes = analysis_base.illegal_wasmer_opcodes()
    print(opcodes)
    
def rule22():
    # *与21同
    #  可能不加mutation无法触发，要观察下有没有其他的触发条件 ==> 也能触发，报错略有差别
    # 0x c5, c6;  c6应该是修了
    key = '((WAVM_default, illegal/unknown opcode), (WasmEdge_disableAOT_newer, illegal/unknown opcode), (wasm3_dump, illegal/unknown opcode), (wasmer_default_dump, illegal/unknown opcode), (wasmi_interp, illegal/unknown opcode))'
    path = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/log_category_base/only_highlight_log_category/7.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    opcodes = analysis_base.illegal_wasmer_opcodes()
    print(opcodes)
    print('-' * 30)
    for k, v in analysis_base.illegal_wasmer_and_tcs().items():
        print(k, v)
    
def rule23():
    # no bug
    # !但是有另外一个问题，这个例子里iwasm用signal报错。。。之前的写法里还是从stdout收信息的做法就不合适了
    key = '((WAVM_default, table OOB), (WasmEdge_disableAOT_newer, table OOB), (wasm3_dump, illegal/unknown opcode), (wasmer_default_dump, table OOB))'
    path = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/log_category_base/only_highlight_log_category/7.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    print(analysis_base.first_tc_path)
    
# WAVM CAN EXECUTE
def rule24():
    # TODO ((WasmEdge_disableAOT_newer, illegal/unknown opcode), (wasmer_default_dump, illegal/unknown opcode))
    # * 和rule18差不多
    # * 报了0xf9和0xec
    # 用过自己检查下，原因，
    key = '((WasmEdge_disableAOT_newer, illegal/unknown opcode), (wasmer_default_dump, illegal/unknown opcode))'
    path = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/log_category_base/only_highlight_log_category/4.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    opcodes = analysis_base.illegal_wasmer_opcodes()
    print(opcodes)  # {'0xec (at offset 75)', '0xf9 (at offset 76)', '0xf9 (at offset 75)'}
    print('-' * 30)
    for k, v in analysis_base.illegal_wasmer_and_tcs().items():
        print(k, v)
    # print(analysis_base.illegal_wasmer_and_tcs())
    # print(get_logs(analysis_base.tc_paths,keys=['WAVM_default']))
    # print(get_logs(analysis_base.tc_paths,keys=['WasmEdge_disableAOT_newer']))

def rule25():
    # ((WasmEdge_disableAOT_newer, type mismatch), (wasmer_default_dump, type mismatch))
    # * 新上报， WAVM type mismatch
    # TODO 只报了 /media/ssd_wd1/cp910_data/main_testing_v13_350_9811/diff_tcs/i16x8.mul_124_32_16802198594248996.wasm
    key = '((WasmEdge_disableAOT_newer, type mismatch), (wasmer_default_dump, type mismatch))'
    path = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/log_category_base/only_highlight_log_category/4.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    for log in get_logs(analysis_base.tc_paths,keys=['wasmer_default_dump'], process=True)['wasmer_default_dump']:
        print(log)
    # analysis_base.wasmer_default_dump()
    


# TODO wrong alignment那几个有没有上报再检查下； wasm3 alignment报了
# TODO 典型那几个有没有上再检查下
# TODO wasm3 size mismatch的上报了但是没写在这

# * 新上报，iwasm OOB
def rule26():
    # * 新上报
    # TODO 只报了 /media/ssd_wd1/cp910_data/main_testing_v13_350_9811/diff_tcs/i16x8.mul_124_32_16802198594248996.wasm
    key = '((WasmEdge_disableAOT_newer, table OOB), (wasm3_dump, illegal/unknown opcode), (wasmer_default_dump, table OOB))'
    path = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/log_category_base/only_highlight_log_category/16.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    # for log in get_logs(analysis_base.tc_paths,keys=['wasmer_default_dump'], process=True)['wasmer_default_dump']:
    #     print(log)

    
# wasm3 可惜被修复了 。。。。
def rule27():
    # * 新bug
    key = '((wasm3_dump, Aborted),)'
    path = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/log_category_base/only_highlight_log_category/17.json'
    tcs_base_dir = '/media/ssd_wd1/cp910_data/main_testing_v13_350_9811/diff_tcs'
    analysis_base = analyzeData(path, key, tcs_base_dir)
    analysis_base.print_first_tc_log()
    print(analysis_base.first_tc_path)



# iwasm data count section的bug被修了。。。。。。。。。


# def rule28():
#     key = "((WasmEdge_disableAOT_newer, table OOB), (wasm3_dump, illegal/unknown opcode), (wasmer_default_dump, table OOB))"
#     path = '/media/ssd_wd1/cp910_data/v15_debug_empty_tcs_5100_9811_p50MC/log_category_base/only_highlight_log_category/10.json'



