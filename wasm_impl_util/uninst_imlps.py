from file_util import combine_path
from file_util import byte2str
import subprocess


class uninst_runtime:
    def __init__(self, name, cmd_fmt, err_channel) -> None:
        assert err_channel in ['stdout', 'stderr']
        self.name = name
        self.cmd_fmt = cmd_fmt
        self.err_channel = err_channel

    def execute(self, wasm_path):
        cmd = self.cmd_fmt.format(wasm_path)
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        out_byte_content = byte2str(p.stdout.read()).strip(' \n\t')
        err_byte_content = byte2str(p.stderr.read()).strip(' \n\t')
        if self.err_channel == 'stdout':
            content = out_byte_content
            if len(err_byte_content):
                content += '\n' + err_byte_content
        else:
            content = err_byte_content
        return content
    
    @classmethod
    def from_std_dict(cls, name, dict_):
        cmd_fmt, err_channel = _get_paras_from_dict(dict_, 'standard_dir')
        return cls(name, cmd_fmt, err_channel)
    
    @classmethod
    def from_lastest_dict(cls, name, dict_):
        cmd_fmt, err_channel = _get_paras_from_dict(dict_, 'lastest_dir')
        return cls(name, cmd_fmt, err_channel)


def _get_paras_from_dict(dict_, runtime_dir_name):
    assert runtime_dir_name in ['standard_dir', 'lastest_dir']
    bin_path = combine_path(dict_[runtime_dir_name], dict_['bin_relative_path'])
    cmd_fmt = dict_['cmd'].format(bin_path, '{}')
    err_channel = detect_channel(dict_['dump_cmd'])
    return cmd_fmt, err_channel


def detect_channel(dump_cmd):
    if ' 2>' in dump_cmd:
        err_channel = 'stderr'
    else:
        assert ' >' in dump_cmd
        err_channel = 'stdout'
    return err_channel
