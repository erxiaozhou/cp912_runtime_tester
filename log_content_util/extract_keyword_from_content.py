from functools import lru_cache


table_OOB = 'table OOB'

fc_opcode = 'unsupported opcode fc'
fd_opcode = 'unsupported opcode fd'
illegal_opcode = 'illegal/unknown opcode'

multi_memory_unsupport = 'multi memory',
memory_OOB = 'memory OOB'

unreachable = 'unreachable'

type_mismatch = 'type mismatch'

# SIMD_unsupport = 'SIMD unsupport'


large_alignment = 'large alignment'
illegal_alignment = 'illegal alignment'

reference_unsupport = 'reference unsupport'

too_many_local = 'too many local'

elem_seg_oob = 'element segment OOB'

# section size related
section_mismatch = 'section mismatch'
unexpected_EOF = 'enexpected EOF'
func_sec_mismatch = 'func section size mismatch'
func_mismatch = 'function size mismatch'
illegal_int_encoding = 'illegal int encoding'
stack_operand_overflow = 'stack operand overflow'
control_structure_depth_related = 'control_structure_depth related'


categorize_info_level1 = {
    'operators remaining after end of function': func_sec_mismatch,
    'expected data but found end of stream': func_sec_mismatch,
    'Invalid var_i32/i64': illegal_int_encoding,
    'integer too large': illegal_int_encoding,
    'Invalid signed LEB encoding': illegal_int_encoding,
    'section size mismatch': section_mismatch,
    'table index out of bounds': table_OOB,
    'out of bounds table access': table_OOB,
    'outOfBoundsTableAccess': table_OOB,
    'unsupported opcode fc': fc_opcode,
    'unsupported opcode fd': fd_opcode,
    'Unknown 0xfd subopcode': fd_opcode,
    'SIMD support is not enabled': fd_opcode,
    'v128 value type requires simd feature': fd_opcode,
    'illegal opcode': illegal_opcode,
    'Unknown opcode': illegal_opcode,
    'unsupported opcode': illegal_opcode,
    'multi-memory not enabled': multi_memory_unsupport,
    'bulk memory support is not enabled': multi_memory_unsupport,
    'multi-memory support is not enabled': multi_memory_unsupport,
    'memoryIndex must be less than module.memories.size':memory_OOB,
    'reachedUnreachable': unreachable,
    'Unknown 0xfc subopcode': fc_opcode,
    'out of bounds memory access': memory_OOB,
    'outOfBoundsMemoryAccess': memory_OOB,
    'type mismatch': type_mismatch,
    'unexpected end-of-file': unexpected_EOF,
    'Unexpected EOF': unexpected_EOF,
    'alignment must not be larger than natural': large_alignment,
    'alignment greater than natural alignment': large_alignment,
    'alignment too large': large_alignment,
    'Mismatched memory alignment': illegal_alignment,
    'Invalid alignment': illegal_alignment,
    'reference types support is not enabled': reference_unsupport,
    'locals exceed maximum': too_many_local,
    'outOfBoundsElemSegmentAccess': elem_seg_oob,
    'elemSegmentIndex must be less than module.elemSegments.size()': elem_seg_oob,
    'compiling function overran its stack height limit': stack_operand_overflow,
    'wasm operand stack overflow': stack_operand_overflow,
    'depth must be less than controlStack': control_structure_depth_related,
    'Expected non-empty control stack': control_structure_depth_related,
    'stack was not empty at end of control structure': control_structure_depth_related
}



to_category_dict = {
        'unknown memory': 'unknown memory',
        'unknown table': 'unknown table',
        'memory index reserved byte must be zero': 'memory index reserved byte must be zero',
        'invalid lane index': 'invalid lane index',
        'local index out of bounds': 'local index out of bounds',
        'function index out of bounds':'function index out of bounds',
        'zero byte expected': 'zero byte expected',
        'invalid function type': 'invalid function type',
        'invalid local type': 'invalid local type ',
        'validation failed: unknown label': 'validation failed: unknown label',
        'tail calls support is not enabled': 'tail calls support is not enabled',
        'malformed value type': 'malformed value type',
}

