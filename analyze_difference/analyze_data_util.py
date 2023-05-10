from debug_util import get_log_by_impl
from file_util import path_read
from .std_exec_get_log import get_logs
from .util import get_illegal_opcode, get_tc_paths, get_illegal_type
from .util import get_wasmer_illegal_opcode
from tqdm import tqdm
from debug_util import wasm2wat

class analyze_data:
    def __init__(self, path, key, tcs_base_dir):
        self.path = path
        assert isinstance(key, (str, list))
        self.key = key
        self.tcs_base_dir = tcs_base_dir
        self._tc_paths = None
        self._logs = None
    
    @property
    def tc_paths(self):
        if self._tc_paths is None:
            self._tc_paths = []
            if isinstance(self.key, str):
                self._tc_paths = get_tc_paths(self.path, self.key, self.tcs_base_dir)
            elif isinstance(self.key, list):
                for k in self.key:
                    self._tc_paths.extend(get_tc_paths(self.path, k, self.tcs_base_dir))
        return self._tc_paths

    def get_logs(self, process=False, use_lastest=False, keys=None):
        if self._logs is None:
            self._logs = get_logs(self.tc_paths, process=process, use_lastest=use_lastest, keys=keys)
        return self._logs

    @property
    def first_tc_path(self):
        return self.tc_paths[0]
    
    def print_first_tc_log(self, process=False, use_lastest=False):
        print('One example of the log:')
        logs = get_logs([self.first_tc_path], process=process, use_lastest=use_lastest)
        for k, v in logs.items():
            print(k, v)
            print('-----------------')
    
    def print_logs(self, process=False, use_lastest=False, keys=None):
        print('All logs:')
        print(get_logs(self.tc_paths, process=process, use_lastest=use_lastest, keys=keys))

    def illegal_iwasm_opcodes(self, runtime_name='iwasm_classic_interp_dump'):
        runtime_logs = self.get_logs()[runtime_name]
        illegal_opcodes = set([get_illegal_opcode(log) for log in runtime_logs])
        return illegal_opcodes

    def illegal_wasmer_opcodes(self):
        runtime_logs = self.get_logs()['wasmer_default_dump']
        illegal_opcodes = set([get_wasmer_illegal_opcode(log) for log in runtime_logs])
        return illegal_opcodes

    def illegal_wasmer_and_tcs(self):
        opcodes = {}
        for path in self.tc_paths:
            log = get_log_by_impl('wasmer_default_dump', path)
            opcode = get_wasmer_illegal_opcode(log)
            if opcode not in opcodes:
                opcodes[opcode] = []
            opcodes[opcode].append(path)
        return opcodes
        
    def illegal_iwasm_local_types(self, runtime_name='iwasm_classic_interp_dump'):
        runtime_logs = self.get_logs()[runtime_name]
        illegal_types = set([get_illegal_type(log) for log in runtime_logs])
        return illegal_types

    def check_call_0(self):
        for p in self.tc_paths:
            wasm2wat(p, 'tt/tt.wat')
            assert 'call 0'  in path_read('tt/tt.wat')

    # def get_wasmedge_lasted_illegal_opcode(self):
    #     illegal_opcodes = set()
    #     for p in tqdm(self.tc_paths):
    #         log = get_log_by_impl('wasmedge_lasted_dump', p)
    #         illegal_opcodes.add(get_wasmer_illegal_opcode(log))
    #     return illegal_opcodes