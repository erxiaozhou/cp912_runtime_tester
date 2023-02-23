'''
旨在生成wasm的插装结果，结构大概是这样的
<code段前面的内容><0A><code段的长度><函数数量><其他函数><被测函数><其他函数与后续>
<code段前面的内容>里面的type section（section id : 1）是要改的
type段，每个type是0x60开头的，para和result区分的具体规则暂时不清楚，但是可以推断出来
func段，看起来是，section id, 字节数量，函数数量，每个函数的类型
'''
from pathlib import Path
import leb128
from file_util import write_bytes


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


def read_next_leb_num(byte_seq, offset):
    a = bytearray()
    while True:
        b = byte_seq[offset]
        offset += 1
        a.append(b)
        if (b & 0x80) == 0:
            break
    return leb128.u.decode(a), offset


def _get_wasm_bytes_from_dict(section_dict):
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


def write_wasm_from_dict(path, section_dict):
    assert not Path(path).exists()
    wasm_bytes = _get_wasm_bytes_from_dict(section_dict)
    write_bytes(path, wasm_bytes)


def prepare_template(template_path):
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
