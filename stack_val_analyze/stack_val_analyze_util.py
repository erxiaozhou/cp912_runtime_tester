from load_results_util import load_results_from_one_dumped_data_dir
from extract_dump import dumpData
from file_util import check_dir, read_json, save_json
from log_content_util import get_reason2result_dirs_from_reason_json
from pathlib import Path
from functools import lru_cache
from tqdm import tqdm
import re
import numpy as np

from nan_detect_util import is_anan, is_cnan, is_illegal_anan, is_nan


def category_stack(reason_json_path, dumped_data_base_dir, result_dir):
    reason2tc_result_dirs = get_reason2result_dirs_from_reason_json(
        reason_json_path, dumped_data_base_dir)
    assert isinstance(reason2tc_result_dirs, dict)
    result_dir = check_dir(result_dir)
    reason_log_pair2path = {}
    path2reason_log_pair = {}
    for i, reason_key in enumerate(reason2tc_result_dirs, start=1):
        # for reason, tc_result_dirs in reason2tc_result_dirs.items():
        if reason_key == '()':
            continue
        tc_result_dirs = reason2tc_result_dirs[reason_key]
        stack_key2tc_names = group_tc_names_by_stack_key(tc_result_dirs)
        stack_key2tc_names_path = str(result_dir / '{}.json'.format(i))
        save_json(stack_key2tc_names_path, stack_key2tc_names)

        for log_key in tqdm(stack_key2tc_names.keys()):
            # generate 0_xxx.json log
            cleaned_reason_key = re.sub(r'[\'"]', '', reason_key)
            reason_content_pair = (cleaned_reason_key, '===', log_key)
            reason_content_pair = repr(reason_content_pair)
            reason_log_pair2path[reason_content_pair] = stack_key2tc_names_path
            # generate 0_xxx_inv_xxx.json
            inv_key = '<-->'.join((stack_key2tc_names_path,
                                  cleaned_reason_key))
            if inv_key not in path2reason_log_pair:
                path2reason_log_pair[inv_key] = []
            path2reason_log_pair[inv_key].append(log_key)

    reason_content_pair_log_path = result_dir / '0_reason_content_pair_log.json'
    save_json(reason_content_pair_log_path, reason_log_pair2path)
    reason_content_pair_log_inv_path = result_dir / '0_reason_content_pair_inv_log.json'
    save_json(reason_content_pair_log_inv_path, path2reason_log_pair)


def group_tc_names_by_stack_key(tc_result_dirs):
    stack_key2tc_names = {}
    for tc_result_dir in tc_result_dirs:
        dumped_results = load_results_from_one_dumped_data_dir(tc_result_dir)
        # print('tc_result_dir', tc_result_dir)
        stack_vals = cleanedStackVals.from_dumped_results(dumped_results, tc_result_dir)
        key = stack_vals.key
        name = Path(tc_result_dir).name
        if key not in stack_key2tc_names:
            stack_key2tc_names[key] = []
        stack_key2tc_names[key].append(name)
    return stack_key2tc_names


class cleanedStackVals:
    def __init__(self, dict_) -> None:
        self.stack_val_dict_ = dict_
        for v in dict_.values():
            assert isinstance(v, cleanedStackVal)

    @property
    def key(self):
        sorted_list = []
        for k, v in self.stack_val_dict_.items():
            # print('in cleaned_stack_vals.key', k)
            impl_repr = (k, v.key)
            sorted_list.append(impl_repr)
        sorted_list = sorted(sorted_list, key=lambda x: x[0])
        key = repr(tuple(sorted_list))
        return key

    @classmethod
    def from_dumped_results(cls, dumped_results, tc_result_dir):
        try:
            r = cls(get_stack_val_from_dumped_results(dumped_results))
        except Exception as e:
            print('tc_result_dir', tc_result_dir)
            raise e 
        return r


# @lru_cache(maxsize=4096 * 4, typed=False)
# def _get_key_from_processed_log_dict_repr(processed_log_dict_repr):
#     processed_log_dict = eval(processed_log_dict_repr)
#     sorted_list = []
#     for k, v in processed_log_dict.items():
#         impl_repr = (k, v)
#         sorted_list.append(impl_repr)
#     sorted_list = sorted(sorted_list, key= lambda x : x[0])
#     key = repr(tuple(sorted_list))
#     return key


def get_stack_val_from_dumped_results(dumped_results):
    stack_val_dict = {}
    for r in dumped_results:
        assert isinstance(r, dumpData)
        if not r.failed_exec:
            stack_val_dict[r.name] = cleanedStackVal.from_dump_data(r)
    return stack_val_dict


class cleanedStackVal:
    def __init__(self, stack_num=-1, stack_types=None, stack_bytes=None, stack_infered_vals=None, stack_bytes_process_nan=None) -> None:
        self.stack_types = None
        self.stack_bytes = None
        self.stack_bytes_process_nan = None
        self.stack_infered_vals = None
        self.stack_num = stack_num
        self.nan_ty =None
        self.is_nan = None
        # self.is_inf = None
        if self.stack_num > 0:
            assert self.stack_num == 1, print(self.stack_num)
            self.stack_types = stack_types
            self.stack_bytes = stack_bytes
            self.stack_infered_vals = stack_infered_vals
            self.stack_bytes_process_nan = stack_bytes_process_nan
            # 
            if self.stack_types[0] in ['f32', 'f64']:
                self.is_nan = is_nan(self.stack_bytes[0])
                if self.is_nan:
                    if is_anan(self.stack_bytes[0]):
                        self.nan_ty = 'anan'
                    elif is_cnan(self.stack_bytes[0]):
                        self.nan_ty = 'cnan'
                    else:
                        assert is_illegal_anan(self.stack_bytes[0])
                        self.nan_ty = 'illegal_anan'
            else:
                self.is_nan = False

    @property
    def key(self):
        assert self.stack_num != -1, print('Except', self.stack_num, self.stack_types, self.stack_bytes)
        if self.stack_num == 0:
            key = ''
        else:
            try:
                key = repr(self.stack_types[0])
            except:
                # print(self.stack_types, self.stack_num, self.stack_bytes)
                raise
            key = repr(self.stack_types[0])
        key += '_{}'.format(self.is_nan)
        if self.is_nan:
            key += '_{}'.format(self.nan_ty)
        if self.stack_infered_vals is not None:
            if self.stack_infered_vals[0] == np.inf:
                key += '_inf'
            elif self.stack_infered_vals[0] == -np.inf:
                key += '_ninf'
        return key

    @classmethod
    def from_dump_data(cls, dump_data_obj):
        assert isinstance(dump_data_obj, dumpData)
        assert not dump_data_obj.failed_exec
        paras = {
            'stack_num': dump_data_obj.stack_num,
            'stack_types': dump_data_obj.stack_types,
            'stack_bytes': dump_data_obj.stack_bytes,
            'stack_infered_vals': dump_data_obj.stack_infered_vals,
            'stack_bytes_process_nan': dump_data_obj.stack_bytes_process_nan
        }
        return cls(**paras)

    @classmethod
    def from_dict(cls, dict_):
        assert isinstance(dict_, dict)
        return cls(**dict_)

    @property
    def to_dict(self):
        paras = {
            'stack_num': self.stack_num,
            'stack_types': self.stack_types,
            'stack_bytes': self.stack_bytes,
            'stack_infered_vals': self.stack_infered_vals,
            'stack_bytes_process_nan': self.stack_bytes_process_nan
        }
        return paras

    def __repr__(self) -> str:
        return repr(self.to_dict)
