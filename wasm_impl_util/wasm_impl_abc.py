from abc import ABC
from abc import abstractclassmethod


class Wasm_impl(ABC):
    @abstractclassmethod
    def execute_and_collect(self):
        pass
