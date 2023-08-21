from extract_dump import at_least_one_can_instantiate
from file_util import check_dir, cp_file, read_json, save_json
from .tester_util import testerExecInfo

from generate_tcs_by_mutation_util import generate_tcs_by_mutate_bytes
from file_util import remove_file_without_exception
from pathlib import Path
from log_content_util.get_key_util import rawRuntimeLogs, onlyInterestingRuntimeLogs
from .tester_util import test_one_tc
from .tester_util import post_process_arrording_to_diff_reason
from .tester import Tester
from collections import Counter


def testing_without_mutation_and_collect_can_init_tc_log_hash(exec_paths, impls, tc_paths_iterator):
    exec_info = testerExecInfo()
    can_init_tc_paths = []
    tc_path2hash = {}
    for tc_name, tc_path in tc_paths_iterator:
        try:
            exec_info.ori_tc_num += 1
            tc_dumped_data_dir = check_dir(exec_paths.dumped_data_base_dir / tc_name)
            dumped_results, difference_reason = test_one_tc(tc_dumped_data_dir, impls, tc_path)
            can_instantiate_ = at_least_one_can_instantiate(dumped_results)
            logs = onlyInterestingRuntimeLogs.from_dumped_results(dumped_results)
            
            exec_info.all_exec_times += 1
            if can_instantiate_:
                exec_info.at_least_one_to_analyze += 1
                can_init_tc_paths.append(tc_path)
                hash_ = hash(logs)
                tc_path2hash[tc_path] = hash_
            post_process_arrording_to_diff_reason(exec_paths, tc_dumped_data_dir, exec_info, tc_path, tc_name, difference_reason)
        except (RuntimeError, Exception) as e:
            raise e
            cp_file(tc_path, exec_paths.except_dir)
    return exec_info, can_init_tc_paths, tc_path2hash


class randomByteMutationLimitbyLogTester(Tester):
    def __init__(self, mutate_num=10, max_log_appear_num=10, reuse_no_mutation_info_dir=None) -> None:
        '''
        1. 首先获取原 tcs 中所有能运行的 tc (后面称为 ori_seeds)， 若该 tc (及基于其生成的tc) 所生成的log 在以往的测试中出现的次数小于 max_log_appear_num 都会被 mutate
        2. mutation次数限制 ： ori_seeds中每个 tc 及基于其生成的 tc 最多被 mutate 无限 次(实际代码上不是，而是可能略有不同，这个好改，暂时不改)；每个 tc 最多被 mutate_num 次

        这个方法约束的是被 有某样 log 的 tc 被 mutate 的次数；如果一种 log 出现了很多次，但被mutate的次数很少 ， 对应 tc 还是会被 mutate 
        '''
        self.mutate_num = mutate_num
        # ! mutate_prob 的名字，默认值都要改
        self.max_log_appear_num = max_log_appear_num
        self.reuse_no_mutation_info_dir = reuse_no_mutation_info_dir
    
    def run_testing(self, exec_paths, impls, tc_paths_iterator):
        print(f'self.mutate_num: {self.mutate_num}; self.max_log_appear_num: {self.max_log_appear_num}')
        #
        if self.reuse_no_mutation_info_dir is not None:
            self.reuse_no_mutation_info_dir = Path(self.reuse_no_mutation_info_dir)
            if self.reuse_no_mutation_info_dir.exists():
                exec_info = testerExecInfo.from_dict(read_json(self.reuse_no_mutation_info_dir/'exec_info.json'))
                can_init_tc_paths = read_json(self.reuse_no_mutation_info_dir/'can_init_tc_paths.json')
                tc_path2hash = read_json(self.reuse_no_mutation_info_dir/'tc_path2hash.json')
            else:
                exec_info, can_init_tc_paths, tc_path2hash = testing_without_mutation_and_collect_can_init_tc_log_hash(exec_paths, impls, tc_paths_iterator)
                self.reuse_no_mutation_info_dir.mkdir(parents=True)
                save_json(self.reuse_no_mutation_info_dir/'exec_info.json', exec_info.to_dict)
                save_json(self.reuse_no_mutation_info_dir/'can_init_tc_paths.json', can_init_tc_paths)
                save_json(self.reuse_no_mutation_info_dir/'tc_path2hash.json', tc_path2hash)
        else:
            exec_info, can_init_tc_paths, tc_path2hash = testing_without_mutation_and_collect_can_init_tc_log_hash(exec_paths, impls, tc_paths_iterator)
        # 
        exec_info.mutation_ori_tc_num = len(can_init_tc_paths)
        self.hash_counter = Counter()
        self.possible_seeds = can_init_tc_paths
        self.tc_path2hash = tc_path2hash

        while self.possible_seeds:
            tc_path = self.possible_seeds.pop()
            if tc_path in self.tc_path2hash:
                if self._tc_path_can_be_seed(tc_path):
                    self.mutate_and_update_log(exec_paths, exec_info, tc_path)
            else:
                tc_name = Path(tc_path).stem
                try:
                    tc_dumped_data_dir = check_dir(exec_paths.dumped_data_base_dir / tc_name)
                    dumped_results, difference_reason = test_one_tc(tc_dumped_data_dir, impls, tc_path)
                    can_instantiate_ = at_least_one_can_instantiate(dumped_results)
                    if can_instantiate_:
                        exec_info.at_least_one_to_analyze += 1
                    if can_instantiate_ and self._resultrs_can_be_seed(dumped_results):
                        self.mutate_and_update_log(exec_paths, exec_info, tc_path)

                    post_process_arrording_to_diff_reason(exec_paths, tc_dumped_data_dir, exec_info, tc_path, tc_name, difference_reason)
                    assert Path(tc_path).parent == exec_paths.new_tc_dir
                    remove_file_without_exception(tc_path)
                except (RuntimeError, Exception) as e:
                    # raise e
                    cp_file(tc_path, exec_paths.except_dir)
        return exec_info
    
    def __repr__(self):
        return self._common_brief_info(
            mutate_num =  self.mutate_num,
            max_log_appear_num = self.max_log_appear_num
        )

    def mutate_and_update_log(self, exec_paths, exec_info, tc_path):
        self.possible_seeds.extend(self.generate_tcs(tc_path, exec_paths.new_tc_dir))
        exec_info.mutation_times += self.mutate_num
    
    def generate_tcs(self, ori_tc, new_tc_dir):
        return generate_tcs_by_mutate_bytes(ori_tc, self.mutate_num, new_tc_dir)

    def _tc_path_can_be_seed(self, tc_path):
        hash_ = self.tc_path2hash[tc_path]
        if self.hash_counter[hash_] < self.max_log_appear_num:
            self.hash_counter[hash_] += 1
            print(f'1: self.hash_counter[hash_]: {self.hash_counter[hash_]}; len(self.hash_counter): {len(self.hash_counter)}')
            return True
        else:
            print(f'1: In false; len(self.hash_counter): {len(self.hash_counter)}')
            return False

    def _resultrs_can_be_seed(self, dumped_results):
        hash_ = hash(onlyInterestingRuntimeLogs.from_dumped_results(dumped_results))
        if self.hash_counter[hash_] < self.max_log_appear_num:
            self.hash_counter[hash_] += 1
            print(f'2: self.hash_counter[hash_]: {self.hash_counter[hash_]}; len(self.hash_counter): {len(self.hash_counter)}')
            return True
        else:
            print(f'2: In false; len(hash_counter): {len(self.hash_counter)}; len(possible_seeds)): {len(self.possible_seeds)}')
            return False
