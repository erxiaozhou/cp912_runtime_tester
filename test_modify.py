from file_util import check_dir, rm_dir
from generate_wasm_tc import _prepare_template, read_next_leb_num
from test_a_dir_std import generate_code_sec_tcs

def print_ba(ba):
    print([hex(x) for x in ba])


def first_func_info(ori_code_sec):
    func_num, offset = read_next_leb_num(ori_code_sec, offset=0)
    before_func = ori_code_sec[:offset]
    func1_len, offset = read_next_leb_num(ori_code_sec, offset=offset)
    func_body = ori_code_sec[offset:func1_len + offset]
    content_after_func1 = ori_code_sec[func1_len + offset:]
    return before_func, func1_len,func_body, content_after_func1


ori_tc_path = './ori_tcs/test_work_tcs/i32.add_0.wasm'
sec_template = _prepare_template(ori_tc_path)
ori_code_sec = bytearray(sec_template['code'])
# print_ba(ori_code_sec)
# print(hex(len(ori_code_sec)))
# func_num, offset = read_next_leb_num(ori_code_sec, offset=0)
# print(func_num)
# func1_len, offset = read_next_leb_num(ori_code_sec, offset=offset)
# print(hex(func1_len), offset)
# func_body = ori_code_sec[offset:func1_len + offset]
# print_ba(func_body)
# content_after_func1 = ori_code_sec[func1_len + offset:]
# print_ba(content_after_func1)

# before_func, func_body, content_after_func1 = first_func_info(ori_code_sec)
# print_ba(ori_code_sec)
# print_ba(before_func)
# print_ba(func_body)
# print_ba(content_after_func1)
rm_dir('v2')
check_dir('v2')
paths = generate_code_sec_tcs(ori_tc_path, mutate_num=5, new_tc_dir='./v2')