from extract_dump import are_different
from extract_dump import at_least_one_can_instantiate
from exec_util import exec_one_tc_mth
from file_util import check_dir, cp_file, rm_dir, save_json
from .tester_util import testerExecInfo
from .tester_util import testerExecPaths

from generate_tcs_by_mutation_util import generate_tcs_by_mutate_bytes
from random import random
from file_util import remove_file_without_exception
from pathlib import Path
from abc import abstractclassmethod


class Tester:
    @abstractclassmethod
    def run_testing(self):
        pass

    def _common_brief_info(self, **kwads):
        paras_parts = [f"<{k}:{v}>" for k, v in kwads.items()]
        paras_part = ' '.join(paras_parts)
        return f'{self.__class__.__name__} {paras_part}'


class noMutationTester(Tester):
    def __init__(self):
        pass

    def run_testing(self, exec_paths, impls, tc_paths_iterator):
        # TODO 其实对exec_paths的类型设定有点宽，可以设定的更紧密点
        assert isinstance(exec_paths, testerExecPaths)
        para_paths = noMutationTestingPaths.from_testerExecPaths(exec_paths)
        exec_info = testing_without_mutation(para_paths, impls, tc_paths_iterator)
        return exec_info
    
    def __repr__(self):
        return self._common_brief_info()


def testing_without_mutation(exec_paths, impls, tc_paths_iterator):
    # TODO tc_paths_iterator 或许要换写法比较好
    # testing_without_mutation_and_collect_can_init_tc 有很多重复的代码，可以把主要的逻辑放进 noMutationTester
    # 然后，用类去收集一些想要的信息
    exec_info = testerExecInfo()
    for tc_name, tc_path in tc_paths_iterator:
        try:
            exec_info.ori_tc_num += 1
            tc_dumped_data_dir = check_dir(exec_paths.dumped_data_base_dir / tc_name)
            can_instantiate_, difference_reason = test_one_tc(tc_dumped_data_dir, impls, tc_path)
            exec_info.all_exec_times += 1
            if can_instantiate_:
                exec_info.at_least_one_to_analyze += 1
            post_process_arrording_to_diff_reason(exec_paths, tc_dumped_data_dir, exec_info, tc_path, tc_name, difference_reason)
        except (RuntimeError, Exception) as e:
            cp_file(tc_path, exec_paths.except_dir)
    return exec_info


def testing_without_mutation_and_collect_can_init_tc(exec_paths, impls, tc_paths_iterator):
    exec_info = testerExecInfo()
    can_init_tc_paths = []
    for tc_name, tc_path in tc_paths_iterator:
        try:
            exec_info.ori_tc_num += 1
            tc_dumped_data_dir = check_dir(exec_paths.dumped_data_base_dir / tc_name)
            can_instantiate_, difference_reason = test_one_tc(tc_dumped_data_dir, impls, tc_path)
            exec_info.all_exec_times += 1
            if can_instantiate_:
                exec_info.at_least_one_to_analyze += 1
                can_init_tc_paths.append(tc_path)
            post_process_arrording_to_diff_reason(exec_paths, tc_dumped_data_dir, exec_info, tc_path, tc_name, difference_reason)
        except (RuntimeError, Exception) as e:
            # raise e
            cp_file(tc_path, exec_paths.except_dir)
    return exec_info, can_init_tc_paths


class noMutationTestingPaths:
    def __init__(self, dumped_data_base_dir, diff_tc_dir, reason_dir, except_dir):
        self.dumped_data_base_dir = dumped_data_base_dir
        self.diff_tc_dir = diff_tc_dir
        self.reason_dir = reason_dir
        self.except_dir = except_dir
    
    @classmethod
    def from_testerExecPaths(cls, tester_exec_paths):
        return cls(tester_exec_paths.dumped_data_base_dir, tester_exec_paths.diff_tc_dir, tester_exec_paths.reason_dir, tester_exec_paths.except_dir)


