
import subprocess


def wasm2wat(wasm_path, wat_path):
    cmd = 'wasm2wat {} -o {}'.format(wasm_path, wat_path)
    subprocess.run(cmd,timeout=20, shell=True)
