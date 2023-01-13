import numpy as np
import struct
import leb128


# def print_bytearray(ba):
#     print([hex(x) for x in ba])

# pinf_32 = struct.pack('<f', np.inf)
# pinf_64 = struct.pack('<d', np.inf)
# ninf_32 = struct.pack('<f', -np.inf)
# ninf_64 = struct.pack('<d', -np.inf)
# print_bytearray(pinf_32)
# print_bytearray(pinf_64)
# print_bytearray(ninf_32)
# print_bytearray(ninf_64)

# pinf_32 = struct.pack('<f', np.nan)
# pinf_64 = struct.pack('<d', np.nan)
# ninf_32 = struct.pack('<f', -np.nan)
# ninf_64 = struct.pack('<d', -np.nan)

# print_bytearray(pinf_32)
# print_bytearray(pinf_64)
# print_bytearray(ninf_32)
# print_bytearray(ninf_64)

# 在wasm里面直接编码得到的 +nan 32 00 00 C0 7F
# 在wasm里面直接编码得到的 -nan 32 00 00 C0 FF
# 在wasm里面直接编码得到的 +nan 64 00 00 00 00 00 00 F8 7F
# 在wasm里面直接编码得到的 -nan 64 00 00 00 00 00 00 F8 FF

print(leb128.u.encode(3))
