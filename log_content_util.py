from exec_util import load_results, load_log_content
from file_util import check_dir, read_json, save_json
from pathlib import Path
import re

hex_p = r'0[xX][0-9a-fA-F]+'
num_p = r'^[\-\+]?(?:(?:\d+)|(?:[\.\+\d]+e[\-\+]?\d+)|(?:\d+\.\d+)|(?:nan)|(?:inf))\n?$'
wasm_path_p = r' [^ ]+\.wasm'
offset_p = r'\(at offset (?:(?:\d+)|(?:0[xX][0-9a-fA-F]+))\)'
time_p = r'\[[\-0-9]+ [\.:0-9]+\]'

def extract_keyword(content):
    content_relation = {
        'type mismatch': 'type mismatch',
        'trailing bytes at end of section': 'trailing bytes at end of section',
        'integer too large': 'integer too large',
        'Invalid signed LEB encoding': 'Invalid signed LEB encoding',
        'section size mismatch': 'section size mismatch',
        'unsupported opcode fd': 'unsupported opcode fd',
        'unsupported opcode fc': 'unsupported opcode fc',
        'Unknown opcode':'Unknown opcode',
        'unknown memory': 'unknown memory',
        'unknown table': 'unknown table',
        'bulk memory support is not enabled': 'bulk memory support is not enabled',
        'ulti-memory support is not enabled': 'multi-memory support is not enabled',
        'memory index reserved byte must be zero': 'memory index reserved byte must be zero',
        'SIMD support is not enabled': 'SIMD support is not enabled',
        'table index out of bounds': 'table index out of bounds', 
        'illegal opcode': 'illegal opcode', 
        'Unexpected EOF': 'Unexpected EOF',
        'expected data but found end of stream': 'expected data but found end of stream',
        'Mismatched memory alignment': 'Mismatched memory alignment',
        'alignment too large': 'alignment too large',
        'alignment greater than natural alignment': 'alignment greater than natural alignment',
        'elemSegmentIndex must be less than module.elemSegments.size()':'elemSegmentIndex must be less than module.elemSegments.size()',
        'operators remaining after end of function': 'operators remaining after end of function',
        'Invalid alignment': 'Invalid alignment',
        'alignment must not be larger than natural': 'alignment must not be larger than natural',
        'unsupported opcode': 'unsupported opcode',
        'section size mismatch': 'section size mismatch',
        'Expected non-empty control stack': 'Expected non-empty control stack',
        'stack was not empty at end of control structure': 'stack was not empty at end of control structure',
        'invalid lane index': 'invalid lane index',
        'local index out of bounds': 'local index out of bounds',
        'reference types support is not enabled': 'reference types support is not enabled',
        'unexpected end-of-file': 'unexpected end-of-file',
        'Invalid var_i32': 'Invalid var_i32',
        'zero byte expected': 'zero byte expected',
        'out of bounds memory access': 'out of bounds memory access',
        'outOfBoundsMemoryAccess': 'outOfBoundsMemoryAccess',
        'reachedUnreachable': 'reachedUnreachable',
        'Unknown 0xfc subopcode': 'Unknown 0xfc subopcode'

    }
    # content_relation_c = {
    #     'type mismatch': 'type mismatch',
    #     'integer too large': 'integer too large',
    #     'Invalid signed LEB encoding': 'Invalid signed LEB encoding',
    #     'section size mismatch': 'section size mismatch',
    #     'unsupported opcode fd': 'unsupported opcode fd',
    #     'unsupported opcode fc': 'unsupported opcode fc',
    #     'Unknown opcode':'illegal opcode',
    #     'illegal opcode': 'illegal opcode', 
    #     'unknown memory': 'unknown memory',
    #     'unknown table': 'unknown table',
    #     'bulk memory support is not enabled': 'bulk memory',
    #     'ulti-memory support is not enabled': 'bulk memory',
    #     'memory index reserved byte must be zero': 'memory index reserved byte must be zero',
    #     'SIMD support is not enabled': 'SIMD support is not enabled',
    #     'table index out of bounds': 'table index out of bounds', 
    #     'Empty Stack': 'Empty Stack', 
    #     'Unexpected EOF': 'Unexpected EOF',
    #     'expected data but found end of stream': 'expected data but found end of stream',
    #     'Mismatched memory alignment': 'Mismatched memory alignment',
    #     'alignment too large': 'alignment too large',
    #     'alignment greater than natural alignment': 'alignment greater than natural alignment',
    #     'elemSegmentIndex must be less than module.elemSegments.size()':'elemSegmentIndex must be less than module.elemSegments.size()',
    #     'operators remaining after end of function': 'operators remaining after end of function',
    #     'Invalid alignment': 'Invalid alignment',
    #     'alignment must not be larger than natural': 'alignment must not be larger than natural',
    #     'unsupported opcode': 'unsupported opcode',
    #     'section size mismatch': 'section size mismatch',
    #     'Expected non-empty control stack': 'Expected non-empty control stack',
    #     'stack was not empty at end of control structure': 'stack was not empty at end of control structure',
    #     'invalid lane index': 'invalid lane index',
    #     'local index out of bounds': 'local index out of bounds',
    #     'reference types support is not enabled': 'reference types support is not enabled',
    #     'unexpected end-of-file': 'unexpected end-of-file'

    # }
    lower_content = content.lower()
    for k, v in content_relation.items():
        if k.lower() in lower_content:
            return v
    return content

