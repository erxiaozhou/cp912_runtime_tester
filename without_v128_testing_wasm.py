import os
import re
from pathlib import Path
from detect_special_logs import iwasm_log, wasmi_log
from file_util import check_dir, cp_file, path_read, path_write, read_json, rm_dir, remove_file_without_exception, save_json
from wasm_impl import Wasm_impl


def is_all_zero_log(path):
    content = path_read(path).split('\n')
    content = [content[i] for i in range(len(content)) if i != 7]
    sum_ = sum([int(x) for x in content if x])
    return (sum_ == 0)


def filter_arg_dict(arg_name):
    # True表示需要在后续被除掉
    shoulf_filter_out = False
    p = r'^[if]\d{1,2}x\d{1,2}\.'
    if re.search(p, arg_name):
        shoulf_filter_out = True
    p = r'^v128\.'
    if re.search(p, arg_name):
        shoulf_filter_out = True
    p = r'^table\.'
    if re.search(p, arg_name):
        shoulf_filter_out = True
    p = r'^ref\.'
    if re.search(p, arg_name):
        shoulf_filter_out = True
    # 反写
    # shoulf_filter_out = True
    # if 'memory' in arg_name:
    #     shoulf_filter_out = False
    # if 'ref.' in arg_name:
    #     shoulf_filter_out = False
    # if 'elem.' in arg_name:
    #     shoulf_filter_out = False
    # if 'data.drop' in arg_name:
    #     shoulf_filter_out = False

    return shoulf_filter_out


def get_arg_dicts(dir=None):
    if dir is None:
        dir = './pd_type_paras'
    dir = Path(dir)
    arg_dicts = {}
    stems = []
    for p in dir.iterdir():
        stem = p.stem
        if filter_arg_dict(stem):
            continue
        data = read_json(str(p))
        arg_dicts[stem] = data
        stems.append(stem)
    save_json('stems_log.json', stems)
    return arg_dicts


