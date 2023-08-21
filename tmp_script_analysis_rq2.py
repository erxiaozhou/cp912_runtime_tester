from file_util import read_json
import re
from pathlib import Path

inst2ctgy = read_json('./retrive_diff_num_from_reason_summary_util/inst2ctgys.json')

def inst_is_numeric(inst):
    ctgy = inst2ctgy[inst]
    return ctgy == 'Numeric'

def get_inst_name_from_file_stem(file_stem):
    p = re.compile(r'(.*)_\d+')
    return p.findall(file_stem)[0]


def wasm3_numeric():
    pre_dir = "/host_data/rewrite/v18_no_mutation/reason_summarys"
    cur_dir = "/host_data/rewrite/v19.1_no_mutation/reason_summarys"
    pre_path = Path(pre_dir) / 'full_summary.json'
    cur_path = Path(cur_dir) / 'full_summary.json'
    pre_wasm3_names = read_json(pre_path)["(('wasm3_dump', ('CanExecute',)),)"]
    pre_wasm3_inst_names = set()
    for name in pre_wasm3_names:
        inst_name = get_inst_name_from_file_stem(name)
        if inst_is_numeric(inst_name):
            pre_wasm3_inst_names.add(inst_name)
    cur_wasm3_names = read_json(cur_path)["(('wasm3_dump', ('CanExecute',)),)"]
    cur_wasm3_inst_names = set()
    for name in cur_wasm3_names:
        inst_name = get_inst_name_from_file_stem(name)
        if inst_is_numeric(inst_name):
            cur_wasm3_inst_names.add(inst_name)
    print(len(pre_wasm3_inst_names))
    print(len(cur_wasm3_inst_names))
    print(pre_wasm3_inst_names - cur_wasm3_inst_names)
    print(cur_wasm3_inst_names - pre_wasm3_inst_names)

wasm3_numeric()