from extract_dump.extractor import get_extractor_from_pkl
# from file_util import check_dir, pickle_load, read_bytes,
# from file_util import remove_file_without_exception, rm_dir, save_json, write_bytes
from concurrent import futures
from pathlib import Path
from file_util import check_dir, save_json


def get_imlp_combine_name(imlps):
    imlp_names = [imlp.name for imlp in imlps]
    return '--'.join(imlp_names)


def get_reason_path_to_save(tested_dir, imlps=None, append_content=None):
    dir_part = Path(tested_dir).name
    if imlps is None:
        imlps_part = get_imlp_combine_name(imlps)
    else:
        imlps_part = ''
    if append_content is None:
        path = 'different_tcs_{}_{}.json'.format(dir_part, imlps_part)
    else:
        path = 'different_tcs_{}_{}_{}.json'.format(dir_part, imlps_part,
                                                    append_content)
    return path


def get_reason_dir(tested_dir, result_dir, imlps, append_content=None):
    # result dir name
    result_dir_name = Path(result_dir).name
    tested_dir_name = Path(tested_dir).name
    base_path = result_dir.parent
    if append_content is None:
        dir_name = '{}_{}_reasons'.format(result_dir_name, tested_dir_name)
    else:
        dir_name = '{}_{}_{}_reasons'.format(result_dir_name, tested_dir_name, append_content)
    dir_path = check_dir(base_path / dir_name)
    # config_log
    config_log = {}
    config_log['result_dir'] = result_dir_name
    config_log['tested_dir'] = tested_dir_name
    config_log['runtimes'] = [imlp.name for imlp in imlps]
    config_log_name = '{}_config_log.json'.format(result_dir_name)
    save_json(base_path / config_log_name, config_log)
    return dir_path


def name_generator(imlp_name, base_dir, appended_part):
    base_dir = Path(base_dir)
    filename = '{}={}'.format(imlp_name, appended_part)
    return str(base_dir / filename)


def _get_dumped_path(save_data_dir, imlp_name):
    dumped_data_name = ''.join(('dumped', '.pkl'))
    dumped_path = name_generator(imlp_name, save_data_dir, dumped_data_name)
    return dumped_path


def exec_one_runtime(imlp, tc_name, tc_result_dir, tc_path):
    imlp_name = imlp.name
    store_append_name = '-'.join((tc_name, 'store-part'))
    store_path = name_generator(imlp_name, tc_result_dir, store_append_name)
    vstack_append_name = '-'.join((tc_name, 'vstack-part'))
    vstack_path = name_generator(imlp_name, tc_result_dir, vstack_append_name)
    log_append_name = '-'.join((tc_name, 'log'))
    log_path = name_generator(imlp_name, tc_result_dir, log_append_name)
    paras = {
        'tgt_vstack_path': vstack_path,
        'tgt_store_path': store_path,
        'tgt_log_path': log_path
    }
    result = imlp.execute_and_collect(tc_path, **paras)
    return result


def exec_one_tc(imlps, tc_name, tc_path, tc_result_dir, save_data_dir=None):
    dumped_results = []
    for imlp in imlps:
        result = exec_one_runtime(imlp, tc_name, tc_result_dir, tc_path)
        dumped_results.append(result)
        if save_data_dir is not None:
            dumped_path = _get_dumped_path(save_data_dir, result.name)
            result.to_dict(dumped_path)
    return dumped_results


def exec_one_tc_mth(imlps,
                    tc_name,
                    tc_path,
                    tc_result_dir,
                    save_data_dir=None):
    dumped_results = []
    to_do = []
    with futures.ProcessPoolExecutor(max_workers=len(imlps)) as executor:
        for imlp in imlps:
            future = executor.submit(exec_one_runtime, imlp, tc_name,
                                     tc_result_dir, tc_path)
            to_do.append(future)
        for future in to_do:
            result = future.result()
            dumped_results.append(result)
            if save_data_dir is not None:
                dumped_path = _get_dumped_path(save_data_dir, result.name)
                # print('dumped_path', dumped_path)
                # print(type(result))
                # print(result.name)
                # input()
                result.to_dict(dumped_path)
    return dumped_results


def load_results(save_data_dir):
    results = []
    for p in Path(save_data_dir).iterdir():
        if p.suffix == '.pkl':
            dumped_path = str(p)
            result = get_extractor_from_pkl(dumped_path)
            results.append(result)
    return results


def get_wasms_from_a_path(dir_):
    tc_paths = []
    dir_ = Path(dir_)
    for p in dir_.iterdir():
        if p.suffix == '.wasm':
            path = str(p)
            tc_name = p.stem
            tc_paths.append((tc_name, path))
    return tc_paths
