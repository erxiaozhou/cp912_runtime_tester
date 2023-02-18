from collections import Counter
import os
from pathlib import Path
import random
import struct
from extract_dump.extractor import dump_data_extractor
from file_util import check_dir, pickle_dump, pickle_load, read_bytes, remove_file_without_exception, rm_dir, save_json, write_bytes
import numpy as np
from file_util import path_read
from file_util import path_write
import leb128
import time
from exec_util import load_log_content, load_results


if __name__ == '__main__':
    test_path = '/media/hdd_xj1/cp910_data/main_testing/result/f32.abs_10/'
    result = load_results(test_path)
    # load_results
    print(result)
    r = result[0]
    print(type(r))
    print(r)
    assert isinstance(r, dump_data_extractor)
    r_data = r.to_dict()
    print('===')
    # for k,v in r_data.items():
    #     print(k, '\n====\n',v)
    # print(r.log_content)
    # print(r.name)
    content_dict = load_log_content(test_path)
    for k,v in content_dict.items():
        print(k, '\n====\n',v)
    print()