

from collections import Counter
from retrive_diff_num_from_reason_summary import names2counter, reasonRelatedC, wrap_one_num
from tmp_script_detect_reffunc0 import get_contain_reffunc0_names_main

no_mutation_result_base = '/host_data/rewrite/v18_no_mutation'
no_mutation_result_base = '/host_data/rewrite/v19.2_no_mutation'

def cal_each_inst_info_nadiff():
    no_mutation_reason = reasonRelatedC(no_mutation_result_base)
    rows = ['Variable', 'Memory', 'Vector', 'Reference', 'Table', 'Numeric', 'Parametric', 'Control']
    runtimes = ['wasmer_default_dump', 'wasmi_interp', 'iwasm_classic_interp_dump', 'iwasm_fast_interp_dump', 'wasm3_dump', 'WasmEdge_disableAOT_newer', 'WAVM_default']
    title_info = {
        'Variable': 'Variable instruction',
        'Memory': 'Memory instruction',
        'Vector': 'SIMD instruction',
        'Reference': 'Reference instruction',
        'Table': 'Table instruction',
        'Numeric': 'Numeric instruction',
        'Parametric': 'Parametric instruction',
        'Control': 'Control instruction',
        'Total': 'Total'
    }
    counters_dict = {}
    fmt = '{} & {} & {} & {} & {} & {} & {} & {} & {} \\\\'
    for row_name in rows:
        counters_dict[row_name] = {}
        can_execute_counter, cannot_execute_counter = no_mutation_reason.cal_execution_diff(row_name)
        counters_dict[row_name]['execution'] = can_execute_counter
        counters_dict[row_name]['abortion'] = cannot_execute_counter
        na_counter = no_mutation_reason.count_na_diff(row_name)
        counters_dict[row_name]['na_diff'] = na_counter
        counters_dict[row_name]['c_diff'],skp_num = no_mutation_reason.count_c_diff(row_name)

        can_execute_names, cannot_execute_names = no_mutation_reason.cal_execution_diff(row_name,get_ori_names=True)

        can_exec_inst_counter = can_execute_names
        cannot_exec_inst_counter = cannot_execute_names
        counters_dict[row_name]['execution_inst_n'] = can_exec_inst_counter
        counters_dict[row_name]['abortion_inst_n'] = cannot_exec_inst_counter
        na_diff_inst_names = no_mutation_reason.count_na_diff(row_name, get_ori_names=True)
        counters_dict[row_name]['na_diff_inst_n'] = na_diff_inst_names
        counters_dict[row_name]['c_diff_inst_n'],skp_num = no_mutation_reason.count_c_diff(row_name, get_ori_names=True)
        total_c_diff_inst_n = set()
        total_na_diff_inst_n = set()
        total_execution_inst_n = set()
        total_abortion_inst_n = set()
        for runtime in runtimes:
            total_c_diff_inst_n |= counters_dict[row_name]['c_diff_inst_n'].get(runtime, set())
            total_na_diff_inst_n |= counters_dict[row_name]['na_diff_inst_n'].get(runtime, set())
            total_execution_inst_n |= counters_dict[row_name]['execution_inst_n'].get(runtime, set())
            total_abortion_inst_n |= counters_dict[row_name]['abortion_inst_n'].get(runtime, set())

        counters_dict[row_name]['c_diff_inst_n']['Total'] = total_c_diff_inst_n
        counters_dict[row_name]['na_diff_inst_n']['Total'] = total_na_diff_inst_n
        counters_dict[row_name]['execution_inst_n']['Total'] = total_execution_inst_n
        counters_dict[row_name]['abortion_inst_n']['Total'] = total_abortion_inst_n
    # counters_dict['Total'] = {}



    runtime_total = {
        'na_diff_inst_n': Counter({v: 0 for v in runtimes+ ['Total']}),
        'execution_inst_n': Counter({v: 0 for v in runtimes+ ['Total']}),
        'abortion_inst_n': Counter({v: 0 for v in runtimes+ ['Total']}),
        'c_diff_inst_n': Counter({v: 0 for v in runtimes+ ['Total']})
    }
    # print
    for row_name in rows:
        items = []
        items.append('    ' + title_info[row_name])
        for runtime in runtimes + ['Total']:
            na_diff_inst_num = len(counters_dict[row_name]['na_diff_inst_n'].get(runtime, set()))
            execution_inst_num = len(counters_dict[row_name]['execution_inst_n'].get(runtime, set()))
            abortion_inst_num = len(counters_dict[row_name]['abortion_inst_n'].get(runtime, set()))
            c_diff_inst_num = len(counters_dict[row_name]['c_diff_inst_n'].get(runtime, set()))
            runtime_total['na_diff_inst_n'][runtime] += na_diff_inst_num
            runtime_total['execution_inst_n'][runtime] += execution_inst_num
            runtime_total['abortion_inst_n'][runtime] += abortion_inst_num
            runtime_total['c_diff_inst_n'][runtime] += c_diff_inst_num

            cell = f'{c_diff_inst_num:,} / {execution_inst_num:,} / {abortion_inst_num:,} / {na_diff_inst_num:,}'
            
            items.append(cell)
        print(r'\cmidrule(r){1-9}')
        print(fmt.format(*items))
    items = []
    items.append('    Total')
    for runtime in runtimes+ ['Total']:
        cell = f'{runtime_total["c_diff_inst_n"][runtime]:,} / {runtime_total["execution_inst_n"][runtime]:,} / {runtime_total["abortion_inst_n"][runtime]:,} / {runtime_total["na_diff_inst_n"][runtime]:,}'
        items.append(cell)
    print(r'\cmidrule(r){1-9}')
    print(fmt.format(*items))



