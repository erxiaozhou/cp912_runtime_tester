import re
from tqdm import tqdm
from load_results_util import load_results_from_one_dumped_data_dir
from extract_dump.dump_data_util import get_diff_attr_names
from file_util import read_json, dir_file_num
from pathlib import Path
from collections import Counter
from extract_dump import are_different


all_runtime_names = [
    'wasmer_default_dump',
    'wasmi_interp',
    'iwasm_classic_interp_dump',
    'iwasm_fast_interp_dump',
    'wasm3_dump',
    'WasmEdge_disableAOT_newer',
    'WAVM_default',
]

class reasonRelatedC:
    def __init__(self, base_dir):
        base_dir = Path(base_dir)
        self.diff_dir = base_dir / 'diff_tcs'
        self.dumped_data_dir = base_dir / 'dumped_data'
        self.reson_file_path = base_dir / 'reason_summarys' / 'full_summary.json'
        self.reason_summary = read_json(self.reson_file_path)
        self.ctgy_info = read_json('./retrive_diff_num_from_reason_summary_util/inst2ctgys.json')


    def check_all_tc_num(self):
        num_from_diff_dir = dir_file_num(self.diff_dir)
        num_from_reason_file = _all_tc_num_in_reason_file(self.reson_file_path)
        assert num_from_diff_dir == num_from_reason_file, print(num_from_diff_dir, num_from_reason_file)
        print(num_from_reason_file)
    
    def count_exec_state_diff(self, ctgy_name=None, get_ori_names=True):
        assert get_ori_names
        not_sure_keys, runtime_counter, to_skip_list, to_skip_num = self.only_can_cannot_execute(ctgy_name, get_ori_names)
        compare_based_c = self.count_by_compare_exec_state(not_sure_keys, ctgy_name, get_ori_names)
        if get_ori_names:
            
            for k in all_runtime_names:
                if k not in runtime_counter:
                    runtime_counter[k] = set()
                runtime_counter[k].update(compare_based_c.get(k, set()))
        else:
            runtime_counter+=compare_based_c
        return runtime_counter, to_skip_num


    def count_c_diff(self, ctgy_name=None, get_ori_names=False):
        not_sure_keys, runtime_counter, to_skip_list, to_skip_num = self.only_can_cannot_execute(ctgy_name, get_ori_names)
        compare_based_c = self.count_by_compare(not_sure_keys, ctgy_name, get_ori_names)
        if get_ori_names:
            
            for k in all_runtime_names:
                if k not in runtime_counter:
                    runtime_counter[k] = set()
                runtime_counter[k].update(compare_based_c.get(k, set()))
        else:
            runtime_counter+=compare_based_c
        return runtime_counter, to_skip_num

    def only_can_cannot_execute(self, ctgy_name=None, get_ori_names=False):
        # not_sure_list = []
        not_sure_keys = []
        to_skip_list = []
        to_skip_num = 0
        runtime_counter = Counter()
        name_dict = dict()
        execute_related_tuple = set(['CanExecute', 'CannotExecute'])
        for k, v in self.reason_summary.items():
            tc_num = self.count_tc_num_with(v, ctgy_name)
            tcs = self.tc_num_with(v, ctgy_name)
            if 'CanRun_CannotDump' in k:
                to_skip_list.append(k)
                continue
            
            elif k.count('has_timeout') != k.count("('WasmEdge_disableAOT_newer', ('has_timeout',))"):
                not_sure_keys.append(k)
                to_skip_num += tc_num
                continue
            k_obj = key_(k)
            other_kwds = [v for v in k_obj.kwds_list if v not in execute_related_tuple]
            execute_related_keys = [v for v in k_obj.kwds_list if v in execute_related_tuple]
            if len(other_kwds) <= 3 and len(execute_related_keys)  <=3:
                print(f'3 num rule: {k}')
                for runtime_name in k_obj.runtime_names:
                    if get_ori_names:
                        if runtime_name not in name_dict:
                            name_dict[runtime_name] = set()
                        name_dict[runtime_name].update(tcs)
                    else:
                        runtime_counter[runtime_name] += tc_num
                continue
            elif 'stack_bytes_process_nan' in k:
                not_sure_keys.append(k)
                continue
            
            elif k_obj.kws.issubset(execute_related_tuple):
                assert len(k_obj.kws) == 1, print(k_obj.kws, k_obj.data)
                if len(k_obj.kwds_list) <=3:
                    print(f'Cannot Can rule: {k}')
                    for runtime_name in k_obj.runtime_names:
                        if get_ori_names:
                            if runtime_name not in name_dict:
                                name_dict[runtime_name] = set()
                            name_dict[runtime_name].update(tcs)
                        else:
                            runtime_counter[runtime_name] += tc_num
                else:
                    print(f'Cannot Can revise rule: f{k}')
                    revised_list =[v for v in all_runtime_names if v not in k_obj.runtime_names]
                    for runtime_name in revised_list:
                        if get_ori_names:
                            if runtime_name not in name_dict:
                                name_dict[runtime_name] = set()
                            name_dict[runtime_name].update(tcs)
                        else:
                            runtime_counter[runtime_name] += tc_num
                continue
            print('?????????????????????????????')
            not_sure_keys.append(k)
        if get_ori_names:
            return not_sure_keys, name_dict, to_skip_list, to_skip_num
        else:
            return not_sure_keys, runtime_counter, to_skip_list, to_skip_num

    def count_na_diff(self, ctgy_name=None, get_ori_names=False):
        # not_sure_list = []
        not_sure_keys = []
        to_skip_num = 0
        runtime_counter = Counter()
        name_dict = dict()
        execute_related_tuple = set(['CanExecute', 'CannotExecute'])
        keys = []
        for k, v in self.reason_summary.items():
            tc_num = self.count_tc_num_with(v, ctgy_name)
            tcs = self.tc_num_with(v, ctgy_name)
            if 'CanRun_CannotDump' in k:
                continue
            k_obj = key_(k)
            kwds = k_obj.kwds_list
            if 'stack_bytes_process_nan' not in kwds:
                continue
            # infer can run num
            if 'CanExecute' in kwds:
                can_run_num = kwds.count('CanExecute')
                can_run_runtimes = [_k for _k,_v in k_obj.data.items() if 'CanExecute' in _v]
            elif 'CannotExecute' in kwds:
                can_run_num = 7 - kwds.count('CannotExecute')
                can_run_runtimes = [_k for _k,_v in k_obj.data.items() if 'CannotExecute' not in _v]
            else:
                can_run_num = 7
                can_run_runtimes = all_runtime_names
            result = self.count_by_compare_nan(k, can_run_num, ctgy_name, get_ori_names, can_run_runtimes)
            if get_ori_names:
                for _k, _v in result.items():
                    if _k not in name_dict:
                        name_dict[_k] = set()
                    name_dict[_k].update(_v)
            else:
                runtime_counter+=result
        if get_ori_names:
            return name_dict
        else:
            return runtime_counter
            
    def count_by_compare_nan(self, key, th, ctgy=None, get_ori_names=False, can_run_runtimes=None):
        name_p = re.compile(r'^(.*)_\d+$')
        skp_list = read_json('./retrive_diff_num_from_reason_summary_util/to_skip_names.json')
        c = Counter()
        name_dict = dict()
        tcs = self.reason_summary[key]
        if ctgy is not None:
            tcs = [_ for _ in tcs if (self.ctgy_info[name_p.findall(_)[0]] == ctgy)]
        tcs = [_ for _ in tcs if _ not in skp_list]
        for tc in tqdm(tcs):
            dumped_dir = self.dumped_data_dir / tc
            names = analyze_a_tc_only_stack(dumped_dir, th, can_run_runtimes)
            for name in names:
                c[name] += 1
                if name not in name_dict:
                    name_dict[name] = set()
                name_dict[name].add(name_p.findall(tc)[0])
        if get_ori_names:
            return name_dict
        else:
            return c

    def count_by_compare(self, keys, ctgy=None, get_ori_names=False):
        name_p = re.compile(r'^(.*)_\d+$')
        c = Counter()
        name_dict = dict()
        skp_list = read_json('./retrive_diff_num_from_reason_summary_util/to_skip_names.json')
        tcs = []
        for k in keys:
            tcs.extend(self.reason_summary[k])
        tcs = [_ for _ in tcs if _ not in skp_list]
        if ctgy is not None:
            tcs = [_ for _ in tcs if self.ctgy_info[name_p.findall(_)[0]] == ctgy]
        for tc in tqdm(tcs):
            dumped_dir = self.dumped_data_dir / tc
            names = analyze_a_tc(dumped_dir)
            for name in names:
                c[name] += 1
                if name not in name_dict:
                    name_dict[name] = set()
                name_dict[name].add(name_p.findall(tc)[0])
        if get_ori_names:
            return name_dict
        else:
            return c
    def count_by_compare_exec_state(self, keys, ctgy=None, get_ori_names=False):
        name_p = re.compile(r'^(.*)_\d+$')
        c = Counter()
        name_dict = dict()
        skp_list = read_json('./retrive_diff_num_from_reason_summary_util/to_skip_names.json')
        tcs = []
        for k in keys:
            tcs.extend(self.reason_summary[k])
        tcs = [_ for _ in tcs if _ not in skp_list]
        if ctgy is not None:
            tcs = [_ for _ in tcs if self.ctgy_info[name_p.findall(_)[0]] == ctgy]
        for tc in tqdm(tcs):
            dumped_dir = self.dumped_data_dir / tc
            names = analyze_a_tc_exec_state(dumped_dir)
            for name in names:
                c[name] += 1
                if name not in name_dict:
                    name_dict[name] = set()
                name_dict[name].add(name_p.findall(tc)[0])
        if get_ori_names:
            return name_dict
        else:
            return c

    def tc_num_with(self, tc_names, ctgy):
        skp_list = read_json('./retrive_diff_num_from_reason_summary_util/to_skip_names.json')
        name_p = re.compile(r'^(.*)_\d+$')
        inst_names = set()
        if ctgy is None:
            return len(tc_names)
        else:
            for name in tc_names:
                if name in skp_list:
                    continue
                name = name_p.findall(name)[0]
                assert name in self.ctgy_info
                if self.ctgy_info[name] == ctgy:
                    inst_names.add(name)
            return inst_names
        
    def count_tc_num_with(self, tc_names, ctgy):
        skp_list = read_json('./retrive_diff_num_from_reason_summary_util/to_skip_names.json')
        name_p = re.compile(r'^(.*)_\d+$')
        if ctgy is None:
            return len(tc_names)
        else:
            num = 0
            for name in tc_names:
                if name in skp_list:
                    continue
                name = name_p.findall(name)[0]
                assert name in self.ctgy_info, print(name, self.ctgy_info)
                if self.ctgy_info[name] == ctgy:
                    num += 1
            return num

    def cal_execution_diff(self, ctgy_name=None, get_ori_names=False):
        to_skip_num = 0
        can_execute_counter = Counter()
        cannot_execute_counter = Counter()
        can_execute_name_dict = dict()
        cannot_execute_name_dict = dict()
        execute_related_tuple = set(['CanExecute', 'CannotExecute'])
        for k, v in self.reason_summary.items():
            if 'CanRun_CannotDump' in k:
                continue
            tc_num = self.count_tc_num_with(v, ctgy_name)
            tcs = self.tc_num_with(v, ctgy_name)
            k_obj = key_(k)
            k_data = k_obj.data
            cannot_execute_names = [_k for _k, _v in k_data.items() if 'CannotExecute' in _v]
            can_execute_keys = [_k for _k, _v in k_data.items() if 'CanExecute' in _v]
            if k_obj.kws.intersection(execute_related_tuple) == set():
                continue
            print(k, cannot_execute_names, can_execute_keys)
            for name in all_runtime_names:
                if name in cannot_execute_names:
                    if len(cannot_execute_names) <= 3:
                        if get_ori_names:
                            if name not in cannot_execute_name_dict:
                                cannot_execute_name_dict[name] = set()
                            cannot_execute_name_dict[name].update(tcs)
                        else:
                            cannot_execute_counter[name] += tc_num
                else:
                    if len(cannot_execute_names) >= 4:
                        if get_ori_names:
                            if name not in can_execute_name_dict:
                                can_execute_name_dict[name] = set()
                            can_execute_name_dict[name].update(tcs)
                        else:
                            can_execute_counter[name] += tc_num
                if name in can_execute_keys:
                    if len(can_execute_keys) <= 3:
                        if get_ori_names:
                            if name not in can_execute_name_dict:
                                can_execute_name_dict[name] = set()
                            can_execute_name_dict[name].update(tcs)
                        else:
                            can_execute_counter[name] += tc_num
                else:
                    if len(can_execute_keys) >= 4:
                        if get_ori_names:
                            if name not in cannot_execute_name_dict:
                                cannot_execute_name_dict[name] = set()
                            cannot_execute_name_dict[name].update(tcs)
                        else:
                            cannot_execute_counter[name] += tc_num
        if get_ori_names:
            return can_execute_name_dict, cannot_execute_name_dict
        else:
            return can_execute_counter, cannot_execute_counter


