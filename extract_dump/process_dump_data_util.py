import numpy as np


def get_int(bytes_):
    return int.from_bytes(bytes_, 'little')


def get_f32(bytes_):
    return np.frombuffer(bytes_, np.float32)[0]


def get_f64(bytes_):
    return np.frombuffer(bytes_, np.float64)[0]


def get_u64(bytes_):
    return np.frombuffer(bytes_, np.uint64)[0]


def get_f32_h10(bs):
    int_val = int.from_bytes(bs, byteorder='little', signed=False)
    highest_32_10 = 0b0111111111 << 22
    int_val = int_val & highest_32_10
    val = bytearray(int.to_bytes(int_val, 4, byteorder='little', signed=False))
    return val


def get_f64_h13(bs):
    int_val = int.from_bytes(bs, byteorder='little', signed=False)
    highest_64_13 = 0b0111111111111 << 51
    int_val = int_val & highest_64_13
    val = bytearray(int.to_bytes(int_val, 8, byteorder='little', signed=False))
    return val
