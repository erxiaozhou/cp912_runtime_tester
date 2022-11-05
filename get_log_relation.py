#!/home/zph/anaconda3/bin/python
from detect_special_logs import wasmi_log
from detect_special_logs import iwasm_log
from pathlib import Path

from file_util import check_dir, read_json, save_json


def get_tc_names(base_dir):
    base_dir = Path(base_dir)
    iwasm_sub_dir = base_dir / 'iwasm'
    wasmi_sub_dir = base_dir / 'wasmi'
    iwasm_names = set(x.name for x in iwasm_sub_dir.iterdir())
    wasmi_names = set(x.name for x in wasmi_sub_dir.iterdir())
    return list(wasmi_names | iwasm_names)


def get_log_relation(base_dir, log_path):
    base_dir = Path(base_dir)
    iwasm_dir = base_dir / 'iwasm'
    wasmi_dir = base_dir / 'wasmi'
    relation = dict()
    wasmi_tags = set()
    iwasm_tags = set()
    names = get_tc_names(base_dir)
    for name in names:
        wasmi_log_path = wasmi_dir / name / 'standard_wasmi_erro_log'
        iwasm_log_path = iwasm_dir / name / 'standard_iwasm_erro_log'
        wasmi_log_case = wasmi_log.from_path(str(wasmi_log_path), name)
        iwasm_log_case = iwasm_log.from_path(str(iwasm_log_path), name)
        wasmi_tag = wasmi_log_case.tag
        iwasm_tag = iwasm_log_case.tag
        wasmi_tags.add(wasmi_tag)
        iwasm_tags.add(iwasm_tag)
        if relation.get(wasmi_tag) is None:
            relation[wasmi_tag] = set()
        relation[wasmi_tag].add(iwasm_tag)
    for k in relation.keys():
        relation[k] = list(relation[k])
    save_json(log_path, relation)

    return relation



def detect_special_content(target_dicts, base_dir):
    assert isinstance(target_dicts, list)
    result_names = []
    for target_dict in target_dicts:
        keys = list(target_dict.keys())
        assert len(keys) ==2
        assert 'wasmi' in keys
        assert 'iwasm' in keys
    base_dir = check_dir(base_dir)
    iwasm_dir = base_dir / 'iwasm'
    wasmi_dir = base_dir / 'wasmi'
    names = get_tc_names(base_dir)
    for name in names:
        wasmi_log_path = wasmi_dir / name / 'standard_wasmi_erro_log'
        iwasm_log_path = iwasm_dir / name / 'standard_iwasm_erro_log'
        wasmi_log_case = wasmi_log.from_path(str(wasmi_log_path), name)
        iwasm_log_case = iwasm_log.from_path(str(iwasm_log_path), name)
        wasmi_tag = wasmi_log_case.tag
        iwasm_tag = iwasm_log_case.tag
        for target_dict in target_dicts:
            if target_dict['wasmi'] == wasmi_tag:
                if target_dict['iwasm'] == iwasm_tag:
                    result_names.append(name)
                    break
    return result_names


if __name__ == '__main__':
    # get_log_relation('cp907_p_cur', './seen_log_relation_cp907_cur.json')
    get_log_relation('cp907_p_cur2', './seen_log_relation_cp907_cur2.json')
    # spec_cases = [
    #     {
    #         'wasmi':'illegal opcode: 0xc5',
    #         'iwasm':'Exception: unreachable'
    #     },
    #     # {
    #     #     'wasmi':'unknown opcode',
    #     #     'iwasm':'normal'
    #     # },
    #     # {
    #     #     'wasmi':'invalid function type',
    #     #     'iwasm':'normal'
    #     # },
    #     # {
    #     #     'wasmi': 'uninitialized element',
    #     #     'iwasm': 'normal'
    #     # },
    #     # {
    #     #     'wasmi': 'operators remaining after end of function',
    #     #     'iwasm': 'normal'
    #     # }
    # ]
    # spec_names = detect_special_content(spec_cases, 'cp907_p1')
    # for name in spec_names:
    #     print(name)
