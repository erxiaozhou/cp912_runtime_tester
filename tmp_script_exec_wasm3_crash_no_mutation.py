from get_impls_util import get_std_impls
from run_dir_testing import test_and_analyze
from run_dir_testing import mutationParas
from pathlib import Path
from file_util import check_dir, read_json
from file_util import cp_file


if __name__ == '__main__':
    json_path = 'tt/v18_340_9811_0810_test_std_new_tcs_wasm3_crash.json'
    tgt_dir = check_dir('/host_data/wasm3_crash_tcs')
    for p in read_json(json_path):
        p = Path(p)
        name = p.name
        new_p = tgt_dir / name
        cp_file(p, new_p)


    tested_dir = tgt_dir
    result_base_dir = '/host_data/wasm3_crash_analysis'
    impls = get_std_impls()
    paras = mutationParas.get_no_mutation_paras(result_base_dir, tested_dir, impls=impls)
    test_and_analyze(result_base_dir, paras, impls=impls)
