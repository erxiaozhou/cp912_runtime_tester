import time
from pathlib import Path
from data_comparer import are_different, at_least_one_can_execute, at_least_one_can_execute, at_least_one_can_instantiate
from exec_util import exec_one_tc, exec_one_tc_mth
from file_util import check_dir, cp_file, get_time_string, remove_file_without_exception, rm_dir, save_json
from get_imlps_util import get_std_imlps
from generate_tcs_by_mutation_util import generate_tcs


def test_with_mutation(tested_dir, new_tc_dir, diff_tc_dir, dumped_data_base_dir, config_log_path, reason_dir, one_tc_limit = 6000, mutate_num = 60, except_dir='except_dir', skip_common_diff=False, add_mutation=True, check_result_dir_not_exist=True):
    imlps = get_std_imlps()
    if check_result_dir_not_exist:
        assert not Path(dumped_data_base_dir).parent.exists(), print(dumped_data_base_dir.parent)
        assert not Path(dumped_data_base_dir).exists(), print(dumped_data_base_dir)
    dumped_data_base_dir = check_dir(dumped_data_base_dir)
    new_tc_dir = check_dir(new_tc_dir)
    diff_tc_dir = check_dir(diff_tc_dir)
    tc_paths_iterator = _get_wasm_paths_iterator(tested_dir)
    except_tc_dir = check_dir(except_dir)
    reason_dir = check_dir(reason_dir)
    # tc execution info
    exec_info = {
        'ori_tc_num': 0,
        'all_exec_times': 0,
        'at_least_one_can_execute': 0, 
        'difference_num': 0,
        'mutation_ori_tc_num': 0,
        'mutation_times': 0,
        'mean_mutation_on_one_ori_tc': 0
    }
    assert isinstance(reason_dir, Path)
    start_time = time.time()
    for tc_name, tc_path in tc_paths_iterator:
        exec_info['ori_tc_num'] += 1
        possible_m = [tc_path]
        generated_tc_num = 0
        is_ori = True
        while possible_m:
            tc_path = possible_m.pop()
            tc_name = Path(tc_path).stem
            tc_dumped_data_dir = check_dir(dumped_data_base_dir / tc_name)
            try:
                print(tc_path)
                dumped_results = exec_one_tc_mth(imlps, tc_path, tc_dumped_data_dir, tc_dumped_data_dir)
                exec_info['all_exec_times'] += 1
                difference_reason = are_different(dumped_results)
                # ! 重新考虑 difference_reason 
                if at_least_one_can_instantiate(dumped_results):
                    exec_info['at_least_one_can_execute'] += 1
                    # print('add_mutation, one_tc_limit, generated_tc_num')
                    # print(add_mutation, one_tc_limit, generated_tc_num)
                    # assert 0
                    if add_mutation and (one_tc_limit > generated_tc_num):
                        # assert 0, print(tc_path, mutate_num, new_tc_dir)
                        paths = generate_tcs(tc_path, mutate_num, new_tc_dir)
                        # assert 0, print(paths)
                        generated_tc_num += mutate_num
                        possible_m.extend(paths)
                        exec_info['mutation_times'] += mutate_num
                        print(exec_info['mutation_times'])
                        if is_ori:
                            exec_info['mutation_ori_tc_num'] += 1
                            is_ori = False

                if difference_reason:
                    exec_info['difference_num'] += 1
                    cp_file(tc_path, diff_tc_dir)
                    json_file_name = ''.join((tc_name, '.json'))
                    json_path = reason_dir / json_file_name
                    save_json(json_path, difference_reason)
                else:
                    rm_dir(tc_dumped_data_dir)
                # * 这么做是假设tc_path不会再被用到
                if Path(tc_path).is_relative_to(new_tc_dir):
                    remove_file_without_exception(tc_path)
                
            except AssertionError as e:
                raise e
            except Exception as e:
                # raise e
                cp_file(tc_path, except_tc_dir)
    end_time = time.time()
    if exec_info['mutation_times'] == 0:
        mean_r = 0
    else:
        mean_r = exec_info['mutation_times'] / exec_info['mutation_ori_tc_num']
    exec_info['mean_mutation_on_one_ori_tc'] = mean_r
    # save config
    config_log = {
        'tested_dir': str(tested_dir),
        'new_tc_dir': str(new_tc_dir),
        'dumped_result_dir': str(dumped_data_base_dir),
        'except_dir': str(except_dir),
        'reason_dir': str(reason_dir),
        'runtimes': [imlp.name for imlp in imlps],
        'one_tc_limit': one_tc_limit,
        'mutate_num': mutate_num,
        'skip_common_diff': skip_common_diff,
        'exec_info': exec_info,
        'exection_time': end_time - start_time
    }
    save_json(config_log_path, config_log)
    # back up config file
    config_stem = Path(config_log_path).stem
    config_base_dir = Path(config_log_path).parent
    config_backup_name = ''.join((config_stem, get_time_string(), '.json'))
    config_backup_path = config_base_dir / config_backup_name
    save_json(config_backup_path, config_log)


def _get_wasm_paths_iterator(dir_):
    dir_ = Path(dir_)
    for p in dir_.iterdir():
        if p.suffix == '.wasm':
            path = str(p)
            tc_name = p.stem
            yield (tc_name, path)
