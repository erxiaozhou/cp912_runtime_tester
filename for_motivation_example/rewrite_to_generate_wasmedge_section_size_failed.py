from file_util import read_bytes, write_bytes


'''
/media/ssd_wd1/cp910_data/only_i32_add_550_9811/diff_tcs/i32.add_415_0_16808518827913826.wasm: 22: [
    '0x1', '0x13', '0x4', '0x1', '0x7f', '0x1', '0x7d', '0x1', '0x7e', '0x1', '0x7c', 
    '0x41', '0x9e', '0xf1', '0xcd', '0xec', '0x7c', 
    '0x41', '0xf8', '0x0', 
    '0x6a', '0xb']
/home/zph/DGit/wasm_projects/runtime_tester/ori_tcs/only_i32_add/tcs/i32.add_415.wasm: 21: [
    '0x1', '0x13', '0x4', '0x1', '0x7f', '0x1', '0x7d', '0x1', '0x7e', '0x1', '0x7c', 
    '0x41', '0x9e', '0xf1', '0xcd', '0xec', '0x7c', 
    '0x41', '0x0', 
    '0x6a', '0xb']
'''


def rewrite():
    ori_file_name = '/home/zph/DGit/wasm_projects/runtime_tester/for_motivation_example/i32add_in_me_v2_fig_b.wasm'
    tgt_file_name = '/home/zph/DGit/wasm_projects/runtime_tester/for_motivation_example/i32add_in_me_v2_fig_d.wasm'
    bs = read_bytes(ori_file_name)
    pre_SEC = bs[:0X32]
    post_SEC = bs[0X32:]
    new_sec = pre_SEC +bytearray([0xc7]) + post_SEC
    # new_sec = pre_SEC + post_SEC
    write_bytes(tgt_file_name, new_sec)
