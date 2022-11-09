import random
import fuzzingbook
from fuzzingbook.Fuzzer import RandomFuzzer
from fuzzingbook.MutationFuzzer import MutationFuzzer

from byte_seq_mutator import mutate
from extract_dump.wasmedge_extract_dump import wasmedge_dumped_data
from file_util import check_dir
class a:
    path = 'abc'
    def print():
        print(a.path)
class b:
    path = 'abac'
    def print():
        print(b.path)
class c:
    path = 'afbc'
    def print():
        print(c.path)
if __name__ == '__main__':
    extractor = wasmedge_dumped_data('result_only2/f32.div_32/wasmedge_dump_f32.div_32-store-part')
    print(extractor.__dir__())
    print(extractor.__dict__.keys())
