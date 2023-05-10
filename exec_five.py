#!/home/zph/anaconda3/bin/python
import sys
from file_util import combine_path
from impl_paras import impl_paras
from pathlib import Path
from impl_paras_std import impl_paras_std
import subprocess
from get_imlps_util import get_std_uninst_imlps
from get_imlps_util import get_lastest_uninst_imlps
from wasm_impl_util import uninst_runtime
from extract_dump import is_failed_content


argv = sys.argv
assert len(argv) == 2
tc_path = argv[1]

std_uinst_impls = get_std_uninst_imlps()
lastest_uninst_imlps = get_lastest_uninst_imlps()
for imlp in std_uinst_impls:
    assert isinstance(imlp, uninst_runtime)
    print('===== {} ====='.format(imlp.name))
    cmd = imlp.cmd_fmt.format(tc_path)
    log = imlp.execute(tc_path)
    print(is_failed_content(log))

print('Lastest:', '-' * 30)

for imlp in lastest_uninst_imlps:
    assert isinstance(imlp, uninst_runtime)
    print('===== {} ====='.format(imlp.name))
    cmd = imlp.cmd_fmt.format(tc_path)
    imlp.execute(tc_path)
    print(is_failed_content(log))
