#!/home/zph/anaconda3/bin/python
import sys
from get_impls_util import get_std_uninst_impls
from get_impls_util import get_lastest_uninst_impls
from wasm_impl_util import uninstRuntime
from extract_dump import is_failed_content


argv = sys.argv
assert len(argv) == 2
tc_path = argv[1]

std_uinst_impls = get_std_uninst_impls()
lastest_uninst_impls = get_lastest_uninst_impls()
for impl in std_uinst_impls:
    assert isinstance(impl, uninstRuntime)
    print('===== {} ====='.format(impl.name))
    cmd = impl.cmd_fmt.format(tc_path)
    log = impl.execute_and_collect_txt(tc_path)
    print(is_failed_content(log))

print('Lastest:', '-' * 30)

for impl in lastest_uninst_impls:
    assert isinstance(impl, uninstRuntime)
    print('===== {} ====='.format(impl.name))
    cmd = impl.cmd_fmt.format(tc_path)
    impl.execute_and_collect_txt(tc_path)
    print(is_failed_content(log))
