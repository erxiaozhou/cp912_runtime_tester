from file_util import read_bytes, write_bytes

p1 = './ori_tcs/tcs_v2/i32.add_12.wasm'
p2 = './ori_tcs/tcs_v2/i32.add_13.wasm'
p3 = './ori_tcs/tcs_v2/v128.const_0.wasm'
p4 = './ori_tcs/tcs_v2/v128.const_1.wasm'

ba1 = read_bytes(p1)
ba2 = read_bytes(p2)
ba3 = read_bytes(p3)


# for i in range(500):
#     if ba1[i] == ba2[i]:
#         print(hex(ba1[i]), end=' ')
#     else:
#         break

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
write_bytes('./byte_mask/local_set_nonv128', local_set_nonv128)


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
write_bytes('./byte_mask/local_set_v128', local_set_v128)