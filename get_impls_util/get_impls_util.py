from wasm_impl_util import fullDumpRuntime
from wasm_impl_util import uninstRuntime
# from impl_paras import impl_paras
from .impl_paras_std import impl_paras_std
from .impl_paras_std_release import impl_paras_std_release


def get_std_impls():
    impls = []
    for name in impl_paras_std.keys():
        impl = fullDumpRuntime.from_dict(name, impl_paras_std[name])
        impls.append(impl)
    return impls


def get_std_uninst_impls():
    impls = []
    for name in impl_paras_std.keys():
        impl = uninstRuntime.from_std_dict(name, impl_paras_std[name])
        impls.append(impl)
    return impls


def get_lastest_uninst_impls():
    impls = []
    for name in impl_paras_std.keys():
        impl = uninstRuntime.from_lastest_dict(name, impl_paras_std[name])
        impls.append(impl)
    return impls


def get_std_release_impls():
    impls = []
    for name in impl_paras_std_release.keys():
        impl = fullDumpRuntime.from_dict(name, impl_paras_std_release[name])
        impls.append(impl)
    return impls
