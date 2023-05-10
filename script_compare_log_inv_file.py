#!/home/zph/anaconda3/bin/python
import sys
import re
from file_util import read_json, save_json


def get_file_paths_to_compare():
    argv = sys.argv
    assert len(argv) == 3
    return argv[1], argv[2]

def get_reason_key_from_whole_key(whole_key):
    p = r'<-->(.*)$'
    p = re.compile(p)
    reason_key = p.findall(whole_key)[0]
    return reason_key


def get_content_only_in_first_dict(data1, data2):
    only_in_data1_log = {}
    for k, v in data1.items():
        if k not in data2:
            only_in_data1_log[k] = v
        else:
            L = [log for log in v if log not in data2[k]]
            if L:
                only_in_data1_log[k] = L
    return only_in_data1_log


def get_key_only_in_first_dict(data1, data2):
    keys = [k for k in data1.keys() if k not in data2]
    return keys


if __name__ == '__main__':
    path1, path2 = get_file_paths_to_compare()
    data1 = read_json(path1)
    data2 = read_json(path2)
    data1 = {get_reason_key_from_whole_key(k): v for k,v in data1.items()}
    data2 = {get_reason_key_from_whole_key(k): v for k,v in data2.items()}
    only_in_data1_log = get_content_only_in_first_dict(data1, data2)
    only_in_data2_log = get_content_only_in_first_dict(data2, data1)
    only_in_data1_key = get_key_only_in_first_dict(data1, data2)
    only_in_data2_key = get_key_only_in_first_dict(data2, data1)
    # print
    # print('first log: {}'.format(path1))
    # print('log only in first log')
    # for k, v in only_in_data1_log.items():
    #     print('key: ={}='.format(k))
    #     print('log:')
    #     for log in v:
    #         print('===> {}'.format(log))
            
    # print('second log: {}'.format(path2))
    # print('log only in second log')
    # for k, v in only_in_data2_log.items():
    #     print('key: ={}='.format(k))
    #     print('log:')
    #     for log in v:
    #         print('===> {}'.format(log))
    result = {}
    result['log_only_in_{}'.format(path1)] = only_in_data1_log
    result['log_only_in_{}'.format(path2)] = only_in_data2_log
    result['key_only_in_{}'.format(path1)] = only_in_data1_key
    result['key_only_in_{}'.format(path2)] = only_in_data2_key
    save_json('tt.json', result)