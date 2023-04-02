from file_util import read_json, save_json
from pathlib import Path
import re


def get_tc_paths(json_path, key, tcs_base_dir):
    tc_names = get_tc_names(json_path, key)
    tc_file_names = ['{}.wasm'.format(name) for name in tc_names]
    tcs_base_dir = Path(tcs_base_dir)
    paths = [tcs_base_dir / name for name in tc_file_names]
    return paths


def get_tc_names(json_path, key):
    data = read_json(json_path)
    tc_names = data[key]
    return tc_names


def get_illegal_opcode(s):
    pass
    p = r'^WASM module load failed: unsupported opcode (.*)\n?$'
    r = re.compile(p).findall(s)
    return r[0]


def get_illegal_type(s):
    pass
    p = r'^WASM module load failed: invalid (.*)\n?$'
    r = re.compile(p).findall(s)
    if len(r) == 0:
        print(s)
    return r[0]
#  Unknown opcode: 


def get_wasmer_illegal_opcode(s):
    pass
    p = r' Unknown opcode: (.*)[\n ]*?$'
    r = re.compile(p).findall(s)
    if len(r) == 0:
        p = r' Validation error: (Unknown 0xfd subopcode:.*)[\n ]*?'
        r = re.compile(p).findall(s)
    return r[0]
