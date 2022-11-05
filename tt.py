import random
import fuzzingbook
from fuzzingbook.Fuzzer import RandomFuzzer
from fuzzingbook.MutationFuzzer import MutationFuzzer

from byte_seq_mutator import mutate
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
    L = [a, b, c]
    for obj in L:
        obj.print()
