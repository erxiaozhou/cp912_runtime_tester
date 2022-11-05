import re
from file_util import path_read, path_write, read_json, save_json
from pathlib import Path
target_dir = Path('./check_result_dir')


def get_tc_names():
    return [x.name for x in Path('./results/iwasm').iterdir()]


def _get_iwasm_content_from_path(path):
    content = path_read(path)
    content = re.sub(r'^\-?(?:(?:inf)|(?:nan)):[if](?:(?:32)|(?:64))$', '', content)
    content = re.sub(r'^[0-9abcdefxi:\n\-\+\.]+$', '', content)
    content = content.strip('\n')
    content = re.sub(r' \(at offset \d+\)', '', content)
    content = re.sub(r'module [a-zA-Z\d\./_]+?\.wasm', '', content)
    return content


def _get_iwasm_content(tc_name):
    iwasm_result_dir = Path('./results/iwasm')
    dir = iwasm_result_dir / tc_name
    p = dir / 'iwasm_erro_log'
    content = _get_iwasm_content_from_path(p)
    return content


def _get_wasmi_content_from_path(path):
    content = path_read(path)
    content = re.sub(r'^[0-9abcdefxi:\n\-\+\.]+$', '', content)
    content = re.sub(r'Error: .*\.wasm: ', '', content)
    content = re.sub(r' \(at offset \d+\)', '', content)
    content = re.sub(r' \(at offset 0x[0-9a-fA-F]+\)', '', content)
    content = content.strip('\n')
    return content


def _get_wasmi_content(tc_name):
    wasmi_result_dir = Path('./results/wasmi')
    dir = wasmi_result_dir / tc_name
    p = dir / 'wasmi_erro_log'
    content = _get_wasmi_content_from_path(p)
    return content


class wasmi_log():
    tags = [
        'SIMD unsupport',
        'memory OOB',
        'reference unsupport',
        'integer overflow',
        'bulk memory unsupport'
    ]
    def __init__(self, processed_content, tc_name):
        if processed_content == '':
            tag = 'normal'
        elif 'SIMD support is not enabled' in processed_content:
            tag = 'SIMD unsupport'
        elif 'out of bounds memory access' in processed_content:
            tag = 'memory OOB'
        elif 'reference types support is not enabled' in processed_content:
            tag = 'reference unsupport'
        elif 'integer overflow' in processed_content:
            tag = 'integer overflow'
        elif 'bulk memory support is not enabled' in processed_content:
            tag = 'bulk memory unsupport'
        elif 'unsupported opcode' in processed_content:
            tag = 'unsupported opcode'
        elif 'unknown function' in processed_content:
            tag = 'unknown function'
        elif 'invalid UTF-8 encoding' in processed_content:
            tag = 'invalid UTF-8 encoding'
        elif 'Unknown opcode' in processed_content:
            tag = 'unknown opcode'
        elif 'Invalid var' in processed_content:
            tag = 'Invalid var'
        elif 'uninitialized element' in processed_content:
            tag = 'uninitialized element'
        elif 'type mismatch' in processed_content:
            tag = 'type mismatch'
        elif 'malformed section' in processed_content:
            tag = 'malformed section'
        elif 'could not find function' in processed_content:
            tag = 'could not find function'
        elif 'local index out of bounds' in processed_content:
            tag = 'local index OOB'
        elif 'exported memory index out of bounds' in processed_content:
            tag = 'exported memory index OOB'
        elif 'type index out of bounds' in processed_content:
            tag = 'type OOB'
        elif processed_content:
            tag = '{}'.format(processed_content)
        self.tag = tag
        self.content = processed_content
        self.tc_name = tc_name

    @property
    def is_normal(self):
        return (self.tag == 'normal')

    @classmethod
    def from_tc_name(cls, tc_name):
        content = _get_wasmi_content(tc_name)
        return cls(content, tc_name)

    @classmethod
    def from_path(cls, path, tc_name=None):
        content = _get_wasmi_content_from_path(path)
        if tc_name is None:
            tc_name = Path(path).stem
        return cls(content, tc_name)


class iwasm_log():
    def __init__(self, processed_content, tc_name):
        if processed_content == '':
            tag = 'normal'
        elif 'invalid section id' in processed_content:
            tag = 'invalid section id'
        elif 'out of bounds memory access' in processed_content:
            tag = 'memory OOB'
        elif 'reference types support is not enabled' in processed_content:
            tag = 'reference unsupport'
        elif 'integer overflow' in processed_content:
            tag = 'integer overflow'
        # elif 'nan:' in processed_content:
        #     tag = 'nan'
        elif 'unsupported opcode' in processed_content:
            tag = 'unsupported opcode'
        elif 'Invalid type' in processed_content:
            tag = 'Invalid type'
        elif 'Bad version number' in processed_content:
            tag = 'Bad version number'
        elif 'invalid function type' in processed_content:
            tag = 'invalid function type'
        elif 'func index out of bounds' in processed_content:
            tag = 'function OOB'
        elif 'invalid UTF-8 encoding' in processed_content:
            tag = 'invalid UTF-8 encoding'
        elif 'unexpected end-of-file' in processed_content:
            tag = 'unexpected EOF'
        elif 'Unexpected EOF' in processed_content:
            tag = 'unexpected EOF'
        elif 'Unexpected data at the end of the section' in processed_content:
            tag = 'unexpected data section end'
        elif 'invalid local type' in processed_content:
            tag = 'invalid local type'
        elif 'unexpected end' in processed_content:
            tag = 'unexpected end'
        elif 'unknown binary version' in processed_content:
            tag = 'unknown binary version'
        elif 'invalid section id' in processed_content:
            tag = 'invalid section id'
        elif 'invalid local count' in processed_content:
            tag = 'invalid local count'
        elif 'unexpected content after last section or junk after last section' in processed_content:
            tag = 'unexpected data section end'
        elif 'invalid mutability' in processed_content:
            tag = 'invalid mutability'
        elif 'section size mismatch' in processed_content:
            tag = 'section size mismatch'
        elif 'unknown function' in processed_content:
            tag = 'unknown function'
        elif 'unknown memory' in processed_content:
            tag = 'unknown memory'
        elif processed_content:
            # assert tag is not None, print(processed_content)
            tag = '{}'.format(processed_content)
        self.tag = tag
        self.content = processed_content
        self.tc_name = tc_name

    @property
    def is_normal(self):
        return (self.tag  == 'normal')

    @classmethod
    def from_tc_name(cls, tc_name):
        content = _get_iwasm_content(tc_name)
        return cls(content, tc_name)

    @classmethod
    def from_path(cls, path, tc_name=None):
        content = _get_iwasm_content_from_path(path)
        if tc_name is None:
            tc_name = Path(path).stem
        return cls(content, tc_name)
