from pathlib import Path
from generate_wasm_tc_util import _prepare_template, read_next_leb_num
from run_dir_std_testing import generate_code_sec_tcs
from file_util import check_dir, cp_file, rm_dir
from file_util import print_ba


def first_func_info(ori_code_sec):
    func_num, offset = read_next_leb_num(ori_code_sec, offset=0)
    before_func = ori_code_sec[:offset]
    func1_len, offset = read_next_leb_num(ori_code_sec, offset=offset)
    func_body = ori_code_sec[offset:func1_len + offset]
    content_after_func1 = ori_code_sec[func1_len + offset:]
    return before_func, func1_len,func_body, content_after_func1


def testing_f32abs(renew=True):
    f32abs_dir = Path('./ori_tcs/test_f32_abs')
    if renew or (not f32abs_dir.exists()):
        # init f32_add
        check_dir(f32abs_dir)
        all_tcs_p = Path('./ori_tcs/tcs_v8')
        name_fmt = 'f32.abs_{}.wasm'
        idx = 0
        while True:
            name = name_fmt.format(idx)
            ori_path = all_tcs_p / name
            if ori_path.exists():
                new_path = f32abs_dir / name
                cp_file(ori_path, new_path)
                idx += 1
            else:
                break


def test_func1():
    ori_tc_path = './ori_tcs/test_work_tcs/i32.add_0.wasm'
    sec_template = _prepare_template(ori_tc_path)
    ori_code_sec = bytearray(sec_template['code'])
    paths = generate_code_sec_tcs(ori_tc_path, mutate_num=5, new_tc_dir='./v2')


if __name__ == '__main__':
    testing_f32abs()