def cal_smy_info_nadiff():
    no_mutation_reason = reasonRelatedC('no_mutation_result_base')
    runtimes = ['wasmer_default_dump', 'wasmi_interp', 'iwasm_classic_interp_dump', 'iwasm_fast_interp_dump', 'wasm3_dump', 'WasmEdge_disableAOT_newer', 'WAVM_default']
    
    m_can_execute_counter, m_cannot_execute_counter = no_mutation_reason.cal_execution_diff()
    m_na_counter = no_mutation_reason.count_na_diff()
    c_diff_counter ,skp_num = no_mutation_reason.count_c_diff()
    # t_can_execute_counter, t_cannot_execute_counter = mutation_reason.cal_execution_diff()
    # t_na_counter = no_mutation_reason.count_na_diff()
    rows = ['Total']
    diff_counter = dict()
    for row in rows:
        diff_counter[row] = dict()
    diff_counter['Total']['execution'] = m_can_execute_counter
    diff_counter['Total']['abortion'] = m_cannot_execute_counter
    diff_counter['Total']['na_diff'] = m_na_counter
    diff_counter['Total']['c_diff'] = c_diff_counter
    # diff_counter['Total']['execution'] = t_can_execute_counter
    # diff_counter['Total']['abortion'] = t_cannot_execute_counter
    # diff_counter['Total']['na_diff'] = t_na_counter
    # diff_counter['Mutator']['execution'] = t_can_execute_counter - m_can_execute_counter
    # diff_counter['Mutator']['abortion'] = t_cannot_execute_counter - m_cannot_execute_counter
    # diff_counter['Mutator']['na_diff'] = t_na_counter - m_na_counter
    
    fmt = '{} & {} & {} & {} & {} & {} & {} & {} & \\\\'
    # print
    for row in rows:
        items = []
        items.append('    ' + row)
        for runtime in runtimes:
            cell = '{} / {} / {} / {}'.format(diff_counter[row]['c_diff'][runtime], diff_counter[row]['execution'][runtime], diff_counter[row]['abortion'][runtime], diff_counter[row]['na_diff'][runtime])
            
            items.append(cell)
        print(r'\cmidrule(r){1-9}')
        print(fmt.format(*items))


if __name__ == '__main__':
    # get_contain_reffunc0_names_main(no_mutation_result_base, './retrive_diff_num_from_reason_summary_util/to_skip_names.json')

    cal_each_inst_info_nadiff()
    # cal_smy_info_nadiff()
