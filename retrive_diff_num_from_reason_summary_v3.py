

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

        can_exec_inst_counter, cannot_exec_inst_counter = no_mutation_reason.cal_execution_diff(row_name,get_ori_names=True)
        na_diff_inst_names = no_mutation_reason.count_na_diff(row_name, get_ori_names=True)
        counters_dict[row_name]['na_diff_inst_n'] = na_diff_inst_names
        counters_dict[row_name]['c_diff_inst_n'],skp_num = no_mutation_reason.count_c_diff(row_name, get_ori_names=True)
        counters_dict[row_name]['exec_diff_inst_n'],skp_num = no_mutation_reason.count_exec_state_diff(row_name, get_ori_names=True)
        total_c_diff_inst_n = set()
        total_na_diff_inst_n = set()
        total_exec_state_inst_n = set()
        for runtime in runtimes:
            total_c_diff_inst_n |= counters_dict[row_name]['c_diff_inst_n'].get(runtime, set())
            total_na_diff_inst_n |= counters_dict[row_name]['na_diff_inst_n'].get(runtime, set())
            total_exec_state_inst_n |= counters_dict[row_name]['exec_diff_inst_n'].get(runtime, set())

        counters_dict[row_name]['c_diff_inst_n']['Total'] = total_c_diff_inst_n
        counters_dict[row_name]['na_diff_inst_n']['Total'] = total_na_diff_inst_n
        counters_dict[row_name]['exec_diff_inst_n']['Total'] = total_exec_state_inst_n

    runtime_total = {
        'na_diff_inst_n': Counter({v: 0 for v in runtimes+ ['Total']}),
        'c_diff_inst_n': Counter({v: 0 for v in runtimes+ ['Total']}),
        'exec_diff_inst_n': Counter({v: 0 for v in runtimes+ ['Total']})
    }
    for row_name in rows:
        items = []
        items.append('    ' + title_info[row_name])
        for runtime in runtimes + ['Total']:
            na_diff_inst_num = len(counters_dict[row_name]['na_diff_inst_n'].get(runtime, set()))
            c_diff_inst_num = len(counters_dict[row_name]['c_diff_inst_n'].get(runtime, set()))
            exec_state_inst_name = len(counters_dict[row_name]['exec_diff_inst_n'].get(runtime, set()))
            runtime_total['na_diff_inst_n'][runtime] += na_diff_inst_num
            runtime_total['c_diff_inst_n'][runtime] += c_diff_inst_num
            runtime_total['exec_diff_inst_n'][runtime] += exec_state_inst_name

            cell = f'{c_diff_inst_num:,} / {exec_state_inst_name:,} / {na_diff_inst_num:,}'
            
            items.append(cell)
        print(r'\cmidrule(r){1-9}')
        print(fmt.format(*items))
    items = []
    items.append('    Total')
    for runtime in runtimes+ ['Total']:
        cell = f'{runtime_total["c_diff_inst_n"][runtime]:,} / {runtime_total["exec_diff_inst_n"][runtime]:,} / {runtime_total["na_diff_inst_n"][runtime]:,}'
        items.append(cell)
    print(r'\cmidrule(r){1-9}')
    print(fmt.format(*items))




if __name__ == '__main__':
    cal_each_inst_info_nadiff()
