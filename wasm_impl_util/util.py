from file_util import byte2str
import subprocess


def exec_impl_and_collect_log(cmd_fmt, timeout_th, wasm_path, err_channel):
    assert err_channel in ['stdout', 'stderr']
    has_timeout = False
    cmd = cmd_fmt.format(wasm_path)
    try:
        p = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, timeout=timeout_th)
        err_byte_content = byte2str(p.stderr).strip(' \n\t')
        if err_channel == 'stdout':
            content = byte2str(p.stdout).strip(' \n\t')
            if len(err_byte_content):
                content += '\n' + err_byte_content
        else:
            content = err_byte_content
    except subprocess.TimeoutExpired:
        has_timeout = True
        content = ''
    return has_timeout, content