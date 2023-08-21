from file_util import check_dir, path_read, save_json
from pathlib import Path
import os

def get_wat_dir(wasm_dir, wat_dir):
    wasm_dir = Path(wasm_dir)
    wat_dir = check_dir(wat_dir)
    for wasm_file in wasm_dir.iterdir():
        wat_file = wat_dir / (wasm_file.name[:-5] + '.wat')
        os.system(f'wasm2wat --no-check {wasm_file} -o {wat_file}')


def wat_contains_reffunc0(wat_path):
    content = path_read(wat_path)
    # special_insts = ['ref.func', 'v128.const', 'ref.null']
    if 'ref.func' in content and ('ref.func' not in str(wat_path)):
        return True
    # if 
    # return 


def get_contain_reffunc0_names(wat_dir):
    wat_dir = Path(wat_dir)
    names = []
    for wat_file in wat_dir.iterdir():
        if wat_contains_reffunc0(wat_file):
            names.append(wat_file.name[:-4])
    return names    

def get_contain_reffunc0_names_main(base_dir, result_path):
    base_dir = Path(base_dir)
    wasm_dir = base_dir / 'diff_tcs'
    wat_dir = base_dir / 'diff_tcs_wat'
    get_wat_dir(wasm_dir, wat_dir)
    names = get_contain_reffunc0_names(wat_dir)
    # print(names)
    save_json(result_path, names)


# get_contain_reffunc0_names_main('/host_data/rewrite/v18_no_mutation', './retrive_diff_num_from_reason_summary_util/contain_reffunc0_names.json')
'''

\cmidrule(r){1-9}
    Variable instruction & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 2 / 2 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 2 / 2 / 0 / 0 \\
\cmidrule(r){1-9}
    Memory instruction & 2 / 2 / 0 / 0 & 2 / 0 / 2 / 0 & 2 / 0 / 2 / 0 & 2 / 0 / 2 / 0 & 23 / 23 / 0 / 0 & 2 / 2 / 0 / 0 & 4 / 4 / 0 / 0 & 27 / 25 / 2 / 0 \\
\cmidrule(r){1-9}
    SIMD instruction & 236 / 236 / 0 / 4 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 236 / 236 / 0 / 1 & 236 / 236 / 0 / 2 & 236 / 236 / 0 / 7 \\
\cmidrule(r){1-9}
    Reference instruction & 2 / 2 / 0 / 0 & 3 / 0 / 3 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 3 / 0 / 3 / 0 & 2 / 2 / 0 / 0 & 2 / 2 / 0 / 0 & 3 / 2 / 3 / 0 \\
\cmidrule(r){1-9}
    Table instruction & 3 / 3 / 0 / 0 & 8 / 0 / 8 / 0 & 2 / 1 / 0 / 0 & 2 / 1 / 0 / 0 & 8 / 0 / 8 / 0 & 4 / 3 / 0 / 0 & 4 / 4 / 0 / 0 & 8 / 4 / 8 / 0 \\
\cmidrule(r){1-9}
    Numeric instruction & 8 / 0 / 0 / 4 & 2 / 0 / 0 / 2 & 8 / 4 / 0 / 7 & 6 / 4 / 0 / 4 & 136 / 136 / 0 / 4 & 8 / 0 / 0 / 8 & 2 / 0 / 0 / 2 & 136 / 136 / 0 / 9 \\
\cmidrule(r){1-9}
    Parametric instruction & 3 / 3 / 0 / 0 & 2 / 0 / 2 / 1 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 3 / 1 / 2 / 0 & 3 / 3 / 0 / 0 & 3 / 3 / 0 / 0 & 3 / 3 / 2 / 1 \\
\cmidrule(r){1-9}
    Control instruction & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 1 / 1 / 0 / 0 & 1 / 0 / 0 / 0 & 0 / 0 / 0 / 0 & 2 / 1 / 0 / 0 \\
\cmidrule(r){1-9}
    Total & 254 / 246 / 0 / 8 & 17 / 0 / 15 / 3 & 12 / 5 / 2 / 7 & 10 / 5 / 2 / 4 & 176 / 163 / 13 / 4 & 256 / 246 / 0 / 9 & 251 / 249 / 0 / 4 & 417 / 409 / 15 / 17 \\
'''