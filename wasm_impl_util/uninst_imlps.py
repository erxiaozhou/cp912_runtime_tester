from file_util import combine_path
from file_util import byte2str
import subprocess


class uninst_runtime:
    def __init__(self, name, cmd_fmt, err_channel) -> None:
        assert err_channel in ['stdout', 'stderr']
        self.name = name
        self.cmd_fmt = cmd_fmt
        self.err_channel = err_channel

    def execute(self, wasm_path, channel='stdout'):
        assert channel in ['stdout', 'stderr', None]
        cmd = self.cmd_fmt.format(wasm_path)
        try:
            p = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, timeout=10)
        except subprocess.TimeoutExpired:
            return 'Z exec : timeout'
        out_byte_content = byte2str(p.stdout).strip(' \n\t')
        err_byte_content = byte2str(p.stderr).strip(' \n\t')
        if channel is None:
            channel = self.err_channel
        if channel == 'stdout':
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
    if runtime_dir_name == 'standard_dir':
        cmd_fmt = dict_['std_cmd'].format(bin_path, '{}')
    else:
        cmd_fmt = dict_['lastest_cmd'].format(bin_path, '{}')
    err_channel = dict_['err_channel']
    assert err_channel in ['stdout', 'stderr']
    return cmd_fmt, err_channel