class df_runner:
    def __init__(self, imlps, dir_args):
        self.imlps = imlps
        self._prepare_dirs(dir_args)
        self.expected_log_data = read_json('seen_log_relation_cp907_cp.json')

    def _prepare_dirs(self, dir_args):
        for name, path in dir_args.items():
            dir_args[name] = check_dir(path)
        self.wasmi_result_base_dir = dir_args['wasmi_result_dir']
        self.iwasm_result_base_dir = dir_args['iwasm_result_dir']
        self.cmp_result_base_dir = dir_args['cmp_result_dir']
        self.non_zero_log_dir = dir_args['non_zero_log_dir']

    def _exec_imlps(self, wasm_path, tc_name):
        for imlp in self.imlps:
            assert isinstance(imlp, Wasm_impl)
            imlp.execute_and_collect(wasm_path, tc_name)

    def _exec_compare(self):
        compare_exe = 'data_compare/build/compare'
        cmd_fmt = ' '.join((compare_exe, '{} {} {} {}'))
        if self.wasmi_stack_path.exists() and\
                self.wasmi_store_path.exists() and\
                self.iwasm_data_path.exists():
            cmd = cmd_fmt.format(
                self.wasmi_store_path,
                self.wasmi_stack_path,
                self.iwasm_data_path,
                self.cmp_result_path
            )
            os.system(cmd)

    def dump_data_is_normal(self):
        return is_all_zero_log(self.cmp_result_path)

    def get_wasmi_tc_result_dir(self, tc_name):
        return self.wasmi_result_base_dir/tc_name

    def get_iwasm_tc_result_dir(self, tc_name):
        return self.iwasm_result_base_dir/tc_name

    def init_path_names(self, tc_name):
        wasmi_tc_result_dir = self.get_wasmi_tc_result_dir(tc_name)
        iwasm_tc_result_dir = self.get_iwasm_tc_result_dir(tc_name)
        self.wasmi_store_path = wasmi_tc_result_dir / 'wasmi_store'
        self.wasmi_stack_path = wasmi_tc_result_dir / 'wasmi_stack'
        self.wasmi_err_log = wasmi_tc_result_dir / 'wasmi_erro_log'
        self.wasmi_std_err_log = wasmi_tc_result_dir / 'standard_wasmi_erro_log'
        self.iwasm_data_path = iwasm_tc_result_dir / 'iwasm_data'
        self.iwasm_err_log = iwasm_tc_result_dir / 'iwasm_erro_log'
        self.iwasm_std_err_log = iwasm_tc_result_dir / 'standard_iwasm_erro_log'
        self.cmp_result_path = self.cmp_result_base_dir / tc_name
        self.non_result_path = self.non_zero_log_dir / tc_name
        self.wasmi_tc_result_dir = wasmi_tc_result_dir
        self.iwasm_tc_result_dir = iwasm_tc_result_dir

    def delete_cur_files(self, wasm_path):
        remove_file_without_exception(self.cmp_result_path)
        remove_file_without_exception(wasm_path)
        rm_dir(self.wasmi_tc_result_dir)
        rm_dir(self.iwasm_tc_result_dir)

    def init_exec_logs(self, tc_name):
        self.cur_wasmi_log = wasmi_log.from_path(self.wasmi_std_err_log, tc_name)
        self.cur_iwasm_log = iwasm_log.from_path(self.iwasm_std_err_log, tc_name)

    def get_wasmi_log(self, tc_name):
        wasmi_std_log = wasmi_log.from_path(self.wasmi_std_err_log, tc_name)
        return wasmi_std_log

    def get_iwasm_log(self, tc_name):
        iwasm_std_log = iwasm_log.from_path(self.iwasm_std_err_log, tc_name)
        return iwasm_std_log

    def run_success(self):
        success_ = False
        if self.cur_iwasm_log.is_normal:
            if self.cur_wasmi_log.is_normal:
                success_ = True
        return success_

    def dump_success(self):
        # TODO 满足这个条件也不代表dump是完全成功的，可能是dump下乱码
        # TODO 但暂时就先这样了
        if self.wasmi_stack_path.exists() and \
                self.wasmi_stack_path.exists() and \
                self.iwasm_data_path.exists():
            return True
        return False

    def is_expected_log_content(self):
        if self.expected_log_data.get(self.cur_wasmi_log.tag) is None:
            return True
        possible_iwasm_tags = self.expected_log_data[self.cur_wasmi_log.tag]
        if self.cur_iwasm_log.tag in possible_iwasm_tags:
            return True
        else:
            return False


    def run_with_mutate(self, tc_generator, mutate_times_args, actions=None):
        # assert 0
        if actions is None:
            actions = []
        skip_remove = True
        if 'remove' in actions:
            skip_remove = False
        arg_dicts = get_arg_dicts()
        dump_failed_names = []
        compare_failed_names = []
        both_success_log = {}
        data_non_zero = []
        # log_diff = []

        for inst_name, arg_dict in arg_dicts.items():
            if both_success_log.get(inst_name) is None:
                both_success_log[inst_name] = 0
            for wasm_path in tc_generator.wasm_mutation_generator(arg_dict, inst_name, **mutate_times_args):
                tc_name = Path(wasm_path).stem
                self._exec_imlps(wasm_path, tc_name)
                self.init_path_names(tc_name)
                self.init_exec_logs(tc_name)
                self._exec_compare()
                can_remove = False
                if self.run_success():
                    both_success_log[inst_name] += 1
                    if not self.dump_success():
                        dump_failed_names.append(tc_name)
                    elif not self.cmp_result_path.exists():
                        compare_failed_names.append(tc_name)
                    elif self.dump_data_is_normal():
                        can_remove = True
                    else:
                        data_non_zero.append(tc_name)
                        cp_file(self.cmp_result_path, self.non_result_path)
                else:
                    if self.is_expected_log_content():
                        can_remove = True
                #     else:
                #         # log_diff.append(tc_name)
                #         pass
                if skip_remove:
                    continue
                if can_remove:
                    self.delete_cur_files(wasm_path)
                remove_file_without_exception(self.wasmi_store_path)
                remove_file_without_exception(self.wasmi_stack_path)
                remove_file_without_exception(self.iwasm_data_path)
        # save_json('dump_failed_names.json', dump_failed_names)
        save_json('both_success_log.json', both_success_log)
        save_json('compare_failed_names.json', compare_failed_names)
        save_json('data_non_zero.json', data_non_zero)
        # save_json('log_diff.json', log_diff)

