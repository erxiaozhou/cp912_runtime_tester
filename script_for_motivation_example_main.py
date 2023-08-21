from file_util import read_bytes, write_bytes
from for_motivation_example.main_debug import print_c5_case_log
from for_motivation_example.main_debug import analyze_wasmedge_section_size_mismatch
from for_motivation_example.rewrite_to_generate_wasmedge_section_size_failed import rewrite
from debug_util import is_executable_by_impl


def generate_tc(insert_num):
    ori_file_name = './for_motivation_example/i32add_in_me_v2_fig_b.wasm'
    tgt_file_name = './for_motivation_example/i32add_in_me_v2_fig_d.wasm'
    bs = read_bytes(ori_file_name)
    pre_SEC = bs[:0X34]
    post_SEC = bs[0X34:]
    new_sec = pre_SEC +bytearray([insert_num]) + post_SEC
    # new_sec = pre_SEC + post_SEC
    write_bytes(tgt_file_name, new_sec)
    return tgt_file_name

if __name__ == '__main__':
    # print_c5_case_log()
    # analyze_wasmedge_section_size_mismatch()
    # rewrite()
    for i in range(256):
        tc_path = generate_tc(i)
        if is_executable_by_impl('WasmEdge_disableAOT_newer',tc_path):
            print(i, 'is executable')
            break

