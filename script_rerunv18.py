from file_util import rm_dir
from run_dir_testing import test_and_analyze
from run_dir_testing import mutationParas
from pathlib import Path
from get_impls_util import get_std_impls
from get_impls_util import get_lastest_halfdump_impls


tested_dir = '/host_data/v18'


def _get_result_base_dir(additional_name):
    return f'/host_data/rerun/v18_{additional_name}'

def common_runner(result_base_dir, paras, impls):
    test_and_analyze(result_base_dir, paras, impls=impls)
    rm_dir(paras.tester_exec_paths.dumped_data_base_dir)
    rm_dir(paras.tester_exec_paths.tmp_data_dir)


class commonTuner:
    def __init__(self, repeat_num, start_num, dir_prefix, impls) -> None:
        self.repeat_num = repeat_num
        self.start_num = start_num
        self.dir_prefix = dir_prefix
        self.impls = impls

    def run(self):
        for num in range(self.repeat_num):
            num += self.start_num
            result_base_dir = _get_result_base_dir(f'{self.dir_prefix}_{num}')
            assert not Path(result_base_dir).exists(), print(result_base_dir)
            paras = self.get_mutator_paras_method(tested_dir=tested_dir, result_base_dir=result_base_dir, **self.unique_paras, impls=self.impls)
            common_runner(result_base_dir, paras, self.impls)


class logLimitMutationTuner(commonTuner):
    def __init__(self, repeat_num, start_num, dir_prefix, mutate_num, max_log_appear_num, impls) -> None:
        super().__init__(repeat_num, start_num, dir_prefix, impls)
        self.get_mutator_paras_method = mutationParas.get_random_byte_mutation_limit_by_log_paras
        self.unique_paras = {
            'mutate_num': mutate_num,
            'max_log_appear_num': max_log_appear_num,
            'reuse_no_mutation_info_dir': '/host_data/rerun/v18_no_mutation_info'
        }


def run_no_mutation(tested_dir):
    result_base_dir = _get_result_base_dir('detect_exception')
    impls = get_std_impls()
    paras = mutationParas.get_no_mutation_paras(result_base_dir, tested_dir, impls=impls)
    common_runner(result_base_dir, paras, impls)


if __name__ == '__main__':
    run_no_mutation(tested_dir='/host_data/rerun_to_analyze_log/except_dir')
    