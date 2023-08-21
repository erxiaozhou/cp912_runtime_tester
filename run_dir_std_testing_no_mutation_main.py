from get_impls_util import get_std_impls
from run_dir_testing import test_and_analyze
from run_dir_testing import mutationParas


if __name__ == '__main__':
    tested_dir = './ori_tcs/v18.1_subset'
    result_base_dir = '/host_data/tmp_v18.1_subset_no_mutation'
    tested_dir = '/home/spec/extract_document/generated_tcs/select_1C/tcs'
    result_base_dir = '/host_data/select_1C_no_mutation/'
    tested_dir = '/home/spec/extract_document/generated_tcs/v18_rewrite/tcs'
    result_base_dir = '/host_data/rewrite/v18_no_mutation'
    tested_dir = '/home/spec/extract_document/generated_tcs/v19.1/tcs'
    result_base_dir = '/host_data/rewrite/v19.1_no_mutation'
    tested_dir = '/home/spec/extract_document/generated_tcs/v19.2/tcs'
    result_base_dir = '/host_data/rewrite/v19.2_no_mutation'
    # tested_dir = '/host_data/rewrite/v19.1_no_mutation/except_dir'
    # result_base_dir = '/host_data/rewrite/debug'
    tested_dir = '/home/spec/extract_document/generated_tcs/v19/tcs'
    result_base_dir = '/host_data/v19_no_mutation'
    impls = get_std_impls()
    paras = mutationParas.get_no_mutation_paras(result_base_dir, tested_dir, impls=impls)
    test_and_analyze(result_base_dir, paras, impls=impls)
