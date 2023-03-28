from extract_dump import get_extractor_from_pkl
from concurrent import futures
from pathlib import Path
from path_group_util import imlp_result_path_group


def load_results_from_one_dumped_data_dir(one_tc_result_dir):
    results = []
    for p in Path(one_tc_result_dir).iterdir():
        if p.suffix == '.pkl':
            dumped_path = str(p)
            result = get_extractor_from_pkl(dumped_path)
            results.append(result)
    return results


def exec_one_tc(imlps, tc_path, tc_result_dir, tc_dump_dir=None):
    dumped_results = []
    for imlp in imlps:
        result = exec_one_runtime(imlp, tc_result_dir, tc_path)
        dumped_results.append(result)
        if tc_dump_dir is not None:
            dumped_path = _get_dumped_path(tc_dump_dir, result.name)
            result.to_dict(dumped_path)
    return dumped_results


def exec_one_tc_mth(imlps,
                    tc_path,
                    tc_result_dir,
                    tc_dump_dir=None):
    dumped_results = []
    to_do = []
    with futures.ProcessPoolExecutor(max_workers=len(imlps)) as executor:
        for imlp in imlps:
            future = executor.submit(exec_one_runtime, imlp,
                                     tc_result_dir, tc_path)
            to_do.append(future)
        for future in to_do:
            result = future.result()
            dumped_results.append(result)
            if tc_dump_dir is not None:
                dumped_path = _get_dumped_path(tc_dump_dir, result.name)
                result.to_dict(dumped_path)
    return dumped_results


def exec_one_runtime(imlp, tc_result_dir, tc_path):
    imlp_name = imlp.name
    store_path = _path_generator(imlp_name, tc_result_dir, 'store-part')
    vstack_path = _path_generator(imlp_name, tc_result_dir, 'vstack-part')
    tgt_log_path = _path_generator(imlp_name, tc_result_dir, 'log')
    tgt_inst_path = _path_generator(imlp_name, tc_result_dir, 'has_instance')
    result_paths = imlp_result_path_group(
        tgt_log_path = tgt_log_path,
        tgt_vstack_path = vstack_path,
        tgt_store_path = store_path,
        tgt_inst_path = tgt_inst_path
    )
    result = imlp.execute_and_collect(tc_path, result_paths)
    return result


def _path_generator(imlp_name, base_dir, appended_part):
    base_dir = Path(base_dir)
    filename = '{}={}'.format(imlp_name, appended_part)
    return str(base_dir / filename)


def _get_dumped_path(save_data_dir, imlp_name):
    dumped_path = _path_generator(imlp_name, save_data_dir, 'dumped.pkl')
    return dumped_path
