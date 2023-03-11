class result_path_group:
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


class ori_path_group:
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