def analyze_a_tc(dumped_tc_dir):
    dumped_results = load_results_from_one_dumped_data_dir(dumped_tc_dir)
    log_counter = Counter()
    assert len(dumped_results) == 7
    for r1_idx in range(7):
        for r2_idx in range(r1_idx+1, 7):
            if get_diff_attr_names(dumped_results[r1_idx], dumped_results[r2_idx]):
                log_counter[dumped_results[r1_idx].name] += 1
                log_counter[dumped_results[r2_idx].name] += 1
    names = [k for k, v in log_counter.items() if v >= 4]
    return names

def analyze_a_tc_exec_state(dumped_tc_dir):
    dumped_results = load_results_from_one_dumped_data_dir(dumped_tc_dir)
    log_counter = Counter()
    assert len(dumped_results) == 7
    for r1_idx in range(7):
        for r2_idx in range(r1_idx+1, 7):
            if get_diff_attr_names(dumped_results[r1_idx], dumped_results[r2_idx], ['log_has_failed_content', 'has_timeout', 'has_crash']):
                log_counter[dumped_results[r1_idx].name] += 1
                log_counter[dumped_results[r2_idx].name] += 1
    names = [k for k, v in log_counter.items() if v >= 4]
    return names


def analyze_a_tc_only_stack(dumped_tc_dir, th, can_run_runtimes):
    dumped_results = load_results_from_one_dumped_data_dir(dumped_tc_dir)
    # assert th == len(can_run_runtimes), print(th, len(can_run_runtimes), can_run_runtimes)
    log_counter = Counter()
    # assert len(dumped_results) == 7
    dumped_results = [r for r in dumped_results if not r.failed_exec]
    if (len(dumped_results)) < 2:
        return []
    for r1_idx in range(len(dumped_results)):
        for r2_idx in range(r1_idx+1, len(dumped_results)):
            # name_tuple = (dumped_results[r1_idx].name, dumped_results[r2_idx].name)
            if get_diff_attr_names(dumped_results[r1_idx], dumped_results[r2_idx], ['stack_bytes_process_nan']):
                log_counter[dumped_results[r1_idx].name] += 1
                log_counter[dumped_results[r2_idx].name] += 1
    names = [k for k, v in log_counter.items() if v*2 >= th]
    return names

class key_:
    def __init__(self, k):
        self.k = k
        self.data = retrive_k(k)
    @property
    def kws(self):
        vs = set()
        for vs_ in self.data.values():
            vs.update(vs_)
        return vs
    @property
    def kwds_list(self):
        vs = []
        for vs_ in self.data.values():
            vs.extend(vs_)
        return vs
    @property
    def runtime_names(self):
        return list(self.data)

def retrive_k(k):
    t = eval(k)
    data = {}
    for k, v in t:
        data[k] = v
    return data


def _all_tc_num_in_reason_file(p):
    data = read_json(p)
    sum_ = 0
    for v in data.values():
        sum_ += len(v)
    return sum_
def wrap_one_num(n1, n2):
    if n1 == 0:
        return 0
    else:
        return f'{n1:,} ({n2:,})'


def names2counter(d):
    new_d = {}
    for k in all_runtime_names:
        new_d[k] = len(d.get(k, []))
    return new_d