class randomByteMutationTester(Tester):
    def __init__(self, one_tc_limit=50, mutate_num=5, mutate_prob=1) -> None:
        '''
        1. 首先获取原 tcs 中所有能运行的 tc (后面称为 ori_seeds)， 每个 tc 都会以 mutate_prob 的 概率被 mutate
        2. mutation次数限制 ： ori_seeds中每个 tc 及基于其生成的 tc 最多被 mutate one_tc_limit 次(实际代码上不是，而是可能略有不同，这个好改，暂时不改)；每个 tc 最多被 mutate_num 次
        '''
        self.one_tc_limit = one_tc_limit
        self.mutate_num = mutate_num
        # ! mutate_prob 的名字，默认值都要改
        self.mutate_prob = mutate_prob
    
    def run_testing(self, exec_paths, impls, tc_paths_iterator):
        exec_info, can_init_tc_paths = testing_without_mutation_and_collect_can_init_tc(exec_paths, impls, tc_paths_iterator)
        exec_info.mutation_ori_tc_num = len(can_init_tc_paths)
        for ori_seed in can_init_tc_paths:
            self.cur_seed_mutant_num = 0
            self.possible_m = []
            if random() < self.mutate_prob:
                self.mutate_and_update_log(exec_paths, exec_info, ori_seed)
            while self.possible_m:
                # assert 0, print(self.possible_m)
                try:
                    tc_path = self.possible_m.pop()
                    tc_name = Path(tc_path).stem
                    # print(self.possible_m)
                    tc_dumped_data_dir = check_dir(exec_paths.dumped_data_base_dir / tc_name)
                    can_instantiate_, difference_reason = test_one_tc(tc_dumped_data_dir, impls,tc_path)
                    if can_instantiate_:
                        exec_info.at_least_one_to_analyze += 1
                    if self._need_mutate(can_instantiate_):
                        self.mutate_and_update_log(exec_paths, exec_info, tc_path)

                    post_process_arrording_to_diff_reason(exec_paths, tc_dumped_data_dir, exec_info, tc_path, tc_name, difference_reason)
                    # assert Path(tc_path).is_relative_to(exec_paths.new_tc_dir)
                    # assert Path(tc_path).is_relative_to(exec_paths.new_tc_dir)
                    assert Path(tc_path).parent == exec_paths.new_tc_dir
                    remove_file_without_exception(tc_path)
                except (RuntimeError, Exception) as e:
                    raise e
                    cp_file(tc_path, exec_paths.except_dir)
        return exec_info
    
    def __repr__(self):
        return self._common_brief_info(**{
            'one_tc_limit': self.one_tc_limit,
            'mutate_num': self.mutate_num,
            'mutate_prob': self.mutate_prob
        })

    def mutate_and_update_log(self, exec_paths, exec_info, tc_path):
        self.cur_seed_mutant_num += self.mutate_num
        self.possible_m.extend(self.generate_tcs(tc_path, exec_paths.new_tc_dir))
        exec_info.mutation_times += self.mutate_num
    
    def generate_tcs(self, ori_tc, new_tc_dir):
        return generate_tcs_by_mutate_bytes(ori_tc, self.mutate_num, new_tc_dir)

    def _need_mutate(self, can_instantiate_):
        if can_instantiate_:
            if self.one_tc_limit > self.cur_seed_mutant_num:
                return True
        return False


def test_one_tc(tc_dumped_data_dir, impls, tc_path):
    print(tc_path)
    dumped_results = exec_one_tc_mth(impls, tc_path, tc_dumped_data_dir, tc_dumped_data_dir)
    difference_reason = are_different(dumped_results)
    return at_least_one_can_instantiate(dumped_results), difference_reason


def post_process_arrording_to_diff_reason(exec_paths, tc_dumped_data_dir, exec_info, tc_path, tc_name, difference_reason):
    if difference_reason:
        exec_info.difference_num += 1
        cp_file(tc_path, exec_paths.diff_tc_dir)
        json_path = exec_paths.reason_dir / f'{tc_name}.json'
        save_json(json_path, difference_reason)
    else:
        rm_dir(tc_dumped_data_dir)
