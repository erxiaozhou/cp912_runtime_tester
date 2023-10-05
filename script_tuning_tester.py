from file_util import rm_dir
from run_dir_testing import test_and_analyze
from run_dir_testing import mutationParas
from pathlib import Path
from get_impls_util import get_std_impls
from get_impls_util import get_lastest_halfdump_impls


tested_dir = './ori_tcs/v18.1_subset_v2'


def _get_result_base_dir(additional_name):
    return f'/host_data/tuning/v18.1_subsetv2_{additional_name}'

def common_runner(result_base_dir, paras, impls):
    test_and_analyze(result_base_dir, paras, impls=impls)
    rm_dir(paras.tester_exec_paths.dumped_data_base_dir)
    rm_dir(paras.tester_exec_paths.tmp_data_dir)


class commonTuner:
    def __init__(self, repeat_num, dir_prefix, impls) -> None:
        self.repeat_num = repeat_num
        self.dir_prefix = dir_prefix
        self.impls = impls

    def run(self):
        for num in range(self.repeat_num):
            result_base_dir = _get_result_base_dir(f'{self.dir_prefix}_{num}')
            assert not Path(result_base_dir).exists()
            paras = self.get_mutator_paras_method(tested_dir=tested_dir, result_base_dir=result_base_dir, **self.unique_paras, impls=self.impls)
            common_runner(result_base_dir, paras, self.impls)

class rawMutationTuner(commonTuner):
    def __init__(self, repeat_num, dir_prefix, one_tc_limit, mutate_num, mutate_prob, impls) -> None:
        super().__init__(repeat_num, dir_prefix, impls)
        self.get_mutator_paras_method = mutationParas.get_paras_with_mutation
        self.unique_paras = {
            'one_tc_limit': one_tc_limit,
            'mutate_num': mutate_num,
            'mutate_prob': mutate_prob
        }


class logLimitMutationTuner(commonTuner):
    def __init__(self, repeat_num, dir_prefix, mutate_num, max_log_appear_num, impls) -> None:
        super().__init__(repeat_num, dir_prefix, impls)
        self.get_mutator_paras_method = mutationParas.get_random_byte_mutation_limit_by_log_paras
        self.unique_paras = {
            'mutate_num': mutate_num,
            'max_log_appear_num': max_log_appear_num
        }


def run_no_mutation():
    result_base_dir = _get_result_base_dir('no_mutation')
    impls = get_std_impls()
    paras = mutationParas.get_no_mutation_paras(result_base_dir, tested_dir, impls=impls)
    common_runner(result_base_dir, paras, impls)
    
def run_no_mutation_lastest():
    result_base_dir = _get_result_base_dir('no_mutation_lastest')
    impls = get_lastest_halfdump_impls()
    paras = mutationParas.get_no_mutation_paras(result_base_dir, tested_dir, impls=impls)
    common_runner(result_base_dir, paras, impls)

def run_raw_mutation_config1(repeat_num=1):
    impls = get_std_impls()
    rawMutationTuner(repeat_num, 'raw_mutation1', 4, 2, 0.9, impls).run()

def run_raw_mutation_config2(repeat_num=1):
    impls = get_std_impls()
    rawMutationTuner(repeat_num, 'raw_mutation2', 50, 5, 1, impls).run()

def run_raw_mutation_config3(repeat_num=1):
    impls = get_std_impls()
    rawMutationTuner(repeat_num, 'raw_mutation3', 50, 5, 0.8, impls).run()

def run_raw_mutation_config4(repeat_num=1):
    impls = get_std_impls()
    rawMutationTuner(repeat_num, 'raw_mutation4', 50, 5, 0.5, impls).run()

def run_raw_mutation_config5(repeat_num=1):
    impls = get_std_impls()
    rawMutationTuner(repeat_num, 'raw_mutation5', 50, 5, 0.2, impls).run()

def run_raw_mutation_config6(repeat_num=1):
    impls = get_std_impls()
    rawMutationTuner(repeat_num, 'raw_mutation5', 30, 3, 1, impls).run()

def run_limit_by_log_mutation_config1(repeat_num=1):
    impls = get_std_impls()
    logLimitMutationTuner(repeat_num, 'limit_by_log_mutation_v21', 3, 20, impls).run()

def run_limit_by_log_mutation_config2(repeat_num=1):
    impls = get_std_impls()
    logLimitMutationTuner(repeat_num, 'limit_by_log_mutation_v22', 5, 10, impls).run()

def run_limit_by_log_mutation_config3(repeat_num=1):
    impls = get_std_impls()
    logLimitMutationTuner(repeat_num, 'limit_by_log_mutation_v23', 10, 10, impls).run()

def run_limit_by_log_mutation_config4(repeat_num=1):
    impls = get_std_impls()
    logLimitMutationTuner(repeat_num, 'limit_by_log_mutation_v24', 20, 10, impls).run()

def run_limit_by_log_mutation_config5(repeat_num=1):
    impls = get_std_impls()
    logLimitMutationTuner(repeat_num, 'limit_by_log_mutation_v25', 20, 50, impls).run()


def run_limit_by_log_mutation_config1(repeat_num=1):
    impls = get_lastest_halfdump_impls()
    logLimitMutationTuner(repeat_num, 'limitByLogMutation_lastest1', 10, 10, impls).run()

def run_limit_by_log_mutation_config2(repeat_num=1):
    impls = get_lastest_halfdump_impls()
    impls = [impl for impl in impls if 'wasm3' not in impl.name]
    logLimitMutationTuner(repeat_num, 'limitByLogMutation_lastest2', 20, 20, impls).run()

if __name__ == '__main__':
    # run_limit_by_log_mutation_config9(5)
    run_limit_by_log_mutation_config2(3)
    