from run_dir_testing import test_and_analyze
from run_dir_testing import mutationParas
from path_group_util import analyzeResultDirs


if __name__ == '__main__':
    # argv = sys.argv
    # reason_base_dir = argv[1]
    # tested_dir = argv[2]
    tested_dir = './ori_tcs/v18.1_subset'
    result_base_dir = '/host_data/tmp_v18.1_subset_mutation'
    # paras = mutationParas.get_paras_with_mutation(tested_dir, result_base_dir, one_tc_limit=40, mutate_num=3, mutate_prob=1.0, use_release=False)
    paras = mutationParas.get_paras_with_mutation(tested_dir, result_base_dir, one_tc_limit=4, mutate_num=2, mutate_prob=0.9, use_release=False)
    analyze_paths = analyzeResultDirs(result_base_dir)
    test_and_analyze(result_base_dir, analyze_paths, paras)