# content_relation2 = {
#     'wasm operand stack overflow': '',
#     'compiling function overran its stack height limit': '',
#     'v128 value type requires simd feature': '',
# }
content_relation0 = {
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
    'Invalid var_i32': 'Invalid var_i32/i64',
    'Invalid var_i64': 'Invalid var_i32/i64',
    'zero byte expected': 'zero byte expected',
    'out of bounds memory access': 'out of bounds memory access',
    'outOfBoundsMemoryAccess': 'outOfBoundsMemoryAccess',
    'reachedUnreachable': 'reachedUnreachable',
    'Unknown 0xfc subopcode': 'Unknown 0xfc subopcode',
    'memoryIndex must be less than module.memories.size': 'memoryIndex must be less than module.memories.size',
    'function index out of bounds':'function index out of bounds',
    'invalid function type': 'invalid function type',
    'Unknown 0xfd subopcode': 'Unknown 0xfd subopcode',
    'invalid local type': 'invalid local type ',
    'depth must be less than controlStack': 'depth must be less than controlStack',
    'validation failed: unknown label': 'validation failed: unknown label',
    'out of bounds table access': 'out of bounds table access',
    'Validation error: locals exceed maximum': 'locals exceed maximum',
    'outOfBoundsElemSegmentAccess': 'outOfBoundsElemSegmentAccess',
    'ail calls support is not enabled': 'ail calls support is not enabled',
    'malformed value type': 'malformed value type',
    'multi-memory not enabled': 'multi-memory not enabled',
    'outOfBoundsTableAccess': 'outOfBoundsTableAccess',
    'v128 value type requires simd feature': 'v128 value type requires simd feature',
    'compiling function overran its stack height limit': 'compiling function overran its stack height limit',
    'wasm operand stack overflow': 'wasm operand stack overflow'
}

content_relation2 = {
    'type mismatch': 'type mismatch',
    'trailing bytes at end of section': 'trailing bytes at end of section',
    'integer too large': 'integer too large',
    'Invalid signed LEB encoding': 'Invalid signed LEB encoding',
    'section size mismatch': 'section size mismatch',
    'unsupported opcode fd': '',
    'unsupported opcode fc': '',
    'Unknown opcode':'Unknown opcode',
    'unknown memory': 'unknown memory',
    'unknown table': 'unknown table',
    'bulk memory support is not enabled': '',
    'ulti-memory support is not enabled': '',
    'memory index reserved byte must be zero': 'memory index reserved byte must be zero',
    'SIMD support is not enabled': '',
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
    'reference types support is not enabled': '',
    'unexpected end-of-file': 'unexpected end-of-file',
    'Invalid var_i32': 'Invalid var_i32/i64',
    'Invalid var_i64': 'Invalid var_i32/i64',
    'zero byte expected': 'zero byte expected',
    'out of bounds memory access': 'out of bounds memory access',
    'outOfBoundsMemoryAccess': 'outOfBoundsMemoryAccess',
    'reachedUnreachable': 'reachedUnreachable',
    'Unknown 0xfc subopcode': '',
    'memoryIndex must be less than module.memories.size': 'memoryIndex must be less than module.memories.size',
    'function index out of bounds':'function index out of bounds',
    'invalid function type': 'invalid function type',
    'Unknown 0xfd subopcode': '',
    'invalid local type': 'invalid local type ',
    'depth must be less than controlStack': 'depth must be less than controlStack',
    'validation failed: unknown label': 'validation failed: unknown label',
    'out of bounds table access': 'out of bounds table access',
    ' wasm operand stack overflow': '',
    'Validation error: locals exceed maximum': '',
    'outOfBoundsElemSegmentAccess': 'outOfBoundsElemSegmentAccess',
    'ail calls support is not enabled': 'ail calls support is not enabled',
    'compiling function overran its stack height limit': '',
    'v128 value type requires simd feature': '',
    'malformed value type': 'malformed value type',
    'multi-memory not enabled': 'multi-memory not enabled',
    'outOfBoundsTableAccess': 'outOfBoundsTableAccess'
}



@lru_cache(maxsize=1024, typed=False)
def extract_keyword_from_content(content, strategy='all'):
    if strategy == 'all':
        content_relation = content_relation0
    elif strategy == 's1':
        content_relation = content_relation2
    else:
        assert 0
    lower_content = content.lower()
    for k, v in content_relation.items():
        if k.lower() in lower_content:
            content = v
    return content


@lru_cache(maxsize=1024, typed=False)
def summary_level2(content):
    lower_content = content.lower()
    for k, v in categorize_info_level1.items():
        if k.lower() in lower_content:
            content = v
    return content

