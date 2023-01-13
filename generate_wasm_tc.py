'''
旨在生成wasm的插装结果，结构大概是这样的
<code段前面的内容><0A><code段的长度><函数数量><其他函数><被测函数><其他函数与后续>
<code段前面的内容>里面的type section（section id : 1）是要改的
type段，每个type是0x60开头的，para和result区分的具体规则暂时不清楚，但是可以推断出来
func段，看起来是，section id, 字节数量，函数数量，每个函数的类型
'''
# TODO 没有考虑带type的select
import leb128
from file_util import write_bytes
import os

id_name_dict = {
    1: 'type',
    2: 'import',
    3: 'function',
    4: 'table',
    5: 'memory',
    6: 'global',
    7: 'export',
    8: 'start',
    9: 'element',
    10: 'code',
    11: 'data',
    12: 'data_count'
}

type_name_to_byte = {
    'i32': 0x7F,
    'i64': 0x7E,
    'f32': 0x7D,
    'f64': 0x7C,
    'v128': 0x7B,
    'funcref': 0x70,
    'externref': 0x6F
}


def transfer_text_type_to_binary(vt):
    assert vt in type_name_to_byte
    return type_name_to_byte[vt]


def detect_new_type(push_type):
    # TODO 目前就是假设只会向栈上压一个值
    # TODO 暂时替代写法
    # * 没写param部分是因为暂时的设定中param部分为空
    type_log = {'param': bytearray(), 'result': bytearray()}
    if push_type is None:
        pass
    else:
        assert push_type != 'any'
        type_byte = transfer_text_type_to_binary(push_type)
        type_log['result'].append(type_byte)
    return type_log


def read_next_leb_num(byte_seq, offset):
    a = bytearray()
    while True:
        b = byte_seq[offset]
        offset += 1
        a.append(b)
        if (b & 0x80) == 0:
            break
    return leb128.u.decode(a), offset


class type_section_log():
    def __init__(self, types):
        self.types = types

    def detect_type(self, query_type):
        for i, possible_type in enumerate(self.types):
            if query_type['param'] == possible_type['param']:
                if query_type['result'] == possible_type['result']:
                    return i
        return None

    def append_type(self, to_appen_type):
        self.types.append(to_appen_type)

    def generate_bytes(self):
        # 不包含section id和字节数量
        body_bytes = bytearray()  # 不包含字节数的bytes
        body_bytes.extend(leb128.u.encode(len(self.types)))
        for type_log in self.types:
            body_bytes.append(0x60)
            param_part = type_log['param']
            body_bytes.extend(leb128.u.encode(len(param_part)))
            assert isinstance(param_part, bytearray)
            body_bytes.extend(param_part)
            result_part = type_log['result']
            body_bytes.extend(leb128.u.encode(len(result_part)))
            body_bytes.extend(result_part)
        return body_bytes

    @classmethod
    def from_bytes(cls, byte_seq):
        offset = 0
        length, offset = read_next_leb_num(byte_seq, offset)
        types = []
        assert byte_seq[offset] == 0x60
        cur_type_bytes = bytearray()
        for b in byte_seq[offset + 1:]:
            if b != 0x60:
                cur_type_bytes.append(b)
            else:
                types.append(cur_type_bytes)
                cur_type_bytes = bytearray()
        assert len(cur_type_bytes)
        types.append(cur_type_bytes)
        for i, type_bytes in enumerate(types):
            cur_type_dict = {'param': bytearray(), 'result': bytearray()}
            type_bytes_offset = 0
            para_num, type_bytes_offset = read_next_leb_num(
                type_bytes, type_bytes_offset)
            for k in range(para_num):
                type_byte = type_bytes[type_bytes_offset]
                cur_type_dict['param'].append(type_byte)
                type_bytes_offset += 1
            result_num, type_bytes_offset = read_next_leb_num(
                type_bytes, type_bytes_offset)
            for k in range(result_num):
                type_byte = type_bytes[type_bytes_offset]
                cur_type_dict['result'].append(type_byte)
                type_bytes_offset += 1
            assert type_bytes_offset == len(type_bytes)
            types[i] = cur_type_dict
        return cls(types)


def get_wasm_bytes_from_dict(section_dict):
    result = bytearray()
    result.extend(section_dict['pre'])
    for i in range(1, 12):
        content = section_dict.get(id_name_dict[i])
        if content is None:
            continue
        result.extend(leb128.u.encode(i))
        section_len = len(content)
        result.extend(leb128.u.encode(section_len))
        result.extend(content)
    return result


def write_new_wasm(path, section_dict):
    wasm_bytes = get_wasm_bytes_from_dict(section_dict)
    write_bytes(path, wasm_bytes)


def end_with_0B(ba):
    assert isinstance(ba, (bytearray, bytes)), print(ba, type(ba))
    return ba[-1] == 0x0B


