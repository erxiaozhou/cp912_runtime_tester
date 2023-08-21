from get_impls_util import get_std_uninst_impls
from get_impls_util import get_std_impls
from exec_util import exec_one_tc
from extract_dump import are_different
from pathlib import Path


uninst_impls = get_std_uninst_impls()
inst_impls = get_std_impls()

path_pattern = '/home/runtime_tester/tt/wasms_for_testing_exec_runtimes/i32add_in_me_v2_fig_{}.wasm'
ps = [path_pattern.format(i) for i in 'abcd']


p = ps[1]
assert Path(p).exists()
uninst_results = exec_one_tc(uninst_impls, p, 'tt/uninst_results', 'tt/uninst_results')
inst_results = exec_one_tc(inst_impls, p, 'tt/inst_results', 'tt/inst_results')

print(are_different(inst_results))
print(are_different(uninst_results))
# print(inst_results)
# for r in uninst_results:
#     print(r.name, '+' * 50)
#     print(r.log_has_failed_content)
#     print(r.log_content)

# print(p)

for p in ps:
    assert Path(p).exists()
    uninst_results = exec_one_tc(uninst_impls, p, 'tt/uninst_results', 'tt/uninst_results')
    inst_results = exec_one_tc(inst_impls, p, 'tt/inst_results', 'tt/inst_results')

    print(are_different(inst_results))
    print(are_different(uninst_results))
    print('=' * 50)

