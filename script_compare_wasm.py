#!/home/zph/anaconda3/bin/python
import sys
from generate_wasm_tc_util import prepare_template
from file_util import print_ba


def compare_2wasms(p1, p2):
    sec1 = prepare_template(p1)
    sec2 = prepare_template(p2)
    keys1 = list(sec1.keys())
    keys2 = list(sec2.keys())
    print('=' * 20, 'only in {}'.format(p1))
    for k in keys1:
        if k not in keys2:
            print(k)
            print_ba(sec1[k])
    print('=' * 20, 'only in {}'.format(p2))
    for k in keys2:
        if k not in keys1:
            print(k)
            print_ba(sec2[k])
    for k in keys1:
        if k in keys2:
            if sec1[k] == sec2[k]:
                continue
            print(k)
            print(p1, end=': ')
            print(len(sec1[k]), end=': ')
            print_ba(sec1[k])
            print(p2, end=': ')
            print(len(sec2[k]), end=': ')
            print_ba(sec2[k])
            print('-' * 20)


if __name__ == '__main__':
    argvs = sys.argv
    assert len(argvs) == 3
    p1 = argvs[1]
    p2 = argvs[2]
    compare_2wasms(p1, p2)