def renew_code_section(sec_template, added_bytes, modified_idx=1):
    ori_code_bytes = sec_template['code']
    offset = 0
    func_num, offset = read_next_leb_num(ori_code_bytes, offset)
    func_num_end_offset = offset
    func_lengths = []
    
    func_start_offsets = []
    func_end_offsets = []
    # end和start之间有一个表示当前code长度的leb
    for i in range(func_num):
        code_len, start_offset = read_next_leb_num(ori_code_bytes, offset)
        end_offset = start_offset + code_len
        func_lengths.append(code_len)
        cur_func_content = ori_code_bytes[start_offset:end_offset]
        func_start_offsets.append(start_offset)
        func_end_offsets.append(end_offset)
        offset = end_offset
        assert end_with_0B(cur_func_content)
        if i == modified_idx:
            content_to_modify = bytearray(cur_func_content)
    # local_part_length = func_lengths[modified_idx] -1  # 这是因为目前假设模板只有local part+0xB
    # TODO 目前是假设新加代码的地方是10个nop占着的
    assert isinstance(content_to_modify, bytearray)
    nop_num = 10
    local_part_length = content_to_modify.find(bytearray([0x1]*nop_num))
    new_code_body = bytearray()
    if modified_idx == 0:
        new_code_body.extend(ori_code_bytes[:func_num_end_offset])
    else:
        start_func_part = ori_code_bytes[:func_end_offsets[modified_idx-1]]
        new_code_body.extend(start_func_part)
    # TODO 假设直接插在local part后面
    # [:code3_len_offset] | [*code3_length_bytes] | [code3_save] | [*code3_new] | [code4_len_offset:]
    # 关于code section中对每个function的编码，第一个数字应该是总字节数，第二个数字应该是local定义的种类的数量，如果定义了三种类型的6给local，这个值应该是3
    new_modified_func_len = func_lengths[modified_idx] + len(added_bytes) - nop_num
    new_code_body.extend(leb128.u.encode(new_modified_func_len))
    local_part_content = ori_code_bytes[func_start_offsets[modified_idx]:func_start_offsets[modified_idx]+local_part_length]
    # assert 0, print([hex(x) for x in local_part_content], func_start_offsets[modified_idx], local_part_length)
    new_code_body.extend(local_part_content)
    new_code_body.extend(added_bytes)
    new_code_body.extend(ori_code_bytes[func_start_offsets[modified_idx]+local_part_length+nop_num: func_end_offsets[modified_idx]])
    new_code_body.extend(ori_code_bytes[func_end_offsets[modified_idx]:])
    return new_code_body



def renew_type_section(sec_template, push_type):
    # type
    cur_type = detect_new_type(push_type)
    types_log = type_section_log.from_bytes(sec_template['type'])
    # cur_type
    type_index = types_log.detect_type(cur_type)
    if type_index is None:
        types_log.append_type(cur_type)
        type_index = len(types_log.types) - 1
    assert type_index == types_log.detect_type(cur_type)
    return types_log.generate_bytes(), type_index

def renew_function_section(sec_template, modified_idx, type_index):
    function_bytes = bytearray(sec_template['function'])
    func_num, offset = read_next_leb_num(function_bytes, offset=0)
    function_bytes[offset+modified_idx] = type_index
    assert len(function_bytes) == func_num + offset
    return function_bytes

def generate_wasm_section_dict(sec_template, push_type, added_bytes, modified_idx=1):
    result = {k: v for k, v in sec_template.items()}
    result['type'], type_index = renew_type_section(sec_template, push_type)
    result['function'] = renew_function_section(sec_template, modified_idx, type_index)
    result['code'] = renew_code_section(sec_template, added_bytes, modified_idx)
    return result


def _prepare_template(template_path):
    with_table_template = {}
    f_temp_src = open(template_path, 'rb')
    # prepare pre
    f_temp_len = f_temp_src.seek(0, 2)
    f_temp_src.seek(0, 0)
    with_table_template['pre'] = f_temp_src.read(0x8)
    while f_temp_src.tell() < f_temp_len:
        cur_section_id_raw_content = f_temp_src.read(1).hex()
        cur_section_id = int(cur_section_id_raw_content, 16)
        cur_section_name = id_name_dict[cur_section_id]
        section_length = leb128.u.decode_reader(f_temp_src)[0]
        content = f_temp_src.read(section_length)
        with_table_template[cur_section_name] = content
    return with_table_template


class wasm_direct_generator:
    _visted_template = {}
    def __init__(self, template_path=None):
        if template_path is None:
            template_path = './hw_z2.wasm'
        if template_path.endswith('.wat'):
            new_path = template_path[:-3]+'wasm'
            os.system('wat2wasm {} -o {}'.format(template_path, new_path))
            template_path = new_path
        if template_path in wasm_direct_generator._visted_template:
            self.sec_template = wasm_direct_generator._visted_template[template_path]
        else:
            self.sec_template = _prepare_template(template_path)

    def wasm_generator(self, tgt_file, push_type, added_bytes):
        new_sec_dict = generate_wasm_section_dict(self.sec_template, push_type, added_bytes, 0)
        wasm_bytes = get_wasm_bytes_from_dict(new_sec_dict)
        write_bytes(tgt_file, wasm_bytes)
        return wasm_bytes

    def test_wasm_generator(self):
        self.wasm_generator('tt_zg.wasm', ['i32'], bytearray([0x41, 0x0f, 0x41, 0x0f, 0x6A]))


def mutate_code_sec(path):
    sec_template = _prepare_template(path)
    code_sec = sec_template['code']
    



if __name__ == '__main__':
    template = _prepare_template('./hw_z2.wasm')
    # for k,v in template.items():
    #     print('{} {}'.format(k, v))
