from exec_util import exec_one_tc
from exec_util import exec_one_tc_mth
from get_impls_util import get_std_uninst_impls
from get_impls_util import get_std_impls
from get_impls_util import get_lastest_uninst_impls
from get_impls_util import get_lastest_halfdump_impls
from extract_dump import are_different
import pytest


def get_wasms():
    path_pattern = './tests/testing_data/mv_wasms_testing_run_impls/i32add_in_me_v2_fig_{}.wasm'
    ps = [path_pattern.format(i) for i in 'abcd']
    ps.append('./tests/testing_data/i32_store_sample.wasm')
    return ps

expected_inst_runtime_results = [
    {'wasm3_dump': ['CanExecute']},
    False,
    {'iwasm_classic_interp_dump': ['CanExecute', 'stack_bytes_process_nan'], 'iwasm_fast_interp_dump': ['CanExecute', 'stack_bytes_process_nan']},
    {'WasmEdge_disableAOT_newer': ['CanExecute']},
    False
]


expected_uninst_runtime_results = [
    {'wasm3_dump': ['CanExecute']},
    False,
    {'iwasm_classic_interp_dump': ['CanExecute'], 'iwasm_fast_interp_dump': ['CanExecute']},
    {'WasmEdge_disableAOT_newer': ['CanExecute']},
    False
]


expected_inst_runtime_results_lastest = [
    {'wasm3_dump': ['CanExecute']},
    False,
    False,
    False,
    False
]


expected_uninst_runtime_results_lastest = [
    {'wasm3_dump': ['CanExecute']},
    False,
    False,
    False,
    False
]

def std_results(result):
    if result is False:
        return False
    else:
        assert isinstance(result, dict)
        return {k: set(v) for k, v in result.items()}

@pytest.mark.parametrize('wasm_path, expected_result', zip(get_wasms(), expected_inst_runtime_results))
def test_inst_runtime_no_mth(wasm_path, expected_result):
    impls = get_std_impls()
    results = _get_no_mth_result_core(impls, wasm_path)
    std_different_result = std_results(are_different(results))
    std_expected_result = std_results(expected_result)
    assert std_different_result == std_expected_result


@pytest.mark.parametrize('wasm_path, expected_result', zip(get_wasms(), expected_inst_runtime_results))
def test_inst_runtime_mth(wasm_path, expected_result):
    impls = get_std_impls()
    results = _get_mth_result_core(impls, wasm_path)
    std_different_result = std_results(are_different(results))
    std_expected_result = std_results(expected_result)
    assert std_different_result == std_expected_result


@pytest.mark.parametrize('wasm_path, expected_result', zip(get_wasms(), expected_uninst_runtime_results))
def test_uninst_runtime_no_mth(wasm_path, expected_result):
    impls = get_std_uninst_impls()
    results = _get_no_mth_result_core(impls, wasm_path)
    std_different_result = std_results(are_different(results))
    std_expected_result = std_results(expected_result)
    assert std_different_result == std_expected_result


@pytest.mark.parametrize('wasm_path, expected_result', zip(get_wasms(), expected_uninst_runtime_results))
def test_uninst_runtime_mth(wasm_path, expected_result):
    impls = get_std_uninst_impls()
    results = _get_mth_result_core(impls, wasm_path)
    std_different_result = std_results(are_different(results))
    std_expected_result = std_results(expected_result)
    assert std_different_result == std_expected_result



@pytest.mark.parametrize('wasm_path, expected_result', zip(get_wasms(), expected_uninst_runtime_results_lastest))
def test_uninst_runtime_no_mth_lastest(wasm_path, expected_result):
    impls = get_lastest_uninst_impls()
    results = _get_no_mth_result_core(impls, wasm_path)
    std_different_result = std_results(are_different(results))
    std_expected_result = std_results(expected_result)
    assert std_different_result == std_expected_result



@pytest.mark.parametrize('wasm_path, expected_result', zip(get_wasms(), expected_inst_runtime_results_lastest))
def test_inst_runtime_no_mth_lastest(wasm_path, expected_result):
    impls = get_lastest_halfdump_impls()
    results = _get_no_mth_result_core(impls, wasm_path)
    std_different_result = std_results(are_different(results))
    std_expected_result = std_results(expected_result)
    assert std_different_result == std_expected_result


@pytest.mark.parametrize('wasm_path, expected_result', zip(get_wasms(), expected_uninst_runtime_results_lastest))
def test_uninst_runtime_mth_lastest(wasm_path, expected_result):
    impls = get_lastest_uninst_impls()
    results = _get_mth_result_core(impls, wasm_path)
    std_different_result = std_results(are_different(results))
    std_expected_result = std_results(expected_result)
    assert std_different_result == std_expected_result

@pytest.mark.parametrize('wasm_path, expected_result', zip(get_wasms(), expected_inst_runtime_results_lastest))
def test_inst_runtime_mth_lastest(wasm_path, expected_result):
    impls = get_lastest_halfdump_impls()
    results = _get_mth_result_core(impls, wasm_path)
    std_different_result = std_results(are_different(results))
    std_expected_result = std_results(expected_result)
    assert std_different_result == std_expected_result

# ref_v128_tcs = [
#     '/home/runtime_tester/tests/testing_data/ref_null.wasm',
#     '/home/runtime_tester/tests/testing_data/v128_const.wasm',
# ]

# uninst_expected_results = [
#     {'wasm3_dump': ['CannotExecute']},
#     {'wasm3_dump': ['CannotExecute']}
# ]

# @pytest.mark.parametrize('wasm_path, expected_result', zip(ref_v128_tcs, uninst_expected_results))
# def test_uninst_runtimes_mtx_lastest_on_ref_v128(wasm_path, expected_result):
#     impls = get_lastest_uninst_impls()
#     results = _get_mth_result_core(impls, wasm_path)
#     std_different_result = std_results(are_different(results))
#     std_expected_result = std_results(expected_result)
#     assert std_different_result == std_expected_result


def _get_no_mth_result_core(impls, wasm_path):
    results = exec_one_tc(impls, wasm_path, 'tt/testing_inst_results', 'tt/testing_inst_results')
    return results


def _get_mth_result_core(impls, wasm_path):
    results = exec_one_tc_mth(impls, wasm_path, 'tt/testing_inst_results', 'tt/testing_inst_results')
    return results
