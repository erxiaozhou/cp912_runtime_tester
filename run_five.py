#!/home/zph/anaconda3/bin/python
import sys
from file_util import combine_path
from impl_paras import impl_paras
from pathlib import Path
from impl_paras_std import impl_paras_std
import subprocess


argv = sys.argv
if len(argv) == 1:
    tc_name = 'f32.div_32'
    tc_path = 'tcs/{}.wasm'.format(tc_name)
else:
    tc_name = argv[1]
    if Path(tc_name).exists():
        tc_path = tc_name
    else:
        tc_path = 'tcs/{}.wasm'.format(tc_name)
# tc_path = 'new_tcs_M/i64.shr_u_5_0.wasm'
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

impl_paras = impl_paras_std
to_test_imlps = list(impl_paras.keys())
for imlp_name in to_test_imlps:
    print('===== {} ====='.format(imlp_name))
    dict_ = impl_paras[imlp_name]
    bin_path = combine_path(dict_['standard_dir'], dict_['bin_relative_path'])
    cmd = dict_['cmd'].format(bin_path, tc_path)

    try:
        subprocess.run(cmd,timeout=20, shell=True)
    except subprocess.TimeoutExpired:
        print('From pyth: timeout')
    # print(cmd)
