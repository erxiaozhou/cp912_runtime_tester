from pathlib import Path


class imlp_result_path_group:
    def __init__(self, tgt_log_path, tgt_vstack_path, tgt_store_path, tgt_inst_path):
        self.log_path = tgt_log_path
        self.vstack_path = tgt_vstack_path
        self.store_path = tgt_store_path
        self.inst_path = tgt_inst_path
    
    @property
    def paths(self):
        return [
            self.log_path,
            self.store_path,
            self.vstack_path
        ]


class imlp_ori_path_group:
    def __init__(self, ori_store_path, ori_vstack_path, ori_inst_path):
        self.store_path = ori_store_path
        self.vstack_path = ori_vstack_path
        self.inst_path = ori_inst_path
    
    @property
    def paths(self):
        return [
            self.store_path,
            self.vstack_path,
            self.inst_path
        ]


class tester_exec_paths:
    def __init__(self, new_tc_dir, dumped_data_base_dir, diff_tc_dir, except_dir, config_log_path, reason_dir):
        self.new_tc_dir = new_tc_dir
        self.dumped_data_base_dir = dumped_data_base_dir
        self.diff_tc_dir = diff_tc_dir
        self.except_dir = except_dir
        self.config_log_path = config_log_path
        self.reason_dir = reason_dir
    
    @property
    def to_dict(self):
        return {
            'new_tc_dir': self.new_tc_dir,
            'dumped_data_base_dir': self.dumped_data_base_dir,
            'diff_tc_dir': self.diff_tc_dir,
            'except_dir': self.except_dir,
            'config_log_path': self.config_log_path,
            'reason_dir': self.reason_dir
        }
    
    @classmethod
    def from_result_base_dir(cls, result_base_dir):
        result_base_dir = Path(result_base_dir)
        paths = {
            'new_tc_dir': result_base_dir / 'test_std_new_tcs',  # 生成的所有 test case
            'dumped_data_base_dir': result_base_dir / 'dumped_data',  # 有difference的数据， pkl, log什么的
            'diff_tc_dir': result_base_dir / 'diff_tcs',  # 有difference 的tc
            'except_dir': result_base_dir / 'except_dir',
            'config_log_path': result_base_dir / 'config_log.json',
            'reason_dir': result_base_dir / 'reasons',
        }
        return cls(**paths)