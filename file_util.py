import os
import json
import time
from pathlib import Path


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
    data = json.load(path.open(encoding="utf8"))
    return data


def save_json(path, data):
    if isinstance(path, str):
        path = Path(path)
    json.dump(data,
              path.open("w", encoding="utf8"),
              ensure_ascii=False,
              indent=4)


def write_bytes(path, byte_seq):
    with open(path, 'wb') as fwriter:
        fwriter.write(byte_seq)


def path_write(path, content):
    if isinstance(path, str):
        path = Path(path)
    with path.open('w', encoding='utf8') as f:
        f.write(content)


def path_read(path):
    if isinstance(path, str):
        path = Path(path)
    with path.open('r', encoding='utf8') as f:
        content = f.read()
    return content


def rm_dir(dir):
    os.system("rm -rf {}".format(dir))


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
