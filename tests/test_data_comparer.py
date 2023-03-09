import pytest
from exec_util import load_results_from_one_tc_result
from data_comparer import _get_can_execute_num
from data_comparer import _get_can_init_num


paras = [
    ['./tests/f32.abs_10', 1, 7]
]


@pytest.mark.parametrize('tc_result_dir, num, result_num', paras)
def test_get_can_execute_num(tc_result_dir, num, result_num):
    results = load_results_from_one_tc_result(tc_result_dir)
    assert len(results) ==  result_num
    assert _get_can_execute_num(results) == num
    # TODO 
    # assert _get_can_init_num(results) == 7
