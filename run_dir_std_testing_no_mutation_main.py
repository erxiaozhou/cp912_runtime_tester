from run_dir_testing import test_and_analyze
from run_dir_testing import mutationParas
from path_group_util import analyzeResultDirs


if __name__ == '__main__':
    tested_dir = './ori_tcs/v18.1_subset'
    result_base_dir = '/host_data/tmp_v18.1_subset_no_mutation'
    analyze_paths = analyzeResultDirs(result_base_dir)
    paras = mutationParas.get_no_mutation_paras(result_base_dir, tested_dir)
    test_and_analyze(result_base_dir, analyze_paths, paras)
