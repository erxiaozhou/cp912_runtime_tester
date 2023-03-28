from file_util import combine_path
import subprocess


class uninst_runtime:
    def __init__(self, name, cmd_fmt, err_channel) -> None:
        assert err_channel in ['stdout', 'stderr']
        self.name = name
        self.cmd_fmt = cmd_fmt
        self.err_channel = err_channel
    
    @classmethod
    def from_dict(cls, name, dict_):
        bin_path = combine_path(dict_['standard_dir'], dict_['bin_relative_path'])
        cmd_fmt = dict_['cmd'].format(bin_path, '{}')
        if ' 2>' in dict_['dump_cmd']:
            err_channel = 'stderr'
        else:
            assert ' >' in dict_['dump_cmd']
            err_channel = 'stdout'
        return cls(name, cmd_fmt, err_channel)

    def execute(self, wasm_path):
        cmd = self.cmd_fmt.format(wasm_path)
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        if self.err_channel == 'stdout':
            out_byte_content = p.stdout.read()
            try: 
                content = out_byte_content.decode()
            except Exception:
                content = str(out_byte_content)
        else:
            err_byte_content = p.stderr.read()
            assert self.err_channel == 'stderr'
            try: 
                content = err_byte_content.decode()
            except Exception:
                content = str(err_byte_content)
        return content