def _get_key_from_log_content(content_dict):
    sorted_list = []
    for k, v in content_dict.items():
        impl_repr = (k, v)
        sorted_list.append(impl_repr)
    sorted_list = sorted(sorted_list, key= lambda x : x[0])
    key = repr(tuple(sorted_list))
    return key


def _process_content_dict(content_dict):
    data = {}
    for key, s in content_dict.items():
        if key == 'wasm3_dump':
            p = r' *Result: *\-?[0-9\.]+$'
            s = re.sub(p, '', s)
            p = r' *Result: *\-?0[xX][0-9a-fA-F]+$'
            s = re.sub(p, '', s)
            p = r' *Result: *\-?nan'
            s = re.sub(p, '', s)
            s = re.sub('\n', '', s)
            if 'Empty Stack' in s:
                s = ''
        elif key == 'WasmEdge_disableAOT_newer':
            s = re.sub(time_p, '', s)
            s = re.sub(wasm_path_p, '', s)
            p = r'Bytecode offset: 0[xX][0-9a-fA-F]+'
            s = re.sub(p, '', s)
            p = r' Code: 0[xX][0-9a-fA-F]+'
            s = re.sub(p, '', s)
            s = re.sub(num_p, '', s)
        elif key == 'wasmer_default_dump':
            s = re.sub(offset_p, '', s)
            s = re.sub(wasm_path_p, '', s)
        elif key == 'wasmi_interp':
            s = re.sub(offset_p, '', s)
            s = re.sub(wasm_path_p, '', s)
        elif key == 'iwasm_fast_interp_dump':
            s = re.sub(r'^\n$', '', s)
            p = r'^0x[a-f\d]+:i32\n$'
            s = re.sub(p, '', s)
            p = r'^.*:f32\n$'
            s = re.sub(p, '', s)
        elif key == 'iwasm_classic_interp_dump':
            s = re.sub(r'^\n$', '', s)
            p = r'^0x[a-f\d]+:i32\n$'
            s = re.sub(p, '', s)
            p = r'^.*:f32\n$'
            s = re.sub(p, '', s)
        elif key == 'WAVM_default':
            pass
        else:
            assert 0
        s = extract_keyword(s)
        data[key]=s
    return data


def _get_content_key_from_dir(path):
    content_dict = load_log_content(path)
    processed_content_dict = _process_content_dict(content_dict)
    key = _get_key_from_log_content(processed_content_dict)
    return key


def get_paths_from_reason_json(reason_path, result_base_dir):
    result_base_dir = Path(result_base_dir)
    reason_paths = {}
    reason_tc_names = read_json(reason_path)
    for k, v in reason_tc_names.items():
        paths = [result_base_dir/name for name in v]
        reason_paths[k] = paths
    return reason_paths


def group_paths_by_log_content(paths, names=None):
    if names is None:
        names = [Path(p).name for p in paths]
    assert len(paths) == len(names)
    content_paths_dict = {}
    i=0
    for p, name in zip(paths, names):
        i+=1
        # print(i)
        key = _get_content_key_from_dir(p)
        if key not in content_paths_dict:
            content_paths_dict[key] = []
        content_paths_dict[key].append(name)
    return content_paths_dict


def log_content_categorize_reason_path(reason_json_path, result_base_dir, log_categorize_dir):
    reason_paths = get_paths_from_reason_json(reason_json_path, result_base_dir)
    assert isinstance(reason_paths, dict)
    log_categorize_dir = check_dir(log_categorize_dir)
    for i, key in enumerate(reason_paths):
        p = log_categorize_dir / '{}.json'.format(i)
        paths = reason_paths[key]
        content_paths_dict = group_paths_by_log_content(paths)
        save_json(p, content_paths_dict)


def test_one_path():
    test_path = '/media/hdd_xj1/cp910_data/main_testing/result/f32.abs_10/'
    content_dict = load_log_content(test_path)
    processed_content_dict = _process_content_dict(content_dict)
    for k,v in processed_content_dict.items():
        print(k, '\n====\n',v)
    pass
    print('='* 50)
    key = _get_key_from_log_content(processed_content_dict)
    print(key)


def test_log_content_categorize_reason_path():
    reason_json_path = '/media/hdd_xj1/cp910_data/main_testing/config_log.json'
    result_base_dir = '/media/hdd_xj1/cp910_data/main_testing/result'
    log_categorize_dir = 'tt_jsons'
    log_content_categorize_reason_path(reason_json_path, result_base_dir, log_categorize_dir)




if __name__ == '__main__':
    pass
    # test_one_path()
    # test_paths()
    # test_log_content_categorize_reason_path()
