import os
import json
import struct
import time
from pathlib import Path
import pickle
import chardet


def pickle_dump(path, data):
    if isinstance(path, str):
        path = Path(path)
    with path.open("wb") as f:
        pickle.dump(data, f)


def pickle_load(path):
    if isinstance(path, str):
        path = Path(path)
    with path.open("rb") as f:
        data = pickle.load(f)
    return data


def check_dir(path, mkdir=True):
    if not isinstance(path, Path):
        path = Path(path)
    if mkdir:
        parent_path = path.parent
        if not parent_path.exists():
            check_dir(parent_path)
        if not path.exists():
            path.mkdir()
        return path
    return path.exists()


def read_json(path):
    if isinstance(path, str):
        path = Path(path)
    f = path.open(encoding="utf8")
    data = json.load(f)
    f.close()
    return data


def save_json(path, data):
    if isinstance(path, str):
        path = Path(path)
    f = path.open("w", encoding="utf8")
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()


def write_bytes(path, byte_seq):
    with open(path, 'wb') as fwriter:
        fwriter.write(byte_seq)


def read_bytes(path):
    with open(path, 'rb') as f:
        return bytearray(f.read())


def path_write(path, content):
    if isinstance(path, str):
        path = Path(path)
    with path.open('w', encoding='utf8') as f:
        f.write(content)


def path_read(path):
    if isinstance(path, str):
        path = Path(path)
    try:
        with path.open('r', encoding='utf8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with path.open('rb') as f:
            rbs = f.read()
            result = chardet.detect(rbs)
            encoding = result['encoding']
        if encoding is not None:
            with path.open('r', encoding=encoding) as f:
                content = f.read()
        else:
            with path.open('rb') as f:
                content = f.read()
            content = str(content)
    return content


def rm_dir(dir):
    os.system("rm -rf {}".format(dir))
    return dir


def cp_file(src_path, tgt_path):
    os.system("cp {} {}".format(src_path, tgt_path))


def get_time_string():
    return time.strftime('%m-%d-%H-%M-%S', time.localtime())


def remove_file_without_exception(path):
    path = str(path)
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def combine_path(p1, p2):
    s = Path(p1) / p2
    return str(s)


def print_ba(ba):
    ba = bytearray(ba)
    print([hex(x) for x in ba])


def bytes2uint(bs):
    int_val = int.from_bytes(bs, byteorder='little', signed=False)
    return int_val


def uint2bytes(val, int_byte_num):
    # int_byte_num: 4, 8, ...
    return bytearray(int.to_bytes(val, int_byte_num,
              byteorder='little', signed=False))


def f32bytes(val):
    return struct.pack('<f', val)


def f64bytes(val):
    return struct.pack('<d', val)


def bytes2f32(bs):
    return struct.unpack('=f', bs)
