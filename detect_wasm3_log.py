import os
from file_util import path_read, read_json
from file_util import save_json
from wasm_impls import common_runtime
from impl_paras import impl_paras
from pathlib import Path


def get_target_tc_names():
    data = read_json('./different_reason_back.json')
    target_tc_names = []
    for tc_name, reason in data.items():
        if 'wasm3' in reason:
            if 'CanDumpDifference' == reason[
                    'wasm3'] or 'CanDumpDifference' in reason['wasm3']:
                target_tc_names.append(tc_name)
    return target_tc_names


if __name__ == '__main__':
    name = 'wasm3_dump'
    wasm3 = common_runtime.from_dict(name, impl_paras[name])
    tc_names = get_target_tc_names()
    # print(tc_names)
    info_dict = {}
    for name in tc_names:
        # self.ori_log_path
        path = 'tcs/{}.wasm'.format(name)
        assert Path(path).exists()
        ori_cmd = wasm3.ori_cmd.format(path)
        dump_cmd = wasm3.cmd_format.format(path)
        # print(dump_cmd, wasm3.cmd_format)
        os.system(ori_cmd)
        assert Path(wasm3.ori_log_path).exists()
        ori_exec_info = path_read(wasm3.ori_log_path)
        os.system(dump_cmd)
        dump_exec_info = path_read(wasm3.ori_log_path)
        logs = [ori_exec_info, dump_exec_info]
        info_dict[name] = logs
    save_json('wasm3_exec_info.json', info_dict)
