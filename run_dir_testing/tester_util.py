from pathlib import Path
from extract_dump import are_different
from exec_util import exec_one_tc_mth
from file_util import check_dir, cp_file, rm_dir, save_json


class testerExecPaths:
    def __init__(self, new_tc_dir, dumped_data_base_dir, diff_tc_dir, except_dir, config_log_path, reason_dir, tmp_data_dir, check_not_exist=True):
        # TODO 包含的路径有点多，其实可以继续拆分
        if check_not_exist:
            assert not Path(new_tc_dir).exists(), f'{new_tc_dir} already exists'
            assert not Path(dumped_data_base_dir).exists()
            assert not Path(diff_tc_dir).exists()
            assert not Path(except_dir).exists()
            assert not Path(config_log_path).exists()
            assert not Path(reason_dir).exists()
            assert not Path(tmp_data_dir).exists()

        self.new_tc_dir = check_dir(new_tc_dir)
        self.dumped_data_base_dir = check_dir(dumped_data_base_dir)
        self.diff_tc_dir = check_dir(diff_tc_dir)
        self.except_dir = check_dir(except_dir)
        self.config_log_path = config_log_path
        self.reason_dir = check_dir(reason_dir)
        self.tmp_data_dir = check_dir(tmp_data_dir)
    
    @property
    def to_dict(self):
        return self.__dict__
    
    @property
    def to_str_dict(self):
        return {k: str(v) for k, v in self.to_dict.items()}

    @classmethod
    def from_result_base_dir(cls, result_base_dir, check_not_exist=True):
        result_base_dir = Path(result_base_dir)
        paras = {
            'new_tc_dir': result_base_dir / 'test_std_new_tcs',  # 生成的所有 test case
            'dumped_data_base_dir': result_base_dir / 'dumped_data',  # 有difference的数据， pkl, log什么的
            'diff_tc_dir': result_base_dir / 'diff_tcs',  # 有difference 的tc
            'except_dir': result_base_dir / 'except_dir',
            'config_log_path': result_base_dir / 'config_log.json',
            'reason_dir': result_base_dir / 'reasons',
            'tmp_data_dir': result_base_dir / 'tmp_data',
            'check_not_exist': check_not_exist
        }
        return cls(**paras)


class testerExecInfo:
    def __init__(self) -> None:
        self.ori_tc_num = 0
        self.all_exec_times = 0
        self.at_least_one_to_analyze = 0
        self.difference_num = 0
        self.mutation_ori_tc_num = 0
        self.mutation_times = 0
        self.mean_mutation_on_one_ori_tc = 0

    @property
    def to_dict(self):
        if self.mutation_times == 0:
            self.mean_mutation_on_one_ori_tc = 0
        else:
            self.mean_mutation_on_one_ori_tc = self.mutation_times / self.mutation_ori_tc_num
        return self.__dict__
    
    @classmethod
    def from_dict(cls, d):
        exec_info = cls()
        exec_info.__dict__ = d
        return exec_info




def test_one_tc(tc_dumped_data_dir, impls, tc_path):
    # print(tc_path)
    dumped_results = exec_one_tc_mth(impls, tc_path, tc_dumped_data_dir, tc_dumped_data_dir)
    difference_reason = are_different(dumped_results)
    return dumped_results, difference_reason


def post_process_arrording_to_diff_reason(exec_paths, tc_dumped_data_dir, exec_info, tc_path, tc_name, difference_reason):
    if difference_reason:
        exec_info.difference_num += 1
        cp_file(tc_path, exec_paths.diff_tc_dir)
        json_path = exec_paths.reason_dir / f'{tc_name}.json'
        save_json(json_path, difference_reason)
    else:
        rm_dir(tc_dumped_data_dir)

