import os
tc_name = 'f32.div_32'
tc_path = 'tcs/{}.wasm'.format(tc_name)
# tc_path = 'tcs/f32.ge_54.wasm'  # ???
# tc_name = 'i64.add_2'  # ???
# i32.rotl_98 # !!!
# f32.div_32 # ???
# f64.convert_i64_s_8 # ???
# f64.convert_i64_s_9 # ???
# f32.lt_18
# f32.div_79 ??
# f32.abs_6
# tc_path = 'f64.lt_16_m.wasm'  # wasmedge上dump不出global值
# tc_name = 'f32.abs_1' wasmedge没dump下来？
# tc_path = 'tcs/i32.rotl_98.wasm'
print('Wasmi-interp:')
cmd = '/home/zph/DGit/wasm_projects/runtime_test/ori_wasmi/target/debug/wasmi_cli {} to_test'.format(tc_path)
os.system(cmd)
print('-' * 50)
print('iwasm-interp-classic:')
cmd = '/home/zph/DGit/wasm_projects/runtime_test/ori_iwasm_interp_classic/product-mini/platforms/linux/build/iwasm --heap-size=0 -f to_test {}'.format(tc_path)
os.system(cmd)
print('-' * 50)
print('wasm3:')
cmd = '/home/zph/DGit/wasm_projects/runtime_test/ori_wasm3_default/build/wasm3 --func to_test {}'.format(tc_path)
os.system(cmd)
print('-' * 50)
print('wasmer:')
cmd = '/home/zph/DGit/wasm_projects/runtime_test/wasmer_default/target/release/wasmer run {} -i to_test '.format(tc_path)
os.system(cmd)
print('-' * 50)
print('wasmedge:')
cmd = '/home/zph/DGit/wasm_projects/runtime_test/ori_WasmEdge_disableAOT/build/tools/wasmedge/wasmedge --reactor {} to_test'.format(tc_path)
os.system(cmd)