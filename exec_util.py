from extract_dump.extractor import get_extractor_from_pkl
# from file_util import check_dir, pickle_load, read_bytes,
# from file_util import remove_file_without_exception, rm_dir, save_json, write_bytes
from concurrent import futures
from pathlib import Path
from file_util import check_dir, save_json
from data_comparer import are_different


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
    result = imlp.execute_and_collect(tc_path, log_path, **paras)
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


def load_log_content(save_data_dir):
    results = load_results(save_data_dir)
    name_log = {}
    for r in results:
        name_log[r.name] = r.log_content
    return name_log


def get_wasms_from_a_path(dir_):
    tc_paths = []
    dir_ = Path(dir_)
    for p in dir_.iterdir():
        if p.suffix == '.wasm':
            path = str(p)
            tc_name = p.stem
            tc_paths.append((tc_name, path))
    return tc_paths

def load_a_result_base_dir(result_json_path, result_dir):
    reasons = {}
    for tc_result_dir in Path(result_dir).iterdir():
        tc_name = tc_result_dir.name
        dumped_results = load_results(tc_result_dir)
        difference_reason = are_different(dumped_results, tc_name)
        if difference_reason:
            reasons[tc_name] = difference_reason
    save_json(result_json_path, reasons)
    return reasons
