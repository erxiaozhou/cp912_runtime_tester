import os
tc_name = 'i64.add_2'  # ???
tc_path = 'tcs/{}.wasm'.format(tc_name)
# tc_path = 'tcs/f32.ge_54.wasm'  # ???
# tc_path = 'f64.lt_16_m.wasm'

print('Wasmi:')
cmd = '/home/zph/DGit/wasm_projects/wasmi/target/debug/wasmi_cli {} to_test'.format(tc_path)
os.system(cmd)
print('-' * 50)
print('iwasm:')
cmd = '/home/zph/DGit/wasm_projects/iwasm_projects/wmrm_911/product-mini/platforms/linux/build/iwasm --heap-size=0 -f to_test {}'.format(tc_path)
os.system(cmd)
print('-' * 50)
print('wasm3:')
cmd = '/home/zph/DGit/wasm_projects/runtime_test/wasm3/build/wasm3 --func to_test {}'.format(tc_path)
os.system(cmd)
print('-' * 50)
print('wasmer:')
cmd = '/home/zph/DGit/wasm_projects/runtime_test/wasmer/target/debug/wasmer run {} -i to_test '.format(tc_path)
os.system(cmd)
print('-' * 50)
print('wasmedge:')
cmd = '/home/zph/DGit/wasm_projects/runtime_test/WasmEdge/build/tools/wasmedge/wasmedge --reactor {} to_test'.format(tc_path)
os.system(cmd)