'''
\cmidrule(r){1-9}
    Variable instruction & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 2 / 2 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 2 / 2 / 0 / 0 \\ 一样
    Variable instruction & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 2 / 2 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 2 / 2 / 0 / 0 \\
\cmidrule(r){1-9}
    Memory instruction & 2 / 2 / 0 / 0 & 2 / 0 / 2 / 0 & 2 / 0 / 2 / 0 & 2 / 0 / 2 / 0 & 23 / 23 / 0 / 0 & 2 / 2 / 0 / 0 & 4 / 4 / 0 / 0 & 27 / 25 / 2 / 0 \\ WasmEdge 在memory.init上的diff应该是被盖住了,即 init上存在其他diff ; iwasm与wasmi不能执行的 是
    Memory instruction & 2 / 2 / 0 / 0 & 2 / 0 / 2 / 0 & 2 / 0 / 2 / 0 & 2 / 0 / 2 / 0 & 23 / 23 / 0 / 0 & 2 / 2 / 0 / 0 & 6 / 6 / 0 / 0 & 27 / 25 / 2 / 0 \\
\cmidrule(r){1-9}
    SIMD instruction & 236 / 236 / 0 / 4 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 236 / 236 / 0 / 0 & 236 / 236 / 0 / 2 & 236 / 236 / 0 / 6 \\       # 有差别，没有质的影响
\cmidrule(r){1-9}
    Reference instruction & 1 / 1 / 0 / 0 & 3 / 0 / 3 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 3 / 0 / 3 / 0 & 1 / 1 / 0 / 0 & 1 / 1 / 0 / 0 & 3 / 1 / 3 / 0 \\       新的应该是更正确的。wasmi wasm3应该全部不能执行
    Reference instruction & 1 / 1 / 0 / 0 & 2 / 0 / 2 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 2 / 0 / 2 / 0 & 1 / 1 / 0 / 0 & 1 / 1 / 0 / 0 & 2 / 1 / 2 / 0 \\
\cmidrule(r){1-9}
    Table instruction & 0 / 0 / 0 / 0 & 8 / 0 / 8 / 0 & 2 / 1 / 0 / 0 & 2 / 1 / 0 / 0 & 8 / 0 / 8 / 0 & 1 / 0 / 0 / 0 & 1 / 1 / 0 / 0 & 8 / 1 / 8 / 0 \\       # 有差别， WasmEdge 的1 因为table.init里的crash，iwasm的两个是因为crash
    Table instruction & 0 / 0 / 0 / 0 & 5 / 0 / 5 / 0 & 1 / 1 / 0 / 0 & 1 / 1 / 0 / 0 & 5 / 0 / 5 / 0 & 0 / 0 / 0 / 0 & 1 / 1 / 0 / 0 & 5 / 1 / 5 / 0 \\
\cmidrule(r){1-9}
    Numeric instruction & 8 / 0 / 0 / 4 & 2 / 0 / 0 / 2 & 6 / 0 / 0 / 6 & 2 / 0 / 0 / 2 & 136 / 136 / 0 / 4 & 8 / 0 / 0 / 8 & 2 / 0 / 0 / 2 & 136 / 136 / 0 / 8 \\       # 有差别, wasm3多了一个,问题不大
    Numeric instruction & 8 / 0 / 0 / 4 & 2 / 0 / 0 / 2 & 6 / 0 / 0 / 6 & 2 / 0 / 0 / 2 & 135 / 135 / 0 / 4 & 8 / 0 / 0 / 8 & 2 / 0 / 0 / 2 & 135 / 135 / 0 / 8 \\      # 要调研下差的wasm3是是很么情况
\cmidrule(r){1-9}
    Parametric instruction & 3 / 3 / 0 / 0 & 2 / 0 / 2 / 1 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 3 / 1 / 2 / 0 & 3 / 3 / 0 / 0 & 3 / 3 / 0 / 0 & 3 / 3 / 2 / 1 \\  drop+ref 与 select_1C+ref 导致两个不能执行的diff; select+ ref大家都不能执行
    Parametric instruction & 3 / 3 / 0 / 0 & 1 / 0 / 0 / 1 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 2 / 1 / 1 / 0 & 3 / 3 / 0 / 0 & 3 / 3 / 0 / 0 & 3 / 3 / 1 / 1 \\   select+ref是不是出了问题
\cmidrule(r){1-9}
    Control instruction & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 1 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 1 / 0 / 0 / 0 \\ 一样
    Control instruction & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 1 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 1 / 0 / 0 / 0 \\
    \cmidrule(r){1-9}
    Total & 250 / 242 / 0 / 8 & 17 / 0 / 15 / 3 & 10 / 1 / 2 / 6 & 6 / 1 / 2 / 2 & 175 / 162 / 13 / 4 & 252 / 242 / 0 / 8 & 247 / 245 / 0 / 4 & 416 / 404 / 15 / 15 \\

'''