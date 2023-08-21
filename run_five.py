import sys
import subprocess
from get_impls_util import get_std_uninst_impls
from get_impls_util import get_lastest_uninst_impls
from wasm_impl_util import uninstRuntime


argv = sys.argv
assert len(argv) == 2
tc_path = argv[1]

std_uinst_impls = get_std_uninst_impls(set_out2out_err=True)
for impl in std_uinst_impls:
    assert isinstance(impl, uninstRuntime)
    print('===== {} ====='.format(impl.name))
    txt = impl.execute_and_collect_txt(tc_path)
    r = impl.execute_and_collect(tc_path)
    print(r.has_crash, r.log_content)
