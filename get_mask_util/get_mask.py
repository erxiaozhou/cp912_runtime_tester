from file_util import read_bytes, write_bytes


local_set_nonv128_ba = read_bytes('./get_mask_util/byte_mask/local_set_nonv128')
local_get_nonv128_ba = read_bytes('./get_mask_util/byte_mask/local_get_nonv128')
local_set_v128_ba = read_bytes('./get_mask_util/byte_mask/local_set_v128')
local_get_v128_ba = read_bytes('./get_mask_util/byte_mask/local_get_v128')


def get_byte_mask_range(base):
    r = _get_mask_idx(base, [local_set_v128_ba, local_get_v128_ba])
    if len(r) == 0:
        r = _get_mask_idx(base, [local_set_nonv128_ba, local_get_nonv128_ba])
    # ! 有点严格，暂时先这样写，v2.0里也理应是这样
    assert len(r) in [0, 2]
    # assert len(r) == 2, print(len(r),r, [hex(x) for x in bytearray(base)], '\n', [hex(x) for x in local_set_nonv128_ba], [hex(x) for x in local_get_nonv128_ba])
    return r


def _get_mask():
    p1 = './get_mask_util/get_mask_tcs/i32.add_12.wasm'
    p3 = './get_mask_util/get_mask_tcs/v128.const_0.wasm'

    ba1 = read_bytes(p1)
    ba3 = read_bytes(p3)

    local_set_start_nonv128 = bytearray([0x41, 0xF8, 0xAC])
    local_set_end_nonv128 = bytearray([0x46, 0x21, 0x03])
    local_set_start_idx = ba1.find(local_set_start_nonv128)
    local_set_end_idx = ba1.find(local_set_end_nonv128) + len(local_set_end_nonv128)
    local_set_nonv128 = ba1[local_set_start_idx:local_set_end_idx]

    local_get_start_nonv128 = bytearray([0x20, 0x00])
    local_get_end_nonv128 = bytearray([0x24, 0x0b])
    local_get_start_idx = ba1.find(local_get_start_nonv128)
    local_get_end_idx = ba1.find(local_get_end_nonv128) + len(local_get_end_nonv128)
    local_get_nonv128 = ba1[local_get_start_idx:local_get_end_idx]

    print([hex(x) for x in local_set_nonv128])
    print([hex(x) for x in local_get_nonv128])
    write_bytes('./get_mask_util/byte_mask/local_set_nonv128', local_set_nonv128)
    write_bytes('./get_mask_util/byte_mask/local_get_nonv128', local_get_nonv128)


    local_set_start_v128 = bytearray([0x41, 0xF8, 0xAC])
    local_set_end_v128 = bytearray([0x21, 0x04])
    local_set_start_idx = ba3.find(local_set_start_v128)
    local_set_end_idx = ba3.find(local_set_end_v128) + len(local_set_end_v128)
    local_set_v128 = ba3[local_set_start_idx:local_set_end_idx]

    local_get_start_v128 = bytearray([0x20, 0x00])
    local_get_end_v128 = bytearray([0x24, 0x0c])
    local_get_start_idx = ba3.find(local_get_start_v128)
    local_get_end_idx = ba3.find(local_get_end_v128) + len(local_get_end_v128)
    local_get_v128 = ba3[local_get_start_idx:local_get_end_idx]

    print([hex(x) for x in local_set_v128])
    print([hex(x) for x in local_get_v128])
    write_bytes('./get_mask_util/byte_mask/local_set_v128', local_set_v128)
    write_bytes('./get_mask_util/byte_mask/local_get_v128', local_get_v128)


def _get_mask_idx(base, masks):
    assert isinstance(base, bytearray)
    for m in masks:
        assert isinstance(m, bytearray)
    r = []
    for m in masks:
        start_idx = base.find(m)
        r_ = [start_idx, start_idx + len(m)]
        if r_[0] != -1:
            r.append(r_)
    return r
