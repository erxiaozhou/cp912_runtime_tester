

from collections import Counter
from script_retrive_diff_num_from_reason_summary import names2counter, reason_related_c, wrap_one_num


def cal_each_inst_info_nadiff():
    # no_mutation_reason = reason_related_c('/media/hdd_xj1/cp910_data/main_testing_v18_340_9811_no_mutation')
    # /media/hdd_xj1/cp910_data/main_testing_v18.1_340_9811_no_mutation
    no_mutation_reason = reason_related_c('/media/hdd_xj1/cp910_data/main_testing_v18.1_340_9811_no_mutation')
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
        # 
        can_execute_names, cannot_execute_names = no_mutation_reason.cal_execution_diff(row_name,get_ori_names=True)
        # assert 0, print(can_execute_names, cannot_execute_names)
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
            # print(counters_dict[row_name]['c_diff_inst_n'])
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
            # na_diff = counters_dict[row_name]['na_diff'][runtime]
            # execution = counters_dict[row_name]['execution'][runtime]
            # abortion = counters_dict[row_name]['abortion'][runtime]
            na_diff_inst_num = len(counters_dict[row_name]['na_diff_inst_n'].get(runtime, set()))
            execution_inst_num = len(counters_dict[row_name]['execution_inst_n'].get(runtime, set()))
            abortion_inst_num = len(counters_dict[row_name]['abortion_inst_n'].get(runtime, set()))
            c_diff_inst_num = len(counters_dict[row_name]['c_diff_inst_n'].get(runtime, set()))
            runtime_total['na_diff_inst_n'][runtime] += na_diff_inst_num
            runtime_total['execution_inst_n'][runtime] += execution_inst_num
            runtime_total['abortion_inst_n'][runtime] += abortion_inst_num
            runtime_total['c_diff_inst_n'][runtime] += c_diff_inst_num
            # 
            # cell = f'{c_diff:,} ({c_diff_inst_num:,}) / {execution:,} ({execution_inst_num:,}) / {abortion:,} ({abortion_inst_num:,})'
            # cell = '{} / {} / {}'.format(wrap_one_num(execution, execution_inst_num), wrap_one_num(abortion, abortion_inst_num), wrap_one_num(na_diff, na_diff_inst_num))
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
    no_mutation_reason = reason_related_c('/media/hdd_xj1/cp910_data/main_testing_v18_340_9811_no_mutation')
    mutation_reason = reason_related_c('/media/hdd_xj1/cp910_data/main_testing_v18_330_9811_2')
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
    cal_each_inst_info_nadiff()
    # cal_smy_info_nadiff()