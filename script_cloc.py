import subprocess
from pathlib import Path


def exec_cmd(e_dir, e_ext):
    e_dir_txt = ','.join(e_dir)
    e_ext_txt = ','.join(e_ext)
    cmd = 'cloc --exclude-dir={} --exclude-ext={} .'.format(e_dir_txt, e_ext_txt)
    subprocess.run(cmd, shell=True)
    return cmd

exculde_dir = [
    'results', 'tt', 'v1_main_script', 'ori_tcs', 'tt.py', 'test_one.py', 'script_compare_log_inv_file.py', 'run_five.py', 'run_one_tc_std_testing.py', 'impl_paras.py', 'tests', 'script_check_ori_tcs_executable.py', 'py_wasm2wat.py', 'debug_util', 'previous_code', 'for_motivation_example', 'script_for_motivation_example_main.py', 'final_findings', 'script_cloc.py', 'analyze_difference', 'analyze_difference_main.py', 'script_exec_five.py', 'special_tcs', 'useful_results', 'run_dir_std_testing_no_mutation_main.py', 'impl_paras_std_release.py'
]
exclude_ext = ['wasm', 'wat', 'json']

# tmp_*.py
tmp_fnames = [f.name for f in Path('.').glob('tmp_*.py')]
script_fnames = [f.name for f in Path('.').glob('script*.py')]
expended_exclude_dir = exculde_dir + tmp_fnames + script_fnames
analyze_result_dir = ['analyze_reslut_util', 'log_content_util', 'stack_val_analyze']


def stat_framework_cloc():
    exec_cmd(expended_exclude_dir+analyze_result_dir, exclude_ext)


def stat_all_cloc():
    exec_cmd(expended_exclude_dir, exclude_ext)


if __name__ == '__main__':
    stat_framework_cloc()
    print('-----------------')
    stat_all_cloc()
